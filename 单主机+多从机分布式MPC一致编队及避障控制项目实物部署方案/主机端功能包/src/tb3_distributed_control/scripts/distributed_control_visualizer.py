#!/usr/bin/env python3

import rospy
import numpy as np
from geometry_msgs.msg import PoseStamped, PointStamped, Point
from nav_msgs.msg import Path, Odometry
from std_msgs.msg import Float64MultiArray
from visualization_msgs.msg import Marker, MarkerArray
import tf.transformations as tf

class DistributedControlVisualizer:
    def __init__(self):
        rospy.init_node('distributed_control_visualizer')
        
        # 🚀 修复: 先初始化数据存储，再创建订阅者（避免回调时属性未初始化）
        # Data storage
        self.leader_path = Path()
        self.leader_path.header.frame_id = "odom"
        
        self.robot_paths = []
        for i in range(5):
            path = Path()
            path.header.frame_id = "odom"
            self.robot_paths.append(path)
        
        # Current robot positions for markers
        self.robot_positions = [None] * 5
        
        # Publishers for visualization
        self.leader_path_pub = rospy.Publisher('/leader/path', Path, queue_size=1)  # 🚀 优化: 轨迹实时性
        self.leader_pose_pub = rospy.Publisher('/leader/pose', PoseStamped, queue_size=1)  # 🚀 优化: 位置实时性
        self.leader_marker_pub = rospy.Publisher('/leader/marker', Marker, queue_size=1)  # 🚀 优化: 标记实时性
        self.robots_markers_pub = rospy.Publisher('/robots/markers', MarkerArray, queue_size=1)  # 🚀 优化: 机器人标记实时性
        
        # Robot path publishers
        self.robot_path_pubs = []
        for i in range(5):
            pub = rospy.Publisher(f'/tb3_{i}/path', Path, queue_size=1)  # 🚀 优化: 机器人轨迹实时性
            self.robot_path_pubs.append(pub)
        
        # Subscribers (创建在数据存储初始化之后)
        # 获取虚拟领导者命名空间并订阅其状态
        virtual_leader_ns = rospy.get_param("/virtual_leader_ns", "tb3_virtual_leader")
        rospy.Subscriber(f'/{virtual_leader_ns}/state', Float64MultiArray, self.leader_state_callback)
        rospy.loginfo(f"可视化节点订阅虚拟领导者状态话题: /{virtual_leader_ns}/state")
        
        # Robot odometry subscribers
        self.robot_odom_subs = []
        for i in range(5):
            sub = rospy.Subscriber(f'/tb3_{i}/odom', 
                                 Odometry, 
                                 lambda msg, robot_id=i: self.robot_odom_callback(msg, robot_id))
            self.robot_odom_subs.append(sub)
        
        # Timer for publishing
        self.timer = rospy.Timer(rospy.Duration(0.1), self.publish_visualizations)
        
        # 发布机器人五边形标记到单独的话题
        self.robot_polygon_pub = rospy.Publisher('/robots/polygon', Marker, queue_size=10)

        rospy.loginfo("Distributed Control Visualizer initialized")

    def leader_state_callback(self, msg):
        """处理虚拟领导者状态数据"""
        if len(msg.data) >= 6:  # 格式：[时间, x, y, u_x, u_y, theta]
            time_stamp = msg.data[0]
            x = msg.data[1]
            y = msg.data[2]
            u_x = msg.data[3]
            u_y = msg.data[4]
            theta = msg.data[5]
            
            # 创建PoseStamped
            pose = PoseStamped()
            pose.header.stamp = rospy.Time.now()
            pose.header.frame_id = "odom"
            pose.pose.position.x = x
            pose.pose.position.y = y
            pose.pose.position.z = 0.0
            
            # 设置方向
            q = tf.quaternion_from_euler(0, 0, theta)
            pose.pose.orientation.x = q[0]
            pose.pose.orientation.y = q[1]
            pose.pose.orientation.z = q[2]
            pose.pose.orientation.w = q[3]
            
            # 添加到路径
            self.leader_path.poses.append(pose)
            self.leader_path.header.stamp = rospy.Time.now()
            
            # 限制路径长度以避免内存问题
            if len(self.leader_path.poses) > 1000:
                self.leader_path.poses.pop(0)
                
        elif len(msg.data) >= 3:  # 备用格式：至少有时间、x、y
            time_stamp = msg.data[0]
            x = msg.data[1]
            y = msg.data[2]
            
            # 创建PoseStamped
            pose = PoseStamped()
            pose.header.stamp = rospy.Time.now()
            pose.header.frame_id = "odom"
            pose.pose.position.x = x
            pose.pose.position.y = y
            pose.pose.position.z = 0.0
            pose.pose.orientation.w = 1.0  # 默认方向
            
            # 添加到路径
            self.leader_path.poses.append(pose)
            self.leader_path.header.stamp = rospy.Time.now()
            
            # 限制路径长度
            if len(self.leader_path.poses) > 1000:
                self.leader_path.poses.pop(0)

    def robot_odom_callback(self, msg, robot_id):
        """处理机器人里程计数据"""
        try:
            # 从里程计消息中提取位置信息
            pose = PoseStamped()
            pose.header.stamp = rospy.Time.now()
            pose.header.frame_id = "odom"
            pose.pose.position.x = msg.pose.pose.position.x
            pose.pose.position.y = msg.pose.pose.position.y
            pose.pose.position.z = 0.0
            pose.pose.orientation = msg.pose.pose.orientation
            
            # 添加到对应机器人的路径
            self.robot_paths[robot_id].poses.append(pose)
            self.robot_paths[robot_id].header.stamp = rospy.Time.now()
            
            # 更新机器人位置用于标记显示
            self.robot_positions[robot_id] = pose.pose.position
            
            # 限制路径长度
            if len(self.robot_paths[robot_id].poses) > 500:
                self.robot_paths[robot_id].poses.pop(0)
                
        except Exception as e:
            # 如果消息格式不对，尝试简单的位置更新
            rospy.logwarn_throttle(5.0, f"Robot {robot_id} odom callback error: {e}")

    def create_leader_marker(self):
        """创建虚拟领导者标记"""
        marker = Marker()
        marker.header.frame_id = "odom"
        marker.header.stamp = rospy.Time.now()
        marker.ns = "leader"
        marker.id = 0
        marker.type = Marker.CYLINDER
        marker.action = Marker.ADD
        
        # 如果有路径点，使用最新位置
        if self.leader_path.poses:
            latest_pose = self.leader_path.poses[-1]
            marker.pose.position = latest_pose.pose.position
            marker.pose.position.z = 0.1  # 稍微抬高
            marker.pose.orientation.w = 1.0
        else:
            marker.pose.position.x = 0.3
            marker.pose.position.y = 0.0
            marker.pose.position.z = 0.1
            marker.pose.orientation.w = 1.0
        
        # 设置大小和颜色
        marker.scale.x = 0.2
        marker.scale.y = 0.2
        marker.scale.z = 0.05
        marker.color.r = 1.0
        marker.color.g = 0.0
        marker.color.b = 0.0
        marker.color.a = 0.8
        
        return marker

    def create_robot_markers(self):
        """创建机器人标记数组"""
        marker_array = MarkerArray()

        # 定义颜色与轨迹一致
        colors = [
            (0.0, 1.0, 0.0),  # 绿色
            (0.0, 0.0, 1.0),  # 蓝色
            (1.0, 1.0, 0.0),  # 黄色
            (1.0, 0.0, 1.0),  # 紫色
            (0.0, 1.0, 1.0),  # 青色
        ]

        for i in range(5):
            marker = Marker()
            marker.header.frame_id = "odom"
            marker.header.stamp = rospy.Time.now()
            marker.ns = f"robot_{i}"
            marker.id = i
            marker.type = Marker.SPHERE
            marker.action = Marker.ADD

            # 使用存储的位置或默认位置
            if self.robot_positions[i] is not None:
                marker.pose.position = self.robot_positions[i]
                marker.pose.position.z = 0.1
            else:
                # 默认位置
                marker.pose.position.x = 0.0
                marker.pose.position.y = 0.0
                marker.pose.position.z = 0.1

            marker.pose.orientation.w = 1.0

            # 设置大小和颜色
            marker.scale.x = 0.15
            marker.scale.y = 0.15
            marker.scale.z = 0.05
            marker.color.r = colors[i][0]
            marker.color.g = colors[i][1]
            marker.color.b = colors[i][2]
            marker.color.a = 0.8

            marker_array.markers.append(marker)

        return marker_array

    def create_robot_polygon_marker(self):
        """创建机器人五边形标记，只在所有机器人位置数据可用时绘制"""
        marker = Marker()
        marker.header.frame_id = "odom"
        marker.header.stamp = rospy.Time.now()
        marker.ns = "robot_polygon"
        marker.id = 100  # 唯一标识符
        marker.type = Marker.LINE_STRIP  # 使用线条连接
        marker.action = Marker.ADD

        # 设置线条颜色和宽度
        marker.scale.x = 0.02  # 线条宽度，调整为更细
        marker.color.r = 1.0  # 红色
        marker.color.g = 0.0
        marker.color.b = 0.0
        marker.color.a = 0.8

        # 设置单位四元数以消除警告
        marker.pose.orientation.x = 0.0
        marker.pose.orientation.y = 0.0
        marker.pose.orientation.z = 0.0
        marker.pose.orientation.w = 1.0

        # 首先检查所有机器人位置是否都可用
        available_positions = [pos for pos in self.robot_positions if pos is not None]
        
        if len(available_positions) < 5:
            # 如果机器人位置数据不完整，记录调试信息但不生成警告
            rospy.logdebug(f"等待所有机器人位置数据，当前可用: {len(available_positions)}/5")
            # 返回空的marker，避免在RViz中显示不完整的图形
            marker.action = Marker.DELETE
            return marker

        # 添加机器人位置点（所有5个机器人都有位置数据）
        for i in range(5):
            point = Point()
            point.x = self.robot_positions[i].x
            point.y = self.robot_positions[i].y
            point.z = self.robot_positions[i].z
            marker.points.append(point)

        # 闭合五边形
        marker.points.append(marker.points[0])

        return marker

    def publish_visualizations(self, event):
        """定时发布可视化数据"""
        try:
            # 发布领导者路径
            if self.leader_path.poses:
                self.leader_path_pub.publish(self.leader_path)

                # 发布领导者当前位置
                latest_pose = self.leader_path.poses[-1]
                self.leader_pose_pub.publish(latest_pose)

            # 发布领导者标记
            leader_marker = self.create_leader_marker()
            self.leader_marker_pub.publish(leader_marker)

            # 发布机器人路径
            for i, path in enumerate(self.robot_paths):
                if path.poses:
                    self.robot_path_pubs[i].publish(path)

            # 发布机器人标记
            robot_markers = self.create_robot_markers()
            self.robots_markers_pub.publish(robot_markers)

            # 发布机器人五边形标记到单独的话题
            robot_polygon_marker = self.create_robot_polygon_marker()
            self.robot_polygon_pub.publish(robot_polygon_marker)

        except Exception as e:
            rospy.logwarn_throttle(5.0, f"Visualization publish error: {e}")

if __name__ == '__main__':
    try:
        visualizer = DistributedControlVisualizer()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
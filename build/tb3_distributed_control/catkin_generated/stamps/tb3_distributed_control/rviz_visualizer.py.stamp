#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RViz实时轨迹可视化节点
功能：通过RViz显示5个机器人和领导者的编队轨迹，支持实时更新
作者：分布式控制系统
创建时间：2025年10月6日
"""

import rospy
import numpy as np
from std_msgs.msg import Float64MultiArray, Bool, ColorRGBA
from nav_msgs.msg import Odometry, Path
from geometry_msgs.msg import PoseStamped, Point, Vector3
from visualization_msgs.msg import Marker, MarkerArray
import tf2_ros
import tf2_geometry_msgs
from datetime import datetime
import threading

class RVizVisualizer:
    def __init__(self):
        rospy.init_node("rviz_visualizer", anonymous=True)
        
        # 数据存储
        self.robots_data = {i: {'path': Path(), 'ref_path': Path()} for i in range(5)}
        self.leader_data = {'path': Path()}
        
        # 当前位置
        self.current_positions = {i: {'x': 0.0, 'y': 0.0} for i in range(5)}
        self.current_leader = {'x': 0.3, 'y': 0.0}
        
        # 控制参数
        self.max_path_points = 1000  # 最大路径点数
        self.update_interval = 0.1   # 更新间隔(s)
        self.is_running = True
        self.data_lock = threading.Lock()
        
        # 机器人颜色配置
        self.robot_colors = [
            ColorRGBA(0.0, 0.0, 1.0, 1.0),  # 蓝色
            ColorRGBA(1.0, 0.65, 0.0, 1.0), # 橙色
            ColorRGBA(0.0, 0.8, 0.0, 1.0),  # 绿色
            ColorRGBA(1.0, 0.0, 0.0, 1.0),  # 红色
            ColorRGBA(0.5, 0.0, 0.5, 1.0)   # 紫色
        ]
        self.leader_color = ColorRGBA(0.0, 0.0, 0.0, 1.0)  # 黑色
        
        # 初始化发布器
        self.setup_publishers()
        
        # 初始化订阅器
        self.setup_subscribers()
        
        # 启动定时更新
        self.timer = rospy.Timer(rospy.Duration(self.update_interval), self.update_markers)
        
        # 注册关闭回调
        rospy.on_shutdown(self.shutdown_callback)
        
        rospy.loginfo("RViz实时轨迹可视化节点启动成功！")
        
    def setup_publishers(self):
        """设置发布器"""
        # 路径发布器（机器人轨迹线）
        self.path_pubs = {}
        self.ref_path_pubs = {}
        
        for i in range(5):
            # 实际轨迹路径
            self.path_pubs[i] = rospy.Publisher(f"/robot_{i}/trajectory", Path, queue_size=10)
            # 参考轨迹路径
            self.ref_path_pubs[i] = rospy.Publisher(f"/robot_{i}/reference_trajectory", Path, queue_size=10)
        
        # 领导者轨迹路径
        self.leader_path_pub = rospy.Publisher("/leader/trajectory", Path, queue_size=10)
        
        # 标记发布器（机器人当前位置、编队形状等）
        self.marker_pub = rospy.Publisher("/formation_markers", MarkerArray, queue_size=10)
        
        # 编队质心轨迹
        self.centroid_path_pub = rospy.Publisher("/formation/centroid_trajectory", Path, queue_size=10)
        self.centroid_path = Path()
        
    def setup_subscribers(self):
        """设置订阅器"""
        # 订阅机器人里程计
        for i in range(5):
            rospy.Subscriber(f"/tb3_{i}/odom", Odometry, 
                           self.robot_odom_callback, callback_args=i)
        
        # 订阅领导者状态
        rospy.Subscriber("/leader/state", Float64MultiArray, self.leader_callback)
        
        # 订阅系统停止信号
        rospy.Subscriber("/system/shutdown", Bool, self.shutdown_signal_callback)
    
    def robot_odom_callback(self, msg, robot_id):
        """机器人里程计回调"""
        with self.data_lock:
            x = msg.pose.pose.position.x
            y = msg.pose.pose.position.y
            
            # 更新当前位置
            self.current_positions[robot_id]['x'] = x
            self.current_positions[robot_id]['y'] = y
            
            # 创建新的路径点（使用Gazebo提供的里程计坐标系）
            pose_stamped = PoseStamped()
            pose_stamped.header = msg.header
            # 确保使用统一的坐标系，避免TF冲突
            pose_stamped.header.frame_id = "odom"  # 使用全局odom坐标系
            pose_stamped.pose = msg.pose.pose
            
            # 添加到机器人轨迹
            self.robots_data[robot_id]['path'].header.frame_id = "odom"
            self.robots_data[robot_id]['path'].header.stamp = rospy.Time.now()
            self.robots_data[robot_id]['path'].poses.append(pose_stamped)
            
            # 限制路径点数
            if len(self.robots_data[robot_id]['path'].poses) > self.max_path_points:
                self.robots_data[robot_id]['path'].poses.pop(0)
            
            # 安全发布轨迹路径
            try:
                self.path_pubs[robot_id].publish(self.robots_data[robot_id]['path'])
            except Exception:
                pass  # 忽略发布错误
    
    def leader_callback(self, msg):
        """领导者状态回调"""
        if len(msg.data) >= 3:
            with self.data_lock:
                x = msg.data[1]  # x0
                y = msg.data[2]  # y0
                
                # 更新当前领导者位置
                self.current_leader['x'] = x
                self.current_leader['y'] = y
                
                # 创建领导者路径点
                pose_stamped = PoseStamped()
                pose_stamped.header.frame_id = "odom"
                pose_stamped.header.stamp = rospy.Time.now()
                pose_stamped.pose.position.x = x
                pose_stamped.pose.position.y = y
                pose_stamped.pose.position.z = 0.1  # 稍微抬高显示
                pose_stamped.pose.orientation.w = 1.0
                
                # 添加到领导者轨迹
                self.leader_data['path'].header.frame_id = "odom"
                self.leader_data['path'].header.stamp = rospy.Time.now()
                self.leader_data['path'].poses.append(pose_stamped)
                
                # 限制路径点数
                if len(self.leader_data['path'].poses) > self.max_path_points:
                    self.leader_data['path'].poses.pop(0)
                
                # 发布领导者轨迹
                self.leader_path_pub.publish(self.leader_data['path'])
    
    def shutdown_signal_callback(self, msg):
        """系统停止信号回调"""
        if msg.data:
            rospy.loginfo("收到系统停止信号，RViz可视化即将关闭...")
            self.is_running = False
            # 立即停止定时器，避免关闭时的通信错误
            if hasattr(self, 'timer'):
                self.timer.shutdown()
            # 延迟关闭，让其他节点先完成保存
            rospy.Timer(rospy.Duration(1.0), self.delayed_shutdown, oneshot=True)
    
    def update_markers(self, event):
        """更新RViz标记"""
        if not self.is_running:
            return
        
        marker_array = MarkerArray()
        current_time = rospy.Time.now()
        
        with self.data_lock:
            # 1. 机器人当前位置标记
            for i in range(5):
                marker = Marker()
                marker.header.frame_id = "odom"
                marker.header.stamp = current_time
                marker.ns = "robots"
                marker.id = i
                marker.type = Marker.CYLINDER
                marker.action = Marker.ADD
                
                # 位置
                marker.pose.position.x = self.current_positions[i]['x']
                marker.pose.position.y = self.current_positions[i]['y']
                marker.pose.position.z = 0.05
                marker.pose.orientation.w = 1.0
                
                # 尺寸
                marker.scale.x = 0.2  # 直径
                marker.scale.y = 0.2
                marker.scale.z = 0.1  # 高度
                
                # 颜色
                marker.color = self.robot_colors[i]
                
                # 生存时间
                marker.lifetime = rospy.Duration(0.2)
                
                marker_array.markers.append(marker)
                
                # 机器人ID文本
                text_marker = Marker()
                text_marker.header.frame_id = "odom"
                text_marker.header.stamp = current_time
                text_marker.ns = "robot_labels"
                text_marker.id = i
                text_marker.type = Marker.TEXT_VIEW_FACING
                text_marker.action = Marker.ADD
                
                text_marker.pose.position.x = self.current_positions[i]['x']
                text_marker.pose.position.y = self.current_positions[i]['y']
                text_marker.pose.position.z = 0.3
                text_marker.pose.orientation.w = 1.0
                
                text_marker.scale.z = 0.15  # 文字大小
                text_marker.color = ColorRGBA(1.0, 1.0, 1.0, 1.0)  # 白色
                text_marker.text = f"R{i}"
                text_marker.lifetime = rospy.Duration(0.2)
                
                marker_array.markers.append(text_marker)
            
            # 2. 领导者位置标记
            leader_marker = Marker()
            leader_marker.header.frame_id = "odom"
            leader_marker.header.stamp = current_time
            leader_marker.ns = "leader"
            leader_marker.id = 0
            leader_marker.type = Marker.SPHERE
            leader_marker.action = Marker.ADD
            
            leader_marker.pose.position.x = self.current_leader['x']
            leader_marker.pose.position.y = self.current_leader['y']
            leader_marker.pose.position.z = 0.1
            leader_marker.pose.orientation.w = 1.0
            
            leader_marker.scale.x = 0.25
            leader_marker.scale.y = 0.25
            leader_marker.scale.z = 0.25
            
            leader_marker.color = self.leader_color
            leader_marker.lifetime = rospy.Duration(0.2)
            
            marker_array.markers.append(leader_marker)
            
            # 领导者标签
            leader_text = Marker()
            leader_text.header.frame_id = "odom"
            leader_text.header.stamp = current_time
            leader_text.ns = "leader_label"
            leader_text.id = 0
            leader_text.type = Marker.TEXT_VIEW_FACING
            leader_text.action = Marker.ADD
            
            leader_text.pose.position.x = self.current_leader['x']
            leader_text.pose.position.y = self.current_leader['y']
            leader_text.pose.position.z = 0.4
            leader_text.pose.orientation.w = 1.0
            
            leader_text.scale.z = 0.2
            leader_text.color = ColorRGBA(1.0, 1.0, 0.0, 1.0)  # 黄色
            leader_text.text = "LEADER"
            leader_text.lifetime = rospy.Duration(0.2)
            
            marker_array.markers.append(leader_text)
            
            # 3. 编队连接线
            if len([pos for pos in self.current_positions.values() if pos['x'] != 0 or pos['y'] != 0]) >= 2:
                formation_lines = Marker()
                formation_lines.header.frame_id = "odom"
                formation_lines.header.stamp = current_time
                formation_lines.ns = "formation_lines"
                formation_lines.id = 0
                formation_lines.type = Marker.LINE_LIST
                formation_lines.action = Marker.ADD
                
                formation_lines.scale.x = 0.02  # 线宽
                formation_lines.color = ColorRGBA(0.5, 0.5, 0.5, 0.6)  # 灰色半透明
                formation_lines.lifetime = rospy.Duration(0.2)
                
                # 连接所有机器人（简单网格连接）
                for i in range(5):
                    for j in range(i+1, 5):
                        p1 = Point()
                        p1.x = self.current_positions[i]['x']
                        p1.y = self.current_positions[i]['y']
                        p1.z = 0.02
                        
                        p2 = Point()
                        p2.x = self.current_positions[j]['x']
                        p2.y = self.current_positions[j]['y']
                        p2.z = 0.02
                        
                        formation_lines.points.append(p1)
                        formation_lines.points.append(p2)
                
                marker_array.markers.append(formation_lines)
            
            # 4. 编队质心
            if len([pos for pos in self.current_positions.values() if pos['x'] != 0 or pos['y'] != 0]) > 0:
                # 计算质心
                centroid_x = sum(pos['x'] for pos in self.current_positions.values()) / 5
                centroid_y = sum(pos['y'] for pos in self.current_positions.values()) / 5
                
                # 质心标记
                centroid_marker = Marker()
                centroid_marker.header.frame_id = "odom"
                centroid_marker.header.stamp = current_time
                centroid_marker.ns = "centroid"
                centroid_marker.id = 0
                centroid_marker.type = Marker.CUBE
                centroid_marker.action = Marker.ADD
                
                centroid_marker.pose.position.x = centroid_x
                centroid_marker.pose.position.y = centroid_y
                centroid_marker.pose.position.z = 0.02
                centroid_marker.pose.orientation.w = 1.0
                
                centroid_marker.scale.x = 0.1
                centroid_marker.scale.y = 0.1
                centroid_marker.scale.z = 0.04
                
                centroid_marker.color = ColorRGBA(1.0, 1.0, 0.0, 0.8)  # 黄色半透明
                centroid_marker.lifetime = rospy.Duration(0.2)
                
                marker_array.markers.append(centroid_marker)
                
                # 添加质心到轨迹
                centroid_pose = PoseStamped()
                centroid_pose.header.frame_id = "odom"
                centroid_pose.header.stamp = current_time
                centroid_pose.pose.position.x = centroid_x
                centroid_pose.pose.position.y = centroid_y
                centroid_pose.pose.position.z = 0.02
                centroid_pose.pose.orientation.w = 1.0
                
                self.centroid_path.header.frame_id = "odom"
                self.centroid_path.header.stamp = current_time
                self.centroid_path.poses.append(centroid_pose)
                
                # 限制质心路径点数
                if len(self.centroid_path.poses) > self.max_path_points:
                    self.centroid_path.poses.pop(0)
                
                # 发布质心轨迹
                self.centroid_path_pub.publish(self.centroid_path)
        
        # 发布所有标记
        self.marker_pub.publish(marker_array)
    
    def delayed_shutdown(self, event):
        """延迟关闭函数，确保优雅退出"""
        try:
            rospy.loginfo("RViz可视化节点正在优雅关闭...")
            rospy.signal_shutdown("收到系统停止信号，RViz可视化正常关闭")
        except Exception as e:
            rospy.logwarn(f"RViz关闭时出现警告（可忽略）: {e}")
    
    def shutdown_callback(self):
        """节点关闭回调"""
        rospy.loginfo("正在关闭RViz可视化节点...")
        self.is_running = False
        
        try:
            # 停止定时器
            if hasattr(self, 'timer') and self.timer:
                self.timer.shutdown()
            
            # 清除所有标记，避免残留
            marker_array = MarkerArray()
            delete_marker = Marker()
            delete_marker.action = Marker.DELETEALL
            marker_array.markers.append(delete_marker)
            
            # 安全发布清除标记
            if hasattr(self, 'marker_pub') and self.marker_pub:
                self.marker_pub.publish(marker_array)
            
            rospy.loginfo("RViz可视化节点已安全关闭")
            
        except Exception as e:
            # 关闭时的连接错误是正常的，不需要报告为错误
            rospy.logdebug(f"RViz关闭时的连接断开（正常现象）: {e}")
    
    def update_markers(self, event):
        """更新RViz标记"""
        # 检查节点是否正在关闭，避免关闭时的通信错误
        if not self.is_running or rospy.is_shutdown():
            return
        
        try:
            marker_array = MarkerArray()
            current_time = rospy.Time.now()
            
            with self.data_lock:
                # 1. 机器人当前位置标记
                for i in range(5):
                    marker = Marker()
                    marker.header.frame_id = "odom"
                    marker.header.stamp = current_time
                    marker.ns = "robots"
                    marker.id = i
                    marker.type = Marker.CYLINDER
                    marker.action = Marker.ADD
                    
                    # 位置
                    marker.pose.position.x = self.current_positions[i]['x']
                    marker.pose.position.y = self.current_positions[i]['y']
                    marker.pose.position.z = 0.05
                    marker.pose.orientation.w = 1.0
                    
                    # 尺寸
                    marker.scale.x = 0.2  # 直径
                    marker.scale.y = 0.2
                    marker.scale.z = 0.1  # 高度
                    
                    # 颜色
                    marker.color = self.robot_colors[i]
                    
                    # 生存时间
                    marker.lifetime = rospy.Duration(0.2)
                    
                    marker_array.markers.append(marker)
                    
                    # 机器人ID文本
                    text_marker = Marker()
                    text_marker.header.frame_id = "odom"
                    text_marker.header.stamp = current_time
                    text_marker.ns = "robot_labels"
                    text_marker.id = i
                    text_marker.type = Marker.TEXT_VIEW_FACING
                    text_marker.action = Marker.ADD
                    
                    text_marker.pose.position.x = self.current_positions[i]['x']
                    text_marker.pose.position.y = self.current_positions[i]['y']
                    text_marker.pose.position.z = 0.3
                    text_marker.pose.orientation.w = 1.0
                    
                    text_marker.scale.z = 0.15  # 文字大小
                    text_marker.color = ColorRGBA(1.0, 1.0, 1.0, 1.0)  # 白色
                    text_marker.text = f"R{i}"
                    text_marker.lifetime = rospy.Duration(0.2)
                    
                    marker_array.markers.append(text_marker)
                
                # 2. 领导者位置标记
                leader_marker = Marker()
                leader_marker.header.frame_id = "odom"
                leader_marker.header.stamp = current_time
                leader_marker.ns = "leader"
                leader_marker.id = 0
                leader_marker.type = Marker.SPHERE
                leader_marker.action = Marker.ADD
                
                leader_marker.pose.position.x = self.current_leader['x']
                leader_marker.pose.position.y = self.current_leader['y']
                leader_marker.pose.position.z = 0.1
                leader_marker.pose.orientation.w = 1.0
                
                leader_marker.scale.x = 0.25
                leader_marker.scale.y = 0.25
                leader_marker.scale.z = 0.25
                
                leader_marker.color = self.leader_color
                leader_marker.lifetime = rospy.Duration(0.2)
                
                marker_array.markers.append(leader_marker)
                
                # 领导者标签
                leader_text = Marker()
                leader_text.header.frame_id = "odom"
                leader_text.header.stamp = current_time
                leader_text.ns = "leader_label"
                leader_text.id = 0
                leader_text.type = Marker.TEXT_VIEW_FACING
                leader_text.action = Marker.ADD
                
                leader_text.pose.position.x = self.current_leader['x']
                leader_text.pose.position.y = self.current_leader['y']
                leader_text.pose.position.z = 0.4
                leader_text.pose.orientation.w = 1.0
                
                leader_text.scale.z = 0.2
                leader_text.color = ColorRGBA(1.0, 1.0, 0.0, 1.0)  # 黄色
                leader_text.text = "LEADER"
                leader_text.lifetime = rospy.Duration(0.2)
                
                marker_array.markers.append(leader_text)
                
                # 3. 编队连接线
                if len([pos for pos in self.current_positions.values() if pos['x'] != 0 or pos['y'] != 0]) >= 2:
                    formation_lines = Marker()
                    formation_lines.header.frame_id = "odom"
                    formation_lines.header.stamp = current_time
                    formation_lines.ns = "formation_lines"
                    formation_lines.id = 0
                    formation_lines.type = Marker.LINE_LIST
                    formation_lines.action = Marker.ADD
                    
                    formation_lines.scale.x = 0.02  # 线宽
                    formation_lines.color = ColorRGBA(0.5, 0.5, 0.5, 0.6)  # 灰色半透明
                    formation_lines.lifetime = rospy.Duration(0.2)
                    
                    # 连接所有机器人（简单网格连接）
                    for i in range(5):
                        for j in range(i+1, 5):
                            p1 = Point()
                            p1.x = self.current_positions[i]['x']
                            p1.y = self.current_positions[i]['y']
                            p1.z = 0.02
                            
                            p2 = Point()
                            p2.x = self.current_positions[j]['x']
                            p2.y = self.current_positions[j]['y']
                            p2.z = 0.02
                            
                            formation_lines.points.append(p1)
                            formation_lines.points.append(p2)
                    
                    marker_array.markers.append(formation_lines)
                
                # 4. 编队质心
                if len([pos for pos in self.current_positions.values() if pos['x'] != 0 or pos['y'] != 0]) > 0:
                    # 计算质心
                    centroid_x = sum(pos['x'] for pos in self.current_positions.values()) / 5
                    centroid_y = sum(pos['y'] for pos in self.current_positions.values()) / 5
                    
                    # 质心标记
                    centroid_marker = Marker()
                    centroid_marker.header.frame_id = "odom"
                    centroid_marker.header.stamp = current_time
                    centroid_marker.ns = "centroid"
                    centroid_marker.id = 0
                    centroid_marker.type = Marker.CUBE
                    centroid_marker.action = Marker.ADD
                    
                    centroid_marker.pose.position.x = centroid_x
                    centroid_marker.pose.position.y = centroid_y
                    centroid_marker.pose.position.z = 0.02
                    centroid_marker.pose.orientation.w = 1.0
                    
                    centroid_marker.scale.x = 0.1
                    centroid_marker.scale.y = 0.1
                    centroid_marker.scale.z = 0.04
                    
                    centroid_marker.color = ColorRGBA(1.0, 1.0, 0.0, 0.8)  # 黄色半透明
                    centroid_marker.lifetime = rospy.Duration(0.2)
                    
                    marker_array.markers.append(centroid_marker)
                    
                    # 添加质心到轨迹
                    centroid_pose = PoseStamped()
                    centroid_pose.header.frame_id = "odom"
                    centroid_pose.header.stamp = current_time
                    centroid_pose.pose.position.x = centroid_x
                    centroid_pose.pose.position.y = centroid_y
                    centroid_pose.pose.position.z = 0.02
                    centroid_pose.pose.orientation.w = 1.0
                    
                    self.centroid_path.header.frame_id = "odom"
                    self.centroid_path.header.stamp = current_time
                    self.centroid_path.poses.append(centroid_pose)
                    
                    # 限制质心路径点数
                    if len(self.centroid_path.poses) > self.max_path_points:
                        self.centroid_path.poses.pop(0)
                    
                    # 发布质心轨迹
                    try:
                        self.centroid_path_pub.publish(self.centroid_path)
                    except Exception:
                        pass  # 忽略发布错误
            
            # 发布所有标记
            try:
                self.marker_pub.publish(marker_array)
            except Exception:
                pass  # 忽略发布错误，避免关闭时的连接错误干扰
                
        except Exception as e:
            if self.is_running:  # 只有在运行时才报告错误
                rospy.logwarn(f"更新标记时出现错误: {e}")

if __name__ == "__main__":
    try:
        visualizer = RVizVisualizer()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
    except Exception as e:
        rospy.logerr(f"RViz可视化节点运行错误：{e}")
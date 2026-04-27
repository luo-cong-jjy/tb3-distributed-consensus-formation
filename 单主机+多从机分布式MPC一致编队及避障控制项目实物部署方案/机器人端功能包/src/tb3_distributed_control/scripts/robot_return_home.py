#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
机器人返回初始位置控制脚本（支持单点和多航点模式，带避障功能）

功能说明：
    - 单点模式：机器人直接返回指定位置（默认原点）
    - 多航点模式：机器人依次经过多个中间点，最后返回原点（自动添加）
    - 使用高精度PID控制，位置精度±2cm，角度精度±3°
    - 激光雷达避障：检测前方（0°、±15°）障碍物，自动旋转避开

使用方法：

1. 单点模式（直接返回原点）：
   python3 robot_return_home.py
   python3 robot_return_home.py -n tb3_0
   python3 robot_return_home.py -n tb3_1

2. 单点模式（返回指定位置）：
   python3 robot_return_home.py -n tb3_0 -x 1.0 -y 0.5
   python3 robot_return_home.py -n tb3_0 -x 1.0 -y 0.5 -t 1.57

3. 多航点模式（经过中间点返回原点）：
   # 经过1个中间点返回原点
   python3 robot_return_home.py -n tb3_0 -w "1.5,1.5,0"
   
   # 经过2个中间点返回原点
   python3 robot_return_home.py -n tb3_0 -w "2.0,2.0,0" "1.0,1.0,0"
   
   # 经过3个中间点返回原点
   python3 robot_return_home.py -n tb3_0 -w "3.0,3.0,0" "2.0,1.0,0" "1.0,0.5,0"
   
   # 带角度的航点
   python3 robot_return_home.py -n tb3_1 -w "2.0,2.0,1.57" "1.0,1.0,0"

参数说明：
    -n, --namespace     机器人命名空间（默认：tb3_0）
    -w, --waypoints     航点列表，格式："x,y,theta" （自动添加原点为最后一点）
    -x, --target_x      目标X坐标（米，仅单点模式，默认：0.0）
    -y, --target_y      目标Y坐标（米，仅单点模式，默认：0.0）
    -t, --target_theta  目标角度（弧度，仅单点模式，默认：0.0）

避障参数：
    obstacle_threshold  障碍物检测距离阈值：0.8米（代码内修改）
    避障策略            检测到障碍物时停止前进，原地逆时针旋转（0.5 rad/s）
    检测范围            前方0°、左前方15°、右前方15°（345°）三个方向

注意事项：
    1. 航点格式：每个航点用逗号分隔 "x,y,theta"，中间不要有空格
    2. 角度单位：使用弧度制（π ≈ 3.14159，90° = 1.57）
    3. 多航点模式会自动在最后添加原点(0,0,0)
    4. 如果环境中有障碍物，建议使用多航点模式规划安全路径

常用角度转换：
    0° = 0       90° = 1.57    180° = 3.14    -90° = -1.57

示例场景：
    场景1：机器人在(3,3)位置，直接返回原点
        python3 robot_return_home.py -n tb3_0
    
    场景2：机器人在(3,3)位置，中间有障碍物，需要绕行
        python3 robot_return_home.py -n tb3_0 -w "0.2,3.0,0" "0.0,0.0,0"
        （先向下到(0.2,3.0)，再向左到(0.0,0.0)，最后到原点）
    
    场景3：5个机器人同时返回各自起点（使用多机器人模式）
        python3 robot_return_home.py --all
        python3 robot_return_home.py --robots tb3_0 tb3_1 tb3_2
        python3 robot_return_home.py --robots tb3_0 tb3_1 -w "2.0,2.0,0"
        python3 robot_return_home.py --all -w "0.2,2.8,0"

作者：分布式控制系统团队
日期：2026-01-08
"""

import rospy
import math
import sys
import threading
import numpy as np
from geometry_msgs.msg import Twist, PoseWithCovarianceStamped
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
from tf.transformations import euler_from_quaternion
import argparse

class RobotReturnHome:
    def __init__(self, namespace="", waypoints=None):
        """
        初始化机器人返回初始位置控制器
        Args:
            namespace: 机器人命名空间，如 "tb3_0", "tb3_1" 等
            waypoints: 航点列表 [(x1,y1,theta1), (x2,y2,theta2), ...], 最后一个点会自动添加为(0,0,0)
        """
        self.namespace = namespace
        
        # 航点模式
        self.waypoints = waypoints if waypoints else []
        self.current_waypoint_index = 0
        
        # 目标位置 (x, y, theta) - 初始化为第一个航点或原点
        if self.waypoints:
            self.target_x = self.waypoints[0][0]
            self.target_y = self.waypoints[0][1]
            self.target_theta = self.waypoints[0][2]
        else:
            self.target_x = 0.0
            self.target_y = 0.0 
            self.target_theta = 0.0
        
        # 当前位置
        self.current_x = 0.0
        self.current_y = 0.0
        self.current_theta = 0.0
        
        # 避障相关参数
        self.obstacle_threshold = 0.4  # 障碍物检测距离阈值（米）
        self.obstacle_detected = False  # 是否检测到障碍物
        self.laser_ranges = []  # 激光雷达数据
        
        # PID控制参数 - 位置
        self.linear_kp = 1.0    # 比例增益
        self.linear_ki = 0.01   # 积分增益
        self.linear_kd = 0.15   # 微分增益
        
        # PID控制参数 - 角度
        self.angular_kp = 1.5   # 比例增益
        self.angular_ki = 0.02  # 积分增益
        self.angular_kd = 0.2   # 微分增益
        
        # PID状态变量 - 位置
        self.linear_error_integral = 0.0
        self.linear_last_error = 0.0
        self.linear_integral_limit = 0.5  # 积分饱和限制
        
        # PID状态变量 - 角度
        self.angular_error_integral = 0.0
        self.angular_last_error = 0.0
        self.angular_integral_limit = 0.5  # 积分饱和限制
        
        # 速度限制
        self.max_linear_vel = 0.22   # 最大线速度 (m/s) - 提高速度
        self.max_angular_vel = 0.8   # 最大角速度 (rad/s) - 提高速度
        
        # 到达阈值（更严格）
        self.position_threshold = 0.02  # 位置阈值 (m) - 从5cm提高到2cm
        self.angle_threshold = 0.05     # 角度阈值 (rad) - 从0.1提高到0.05 (~3度)
        
        # 时间相关
        self.last_time = None
        self.control_rate = 20  # 控制频率 20Hz（提高控制频率）
        
        # ROS节点和话题设置
        if namespace:
            cmd_topic = f"/{namespace}/cmd_vel"
            odom_topic = f"/{namespace}/odom"
            scan_topic = f"/{namespace}/scan"
        else:
            cmd_topic = "/cmd_vel"
            odom_topic = "/odom"
            scan_topic = "/scan"
            
        # 发布器和订阅器
        self.cmd_pub = rospy.Publisher(cmd_topic, Twist, queue_size=10)
        self.odom_sub = rospy.Subscriber(odom_topic, Odometry, self.odom_callback)
        self.scan_sub = rospy.Subscriber(scan_topic, LaserScan, self.scan_callback)
        
        rospy.loginfo(f"机器人返回初始位置控制器启动")
        rospy.loginfo(f"命名空间: {namespace if namespace else '默认'}")
        rospy.loginfo(f"监听话题: {odom_topic}, {scan_topic}")
        rospy.loginfo(f"发布话题: {cmd_topic}")
        if self.waypoints:
            rospy.loginfo(f"多航点模式: 共 {len(self.waypoints)} 个航点")
            for i, wp in enumerate(self.waypoints):
                rospy.loginfo(f"  航点 {i+1}: ({wp[0]:.2f}, {wp[1]:.2f}, {wp[2]:.2f})")
        else:
            rospy.loginfo(f"单点模式 - 目标位置: ({self.target_x}, {self.target_y}, {self.target_theta})")
        
    def odom_callback(self, msg):
        """里程计回调函数，更新当前位姿"""
        # 获取位置
        self.current_x = msg.pose.pose.position.x
        self.current_y = msg.pose.pose.position.y
        
        # 获取角度
        orientation = msg.pose.pose.orientation
        _, _, yaw = euler_from_quaternion([
            orientation.x, orientation.y, orientation.z, orientation.w
        ])
        self.current_theta = yaw
    
    def scan_callback(self, msg):
        """激光雷达回调函数，用于障碍物检测"""
        self.laser_ranges = msg.ranges
        
        # 检查前方、左前方15度、右前方15度的距离（参考避障项目）
        if len(msg.ranges) > 0:
            # TurtleBot3雷达有360个点，0度在正前方
            front = msg.ranges[0] if len(msg.ranges) > 0 else float('inf')
            left_15 = msg.ranges[15] if len(msg.ranges) > 15 else float('inf')
            right_15 = msg.ranges[345] if len(msg.ranges) > 345 else float('inf')
            
            # 如果三个方向都大于阈值，则无障碍物
            if front > self.obstacle_threshold and left_15 > self.obstacle_threshold and right_15 > self.obstacle_threshold:
                self.obstacle_detected = False
            else:
                self.obstacle_detected = True
        else:
            self.obstacle_detected = False
    
    def normalize_angle(self, angle):
        """将角度规范化到[-pi, pi]"""
        while angle > math.pi:
            angle -= 2.0 * math.pi
        while angle < -math.pi:
            angle += 2.0 * math.pi
        return angle
        
    def calculate_control(self):
        """计算PID控制指令（带避障）"""
        # 计算时间增量
        current_time = rospy.Time.now()
        if self.last_time is None:
            self.last_time = current_time
            dt = 0.05  # 初始假设50ms
        else:
            dt = (current_time - self.last_time).to_sec()
            if dt <= 0:
                dt = 0.05
        self.last_time = current_time
        
        # 计算位置误差
        dx = self.target_x - self.current_x
        dy = self.target_y - self.current_y
        distance = math.sqrt(dx*dx + dy*dy)
        
        # 计算角度误差
        target_angle = math.atan2(dy, dx)
        angle_to_target = self.normalize_angle(target_angle - self.current_theta)
        angle_to_goal = self.normalize_angle(self.target_theta - self.current_theta)
        
        # 控制逻辑
        cmd = Twist()
        
        # 避障逻辑：如果检测到前方有障碍物（参考避障项目）
        if self.obstacle_detected and distance > self.position_threshold:
            # 停止前进，旋转避障
            cmd.linear.x = 0.0
            cmd.angular.z = 0.5  # 逆时针旋转
            rospy.logwarn_throttle(1.0, "⚠️ 检测到障碍物！正在避障...")
        
        # 如果距离目标位置较远，先转向目标点再前进
        elif distance > self.position_threshold:
            # 先确保朝向目标
            if abs(angle_to_target) > 0.2:  
                # 角度PID控制（转向目标）
                angular_error = angle_to_target
                self.angular_error_integral += angular_error * dt
                # 积分限幅
                self.angular_error_integral = max(min(self.angular_error_integral, 
                                                      self.angular_integral_limit), 
                                                  -self.angular_integral_limit)
                angular_derivative = (angular_error - self.angular_last_error) / dt
                self.angular_last_error = angular_error
                
                cmd.angular.z = (self.angular_kp * angular_error + 
                               self.angular_ki * self.angular_error_integral + 
                               self.angular_kd * angular_derivative)
                cmd.linear.x = 0.0
            else:  
                # 位置PID控制（前进）
                linear_error = distance
                self.linear_error_integral += linear_error * dt
                # 积分限幅
                self.linear_error_integral = max(min(self.linear_error_integral, 
                                                     self.linear_integral_limit), 
                                                 -self.linear_integral_limit)
                linear_derivative = (linear_error - self.linear_last_error) / dt
                self.linear_last_error = linear_error
                
                cmd.linear.x = (self.linear_kp * linear_error + 
                              self.linear_ki * self.linear_error_integral + 
                              self.linear_kd * linear_derivative)
                
                # 同时微调角度
                cmd.angular.z = 0.3 * self.angular_kp * angle_to_target
        else:
            # 已到达目标位置，调整最终朝向（PID控制）
            if abs(angle_to_goal) > self.angle_threshold:
                angular_error = angle_to_goal
                self.angular_error_integral += angular_error * dt
                self.angular_error_integral = max(min(self.angular_error_integral, 
                                                      self.angular_integral_limit), 
                                                  -self.angular_integral_limit)
                angular_derivative = (angular_error - self.angular_last_error) / dt
                self.angular_last_error = angular_error
                
                cmd.angular.z = (self.angular_kp * angular_error + 
                               self.angular_ki * self.angular_error_integral + 
                               self.angular_kd * angular_derivative)
                cmd.linear.x = 0.0
            else:
                # 已到达目标位置和朝向
                cmd.linear.x = 0.0
                cmd.angular.z = 0.0
                # 重置PID状态
                self.reset_pid()
                return cmd, True  # 返回已完成标志
        
        # 限制速度
        cmd.linear.x = max(min(cmd.linear.x, self.max_linear_vel), -self.max_linear_vel)
        cmd.angular.z = max(min(cmd.angular.z, self.max_angular_vel), -self.max_angular_vel)
        
        return cmd, False
    
    def reset_pid(self):
        """重置PID状态"""
        self.linear_error_integral = 0.0
        self.linear_last_error = 0.0
        self.angular_error_integral = 0.0
        self.angular_last_error = 0.0
    
    def switch_to_next_waypoint(self):
        """切换到下一个航点"""
        if not self.waypoints or self.current_waypoint_index >= len(self.waypoints) - 1:
            return False  # 没有下一个航点了
        
        self.current_waypoint_index += 1
        waypoint = self.waypoints[self.current_waypoint_index]
        self.target_x = waypoint[0]
        self.target_y = waypoint[1]
        self.target_theta = waypoint[2]
        
        # 重置PID状态
        self.reset_pid()
        
        rospy.loginfo("=" * 60)
        rospy.loginfo(f"✅ 航点 {self.current_waypoint_index} 已到达！")
        rospy.loginfo(f"🎯 切换到航点 {self.current_waypoint_index + 1}: ({self.target_x:.2f}, {self.target_y:.2f}, {self.target_theta:.2f})")
        rospy.loginfo("=" * 60)
        
        return True
        
    def run(self):
        """运行控制循环"""
        rate = rospy.Rate(self.control_rate)  # 使用更高的控制频率
        
        rospy.loginfo("等待里程计数据...")
        # 等待第一个里程计消息并获取有效数据
        first_data_received = False
        while not rospy.is_shutdown():
            rate.sleep()  # 先等待
            if hasattr(self, 'current_x'):  # 确保已接收到里程计数据
                # 再等待0.5秒确保数据稳定
                if not first_data_received:
                    first_data_received = True
                    rospy.loginfo(f"首次接收到里程计数据，等待数据稳定...")
                    rospy.sleep(0.5)
                break
            
        rospy.loginfo(f"开始返回初始位置（高精度PID控制）...")
        rospy.loginfo(f"当前位置: ({self.current_x:.4f}, {self.current_y:.4f}, {self.current_theta:.4f})")
        rospy.loginfo(f"精度目标: 位置±{self.position_threshold*100:.1f}cm, 角度±{math.degrees(self.angle_threshold):.1f}°")
        
        start_time = rospy.Time.now()
        timeout = 120.0  # 增加超时时间到120秒（高精度需要更多时间）
        
        while not rospy.is_shutdown():
            # 检查超时
            if (rospy.Time.now() - start_time).to_sec() > timeout:
                rospy.logwarn("返回初始位置超时！")
                break
                
            # 计算控制指令
            cmd, completed = self.calculate_control()
            
            # 发布控制指令
            self.cmd_pub.publish(cmd)
            
            # 打印当前状态（每2秒）
            distance = math.sqrt((self.target_x - self.current_x)**2 + 
                               (self.target_y - self.current_y)**2)
            angle_error = abs(self.normalize_angle(self.target_theta - self.current_theta))
            
            waypoint_info = f"[航点 {self.current_waypoint_index + 1}/{len(self.waypoints)}] " if self.waypoints else ""
            rospy.loginfo_throttle(2, 
                f"{waypoint_info}位置: ({self.current_x:.4f}, {self.current_y:.4f}, {self.current_theta:.4f}) "
                f"距离误差: {distance*100:.2f}cm, 角度误差: {math.degrees(angle_error):.2f}°")
            
            # 检查是否完成
            if completed:
                # 如果是多航点模式，尝试切换到下一个航点
                if self.waypoints and self.switch_to_next_waypoint():
                    # 成功切换到下一个航点，继续执行
                    continue
                else:
                    # 所有航点都已完成
                    rospy.loginfo("=" * 60)
                    if self.waypoints:
                        rospy.loginfo(f"✅ 所有 {len(self.waypoints)} 个航点已完成！成功返回初始位置！")
                    else:
                        rospy.loginfo("✅ 成功返回初始位置！")
                    rospy.loginfo(f"最终位置: ({self.current_x:.4f}, {self.current_y:.4f}, {self.current_theta:.4f})")
                    rospy.loginfo(f"最终误差: 位置={distance*100:.2f}cm, 角度={math.degrees(angle_error):.2f}°")
                    rospy.loginfo("=" * 60)
                    break
                
            rate.sleep()
            
        # 停止机器人
        stop_cmd = Twist()
        self.cmd_pub.publish(stop_cmd)
        rospy.loginfo("机器人已停止")

def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(
        description='机器人返回初始位置脚本（支持多航点模式和多机器人并行控制）',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  单机器人模式:
    %(prog)s                           # 默认控制 tb3_0 返回原点
    %(prog)s -n tb3_1                  # tb3_1 机器人返回原点
    %(prog)s -n tb3_0 -x 1.0 -y 0.5    # 返回到指定位置 (1.0, 0.5, 0.0)
  
  多航点模式:
    %(prog)s -w "2.0,2.0,0" "1.0,1.0,0"   # 经过2个中间点返回原点
    %(prog)s -n tb3_1 -w "1.5,1.5,1.57"   # 经过1个中间点返回原点
  
  多机器人并行模式:
    %(prog)s --all                        # 所有机器人(tb3_0到tb3_4)同时返回原点
    %(prog)s --robots tb3_0 tb3_1 tb3_2   # 指定3个机器人同时返回原点
    %(prog)s --robots tb3_0 tb3_1 -w "2.0,2.0,0"  # 多机器人+多航点
  
  注意: 
    - 多航点模式会自动在最后添加原点(0,0,0)
    - 每个航点格式为 "x,y,theta" (逗号分隔，无空格)
    - 多机器人模式下，所有机器人使用相同的航点配置
  
提示: 使用 'rostopic list | grep cmd_vel' 查看可用的机器人命名空间
        """)
    parser.add_argument('--namespace', '-n', type=str, default='tb3_0',
                       help='机器人命名空间 (默认: tb3_0) - 单机器人模式')
    parser.add_argument('--all', action='store_true',
                       help='控制所有机器人(tb3_0到tb3_4)同时返回原点 - 多机器人模式')
    parser.add_argument('--robots', '-r', nargs='+', type=str,
                       help='指定多个机器人命名空间 - 多机器人模式')
    parser.add_argument('--waypoints', '-w', nargs='+', type=str,
                       help='航点列表，格式: "x1,y1,theta1" "x2,y2,theta2" ... (自动添加原点为最后一个航点)')
    parser.add_argument('--target_x', '-x', type=float, default=0.0,
                       help='目标X位置 (默认: 0.0) - 仅单点模式有效')
    parser.add_argument('--target_y', '-y', type=float, default=0.0,
                       help='目标Y位置 (默认: 0.0) - 仅单点模式有效')
    parser.add_argument('--target_theta', '-t', type=float, default=0.0,
                       help='目标角度 (弧度，默认: 0.0) - 仅单点模式有效')
    
    args = parser.parse_args()
    
    # 初始化ROS节点（多机器人模式使用唯一节点名）
    node_name = "robot_return_home_multi" if (args.all or args.robots) else f"robot_return_home_{args.namespace}"
    rospy.init_node(node_name, anonymous=True)
    
    try:
        # 解析航点
        waypoints = None
        if args.waypoints:
            waypoints = []
            for i, wp_str in enumerate(args.waypoints):
                try:
                    parts = wp_str.split(',')
                    if len(parts) != 3:
                        rospy.logerr(f"航点 {i+1} 格式错误: {wp_str} (应为 'x,y,theta')")
                        return
                    x, y, theta = float(parts[0]), float(parts[1]), float(parts[2])
                    waypoints.append((x, y, theta))
                except ValueError as e:
                    rospy.logerr(f"航点 {i+1} 解析错误: {wp_str} - {e}")
                    return
            
            # 自动添加原点作为最后一个航点
            waypoints.append((0.0, 0.0, 0.0))
            rospy.loginfo(f"多航点模式: 已解析 {len(waypoints)-1} 个中间点 + 原点")
        
        # 确定要控制的机器人列表
        robot_namespaces = []
        if args.all:
            robot_namespaces = ['tb3_0', 'tb3_1', 'tb3_2', 'tb3_3', 'tb3_4']
            rospy.loginfo("🤖 多机器人模式: 控制所有5个机器人")
        elif args.robots:
            robot_namespaces = args.robots
            rospy.loginfo(f"🤖 多机器人模式: 控制 {len(robot_namespaces)} 个机器人: {', '.join(robot_namespaces)}")
        else:
            robot_namespaces = [args.namespace]
        
        # 多机器人模式：使用多线程并行控制
        if len(robot_namespaces) > 1:
            rospy.loginfo("=" * 70)
            rospy.loginfo("🚀 开始多机器人并行返航控制")
            rospy.loginfo("=" * 70)
            
            controllers = []
            threads = []
            
            # 为每个机器人创建控制器
            for namespace in robot_namespaces:
                controller = RobotReturnHome(namespace, waypoints=waypoints)
                
                # 单点模式：设置目标位置（仅在没有航点时生效）
                if not waypoints and (args.target_x != 0.0 or args.target_y != 0.0 or args.target_theta != 0.0):
                    controller.target_x = args.target_x
                    controller.target_y = args.target_y 
                    controller.target_theta = args.target_theta
                
                controllers.append(controller)
            
            # 为每个控制器创建线程
            for controller in controllers:
                thread = threading.Thread(target=controller.run, name=f"Thread-{controller.namespace}")
                thread.daemon = True  # 设置为守护线程，主线程结束时自动退出
                threads.append(thread)
            
            # 启动所有线程
            for thread in threads:
                thread.start()
                rospy.sleep(0.1)  # 稍微错开启动时间，避免资源竞争
            
            rospy.loginfo(f"✅ 已启动 {len(threads)} 个控制线程")
            
            # 等待所有线程完成
            for thread in threads:
                thread.join()
            
            rospy.loginfo("=" * 70)
            rospy.loginfo("🎉 所有机器人已完成返航！")
            rospy.loginfo("=" * 70)
            
        else:
            # 单机器人模式
            controller = RobotReturnHome(args.namespace, waypoints=waypoints)
            
            # 单点模式：设置目标位置
            if not waypoints and (args.target_x != 0.0 or args.target_y != 0.0 or args.target_theta != 0.0):
                controller.target_x = args.target_x
                controller.target_y = args.target_y 
                controller.target_theta = args.target_theta
                rospy.loginfo(f"单点模式 - 目标位置已设置为: ({args.target_x}, {args.target_y}, {args.target_theta})")
            
            # 运行控制器
            controller.run()
        
    except rospy.ROSInterruptException:
        rospy.loginfo("程序被中断")
    except Exception as e:
        rospy.logerr(f"程序运行出错: {e}")

if __name__ == '__main__':
    main()
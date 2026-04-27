#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
机器人逆时针旋转90°控制脚本（支持多机器人并行控制）

功能说明：
    - 让机器人在当前位置逆时针旋转90度（π/2弧度）
    - 使用高精度PID控制，角度精度±3°
    - 支持单机器人和多机器人并行控制

使用方法：

1. 单机器人模式：
   python3 robot_rotate_90.py                # 默认控制 tb3_0
   python3 robot_rotate_90.py -n tb3_1       # 控制 tb3_1
   python3 robot_rotate_90.py -n tb3_2       # 控制 tb3_2

2. 多机器人并行模式：
   python3 robot_rotate_90.py --all          # 所有机器人(tb3_0到tb3_4)同时旋转
   python3 robot_rotate_90.py --robots tb3_0 tb3_1 tb3_2  # 指定机器人同时旋转

3. 自定义旋转角度：
   python3 robot_rotate_90.py -a 1.57        # 旋转90度（默认）
   python3 robot_rotate_90.py -a 3.14        # 旋转180度
   python3 robot_rotate_90.py -a -1.57       # 顺时针旋转90度

参数说明：
    -n, --namespace     机器人命名空间（默认：tb3_0）
    --all               控制所有机器人(tb3_0到tb3_4)
    --robots            指定多个机器人命名空间
    -a, --angle         旋转角度（弧度，默认：1.57 = 90度）

常用角度转换：
    90° = 1.57    180° = 3.14    -90° = -1.57    45° = 0.785

作者：分布式控制系统团队
日期：2026-02-07
"""

import rospy
import math
import threading
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
import argparse

class RobotRotate90:
    def __init__(self, namespace="", rotation_angle=math.pi/2):
        """
        初始化机器人旋转控制器
        Args:
            namespace: 机器人命名空间，如 "tb3_0", "tb3_1" 等
            rotation_angle: 旋转角度（弧度），默认π/2（90度）
        """
        self.namespace = namespace
        self.rotation_angle = rotation_angle  # 要旋转的角度
        
        # 当前角度和目标角度
        self.current_theta = None
        self.initial_theta = None  # 初始角度
        self.target_theta = None   # 目标角度
        
        # PID控制参数 - 角度
        self.angular_kp = 1.5   # 比例增益
        self.angular_ki = 0.02  # 积分增益
        self.angular_kd = 0.2   # 微分增益
        
        # PID状态变量
        self.angular_error_integral = 0.0
        self.angular_last_error = 0.0
        self.angular_integral_limit = 0.5  # 积分饱和限制
        
        # 速度限制
        self.max_angular_vel = 0.8   # 最大角速度 (rad/s)
        
        # 到达阈值
        self.angle_threshold = 0.05  # 角度阈值 (rad) - 约3度
        
        # 时间相关
        self.last_time = None
        self.control_rate = 20  # 控制频率 20Hz
        
        # ROS节点和话题设置
        if namespace:
            cmd_topic = f"/{namespace}/cmd_vel"
            odom_topic = f"/{namespace}/odom"
        else:
            cmd_topic = "/cmd_vel"
            odom_topic = "/odom"
            
        # 发布器和订阅器
        self.cmd_pub = rospy.Publisher(cmd_topic, Twist, queue_size=10)
        self.odom_sub = rospy.Subscriber(odom_topic, Odometry, self.odom_callback)
        
        rospy.loginfo(f"机器人旋转控制器启动")
        rospy.loginfo(f"命名空间: {namespace if namespace else '默认'}")
        rospy.loginfo(f"监听话题: {odom_topic}")
        rospy.loginfo(f"发布话题: {cmd_topic}")
        rospy.loginfo(f"旋转角度: {math.degrees(rotation_angle):.1f}° ({rotation_angle:.3f} rad)")
        
    def odom_callback(self, msg):
        """里程计回调函数，更新当前角度"""
        # 获取角度
        orientation = msg.pose.pose.orientation
        _, _, yaw = euler_from_quaternion([
            orientation.x, orientation.y, orientation.z, orientation.w
        ])
        self.current_theta = yaw
        
        # 记录初始角度并计算目标角度（只在第一次执行）
        if self.initial_theta is None and self.current_theta is not None:
            self.initial_theta = self.current_theta
            self.target_theta = self.normalize_angle(self.initial_theta + self.rotation_angle)
            rospy.loginfo(f"初始角度: {math.degrees(self.initial_theta):.2f}° ({self.initial_theta:.3f} rad)")
            rospy.loginfo(f"目标角度: {math.degrees(self.target_theta):.2f}° ({self.target_theta:.3f} rad)")
    
    def normalize_angle(self, angle):
        """将角度规范化到[-pi, pi]"""
        while angle > math.pi:
            angle -= 2.0 * math.pi
        while angle < -math.pi:
            angle += 2.0 * math.pi
        return angle
        
    def calculate_control(self):
        """计算PID控制指令"""
        if self.current_theta is None or self.target_theta is None:
            return Twist(), False
        
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
        
        # 计算角度误差
        angle_error = self.normalize_angle(self.target_theta - self.current_theta)
        
        # 控制逻辑
        cmd = Twist()
        
        # 如果角度误差大于阈值，继续旋转
        if abs(angle_error) > self.angle_threshold:
            # 角度PID控制
            self.angular_error_integral += angle_error * dt
            # 积分限幅
            self.angular_error_integral = max(min(self.angular_error_integral, 
                                                  self.angular_integral_limit), 
                                              -self.angular_integral_limit)
            angular_derivative = (angle_error - self.angular_last_error) / dt
            self.angular_last_error = angle_error
            
            cmd.angular.z = (self.angular_kp * angle_error + 
                           self.angular_ki * self.angular_error_integral + 
                           self.angular_kd * angular_derivative)
            
            # 限制角速度
            cmd.angular.z = max(min(cmd.angular.z, self.max_angular_vel), -self.max_angular_vel)
            
            return cmd, False
        else:
            # 已到达目标角度
            cmd.angular.z = 0.0
            self.reset_pid()
            return cmd, True
    
    def reset_pid(self):
        """重置PID状态"""
        self.angular_error_integral = 0.0
        self.angular_last_error = 0.0
        
    def run(self):
        """运行控制循环"""
        rate = rospy.Rate(self.control_rate)
        
        rospy.loginfo("等待里程计数据...")
        # 等待里程计数据并初始化
        while not rospy.is_shutdown() and (self.current_theta is None or self.target_theta is None):
            rate.sleep()
            
        rospy.loginfo(f"开始旋转（高精度PID控制）...")
        rospy.loginfo(f"当前角度: {math.degrees(self.current_theta):.2f}°")
        rospy.loginfo(f"目标角度: {math.degrees(self.target_theta):.2f}°")
        rospy.loginfo(f"精度目标: 角度±{math.degrees(self.angle_threshold):.1f}°")
        
        start_time = rospy.Time.now()
        timeout = 30.0  # 30秒超时
        
        while not rospy.is_shutdown():
            # 检查超时
            if (rospy.Time.now() - start_time).to_sec() > timeout:
                rospy.logwarn("旋转超时！")
                break
                
            # 计算控制指令
            cmd, completed = self.calculate_control()
            
            # 发布控制指令
            self.cmd_pub.publish(cmd)
            
            # 打印当前状态（每2秒）
            if self.current_theta is not None and self.target_theta is not None:
                angle_error = abs(self.normalize_angle(self.target_theta - self.current_theta))
                rospy.loginfo_throttle(2, 
                    f"当前角度: {math.degrees(self.current_theta):.2f}°, "
                    f"角度误差: {math.degrees(angle_error):.2f}°")
            
            # 检查是否完成
            if completed:
                rospy.loginfo("=" * 60)
                rospy.loginfo(f"✅ 旋转完成！")
                rospy.loginfo(f"最终角度: {math.degrees(self.current_theta):.2f}°")
                rospy.loginfo(f"旋转了: {math.degrees(self.normalize_angle(self.current_theta - self.initial_theta)):.2f}°")
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
        description='机器人旋转控制脚本（支持多机器人并行控制）',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  单机器人模式:
    %(prog)s                           # 默认控制 tb3_0 旋转90度
    %(prog)s -n tb3_1                  # tb3_1 旋转90度
    %(prog)s -n tb3_0 -a 3.14          # tb3_0 旋转180度
    %(prog)s -n tb3_2 -a -1.57         # tb3_2 顺时针旋转90度
  
  多机器人并行模式:
    %(prog)s --all                     # 所有机器人同时旋转90度
    %(prog)s --robots tb3_0 tb3_1      # 两个机器人同时旋转90度
    %(prog)s --all -a 1.57             # 所有机器人同时旋转90度
  
常用角度:
    90度  = 1.57 rad
    180度 = 3.14 rad
    -90度 = -1.57 rad (顺时针)
    45度  = 0.785 rad
        """)
    parser.add_argument('--namespace', '-n', type=str, default='tb3_0',
                       help='机器人命名空间 (默认: tb3_0)')
    parser.add_argument('--all', action='store_true',
                       help='控制所有机器人(tb3_0到tb3_4)同时旋转')
    parser.add_argument('--robots', '-r', nargs='+', type=str,
                       help='指定多个机器人命名空间')
    parser.add_argument('--angle', '-a', type=float, default=math.pi/2,
                       help='旋转角度（弧度，默认: 1.57 = 90度）')
    
    args = parser.parse_args()
    
    # 初始化ROS节点
    node_name = "robot_rotate_90_multi" if (args.all or args.robots) else f"robot_rotate_90_{args.namespace}"
    rospy.init_node(node_name, anonymous=True)
    
    try:
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
            rospy.loginfo(f"🚀 开始多机器人并行旋转控制 (旋转 {math.degrees(args.angle):.1f}°)")
            rospy.loginfo("=" * 70)
            
            controllers = []
            threads = []
            
            # 为每个机器人创建控制器
            for namespace in robot_namespaces:
                controller = RobotRotate90(namespace, rotation_angle=args.angle)
                controllers.append(controller)
            
            # 为每个控制器创建线程
            for controller in controllers:
                thread = threading.Thread(target=controller.run, name=f"Thread-{controller.namespace}")
                thread.daemon = True
                threads.append(thread)
            
            # 启动所有线程
            for thread in threads:
                thread.start()
                rospy.sleep(0.1)
            
            rospy.loginfo(f"✅ 已启动 {len(threads)} 个控制线程")
            
            # 等待所有线程完成
            for thread in threads:
                thread.join()
            
            rospy.loginfo("=" * 70)
            rospy.loginfo("🎉 所有机器人已完成旋转！")
            rospy.loginfo("=" * 70)
            
        else:
            # 单机器人模式
            controller = RobotRotate90(args.namespace, rotation_angle=args.angle)
            controller.run()
        
    except rospy.ROSInterruptException:
        rospy.loginfo("程序被中断")
    except Exception as e:
        rospy.logerr(f"程序运行出错: {e}")

if __name__ == '__main__':
    main()

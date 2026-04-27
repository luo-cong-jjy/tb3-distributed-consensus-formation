#!/usr/bin/env python3
"""
激光雷达测试脚本
基于tb3_controller_node.py的激光雷达处理逻辑
用于测试任意机器人的激光雷达是否工作正常

使用方法:
python3 laser_test.py --robot_id 0  # 测试tb3_0的激光雷达
python3 laser_test.py --topic /tb3_1/scan  # 直接指定激光雷达话题
python3 laser_test.py --help  # 查看帮助信息
"""

import rospy
import math
import numpy as np
import argparse
import sys
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
import tf
from datetime import datetime

class LaserTester:
    def __init__(self, laser_topic="/tb3_0/scan", odom_topic="/tb3_0/odom", robot_id=0):
        """
        初始化激光雷达测试器
        
        Args:
            laser_topic: 激光雷达话题名称
            odom_topic: 里程计话题名称（用于获取机器人位姿）
            robot_id: 机器人ID（用于显示）
        """
        rospy.init_node(f'laser_tester_{robot_id}', anonymous=True)
        
        self.robot_id = robot_id
        self.laser_topic = laser_topic
        self.odom_topic = odom_topic
        
        # 机器人当前位姿
        self.xc = 0.0
        self.yc = 0.0
        self.thetac = 0.0
        
        # 激光雷达数据
        self.laser_data = None
        self.laser_update_time = 0.0
        self.laser_callback_count = 0
        self.last_callback_time = 0.0
        
        # 障碍物数据
        self.xobs = []
        self.yobs = []
        self.n_o = 0
        self.dobsmin = float('inf')
        self.min_obs_num = -1
        
        # 统计数据
        self.start_time = rospy.get_time()
        self.total_points = 0
        self.min_distance_history = []
        
        # 检测参数（与控制脚本保持一致）
        self.obstacle_detection_range = 2.0  # 障碍物检测最大距离（米）
        
        # 输出控制
        self.output_interval = 1.0  # 输出间隔（秒）
        self.last_output_time = 0.0
        
        print(f"========== 激光雷达测试器 ==========")
        print(f"机器人ID: {self.robot_id}")
        print(f"激光雷达话题: {self.laser_topic}")
        print(f"里程计话题: {self.odom_topic}")
        print(f"检测范围: {self.obstacle_detection_range}m")
        print(f"输出间隔: {self.output_interval}s")
        print("=" * 40)
        
        # 订阅激光雷达和里程计数据
        try:
            rospy.Subscriber(self.laser_topic, LaserScan, self.laser_callback)
            rospy.Subscriber(self.odom_topic, Odometry, self.odom_callback)
            print(f"✅ 成功订阅话题")
        except Exception as e:
            print(f"❌ 订阅话题失败: {e}")
            sys.exit(1)
        
        # 定时输出统计信息
        self.timer = rospy.Timer(rospy.Duration(self.output_interval), self.output_statistics)
        
        print("开始监听激光雷达数据... (按Ctrl+C退出)")
        
    def odom_callback(self, msg):
        """更新机器人位姿"""
        self.xc = msg.pose.pose.position.x
        self.yc = msg.pose.pose.position.y
        # 四元数转航向角
        q = [msg.pose.pose.orientation.x, msg.pose.pose.orientation.y,
             msg.pose.pose.orientation.z, msg.pose.pose.orientation.w]
        self.thetac = tf.transformations.euler_from_quaternion(q)[2]
        
    def laser_callback(self, msg):
        """
        处理激光雷达数据，计算障碍物信息
        基于tb3_controller_node.py的laser_callback逻辑
        """
        current_time = rospy.get_time()
        
        # 更新回调统计
        self.laser_callback_count += 1
        if self.last_callback_time > 0:
            callback_interval = current_time - self.last_callback_time
        else:
            callback_interval = 0.0
        self.last_callback_time = current_time
        
        # 存储激光雷达数据
        self.laser_data = msg
        self.laser_update_time = current_time
        
        # 重置障碍物列表
        self.xobs = []
        self.yobs = []
        self.raw_distances = []  # 🔥 新增：保存原始距离数据
        
        # 激光雷达参数
        angle_min = msg.angle_min
        angle_increment = msg.angle_increment
        range_min = msg.range_min
        range_max = msg.range_max
        
        # 处理激光雷达扫描数据
        valid_points = 0
        for i, range_value in enumerate(msg.ranges):
            # 🔥 修改：根据TurtleBot3激光雷达规格设置阈值
            # LDS-01: 最小检测距离0.12m, LDS-02: 最小检测距离0.16m  
            # 使用0.10m作为通用阈值，兼容两种雷达并排除无效测量
            if (range_value > 0.10 and  # 兼容LDS-01(0.12m)和LDS-02(0.16m)的最小检测距离
                range_value <= min(range_max, self.obstacle_detection_range) and
                not math.isinf(range_value) and  # 排除无穷大值
                not math.isnan(range_value)):    # 排除NaN值
                valid_points += 1
                
                # 🔥 保存原始距离数据（这才是真实的激光雷达距离）
                self.raw_distances.append(range_value)
                
                # 计算扫描点角度
                angle = angle_min + i * angle_increment
                
                # 转换为机器人本体坐标系
                x_local = range_value * math.cos(angle)
                y_local = range_value * math.sin(angle)
                
                # 转换为全局坐标系（保留用于可视化，但不用于距离计算）
                cos_theta = math.cos(self.thetac)
                sin_theta = math.sin(self.thetac)
                
                x_global = self.xc + (cos_theta * x_local - sin_theta * y_local)
                y_global = self.yc + (sin_theta * x_local + cos_theta * y_local)
                
                # 添加到障碍物列表
                self.xobs.append(x_global)
                self.yobs.append(y_global)
        
        # 转换为numpy数组
        self.xobs = np.array(self.xobs)
        self.yobs = np.array(self.yobs)
        self.raw_distances = np.array(self.raw_distances)  # 🔥 转换原始距离为numpy数组
        self.n_o = len(self.xobs)
        self.total_points += self.n_o
        
        # 计算最近障碍物距离
        self.calculate_obstacle_distances()
        
        # 记录最近距离历史
        if self.dobsmin != float('inf'):
            self.min_distance_history.append(self.dobsmin)
            # 只保留最近100个数据点
            if len(self.min_distance_history) > 100:
                self.min_distance_history.pop(0)
        
        # 简化调试输出（仅前3次回调）
        if self.laser_callback_count <= 3:
            if len(self.raw_distances) > 0:
                print(f"[回调#{self.laser_callback_count:2d}] "
                      f"检测点数: {self.n_o:3d}, "
                      f"激光距离: {self.dobsmin:.3f}m")
                
                # 显示全局坐标距离对比
                if hasattr(self, 'dobsmin_global'):
                    print(f"  全局距离: {self.dobsmin_global:.3f}m, "
                          f"障碍物坐标: ({self.min_obs_global_x:.3f}, {self.min_obs_global_y:.3f})")
            else:
                print(f"[回调#{self.laser_callback_count:2d}] "
                      f"检测点数: {self.n_o:3d}, "
                      f"激光距离: {self.dobsmin:.3f}m")
    
    def calculate_obstacle_distances(self):
        """
        计算到障碍物的距离
        提供两种计算方法：
        1. 原始激光距离（最准确）
        2. 全局坐标距离（与控制脚本一致）
        """
        if not hasattr(self, 'raw_distances') or len(self.raw_distances) == 0:
            self.dobsmin = float('inf')  
            self.dobsmin_global = float('inf')
            self.min_obs_num = -1
            return
        
        # 方法1：🔥 使用激光雷达原始距离数据（最准确）
        valid_distances = self.raw_distances[self.raw_distances > 0.0]
        
        if len(valid_distances) == 0:
            self.dobsmin = float('inf')
            self.dobsmin_global = float('inf')
            self.min_obs_num = -1
            return
        
        # 找到最近的有效障碍物（激光雷达原始距离）
        min_valid_distance = np.min(valid_distances)
        self.min_obs_num = np.where(self.raw_distances == min_valid_distance)[0][0]
        self.dobsmin = min_valid_distance
        
        # 方法2：🆕 使用全局坐标计算距离（与控制脚本一致）
        if len(self.xobs) > 0 and len(self.yobs) > 0:
            # 创建距离数组（模拟控制脚本的计算方法）
            dobs_global = np.zeros(self.n_o)
            
            for j in range(self.n_o):
                # 🔥 使用机器人当前位置计算到障碍物的距离
                # 注意：控制脚本使用参考轨迹位置(xr,yr)，这里用实际位置(xc,yc)演示
                dx = self.xc - self.xobs[j]  # 机器人当前x - 障碍物x
                dy = self.yc - self.yobs[j]  # 机器人当前y - 障碍物y
                dobs_global[j] = np.sqrt(dx**2 + dy**2)  # 欧几里得距离
            
            # 找到最近的障碍物（全局坐标方法）
            min_global_idx = np.argmin(dobs_global)
            self.dobsmin_global = dobs_global[min_global_idx]
            self.min_obs_global_x = self.xobs[min_global_idx] 
            self.min_obs_global_y = self.yobs[min_global_idx]
        else:
            self.dobsmin_global = float('inf')
            self.min_obs_global_x = 0.0
            self.min_obs_global_y = 0.0
    
    def output_statistics(self, event):
        """定时输出统计信息"""
        current_time = rospy.get_time()
        elapsed_time = current_time - self.start_time
        
        if elapsed_time == 0:
            return
        
        # 计算统计数据
        avg_callback_freq = self.laser_callback_count / elapsed_time if elapsed_time > 0 else 0
        avg_points_per_scan = self.total_points / max(self.laser_callback_count, 1)
        
        # 距离统计
        if self.min_distance_history:
            min_dist = min(self.min_distance_history)
            max_dist = max(self.min_distance_history)
            avg_dist = sum(self.min_distance_history) / len(self.min_distance_history)
        else:
            min_dist = max_dist = avg_dist = 0.0
        
        # 获取当前时间戳
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        print(f"\n[{timestamp}] ========== 激光雷达状态报告 ==========")
        print(f"机器人位置: ({self.xc:.3f}, {self.yc:.3f}, {math.degrees(self.thetac):.1f}°)")
        print(f"运行时间: {elapsed_time:.1f}s")
        print(f"激光回调: {self.laser_callback_count} 次 (频率: {avg_callback_freq:.1f} Hz)")
        print(f"当前检测: {self.n_o} 个障碍点")
        print(f"平均点数: {avg_points_per_scan:.1f} 点/帧")
        print(f"当前最近距离: {self.dobsmin:.3f}m (激光雷达)")
        if hasattr(self, 'dobsmin_global'):
            print(f"全局坐标距离: {self.dobsmin_global:.3f}m (与控制脚本一致)")
            if hasattr(self, 'min_obs_global_x'):
                print(f"最近障碍物全局坐标: ({self.min_obs_global_x:.3f}, {self.min_obs_global_y:.3f})")
        if self.min_distance_history:
            print(f"距离统计: 最小={min_dist:.3f}m, 最大={max_dist:.3f}m, 平均={avg_dist:.3f}m")
        
        # 激光雷达数据健康检查
        if self.laser_data:
            print(f"激光参数: 角度范围=[{math.degrees(self.laser_data.angle_min):.1f}°, "
                  f"{math.degrees(self.laser_data.angle_max):.1f}°], "
                  f"分辨率={math.degrees(self.laser_data.angle_increment):.2f}°, "
                  f"距离范围=[{self.laser_data.range_min:.2f}, {self.laser_data.range_max:.2f}]m")
            
            # 检查数据质量
            if avg_callback_freq < 5:
                print("⚠️  警告: 激光雷达回调频率较低，可能存在问题")
            elif avg_callback_freq > 30:
                print("⚠️  警告: 激光雷达回调频率过高，可能影响性能")
            else:
                print("✅ 激光雷达工作正常")
        else:
            print("❌ 错误: 未收到激光雷达数据")
        
        print("=" * 50)
    
    def run(self):
        """运行测试器"""
        try:
            rospy.spin()
        except KeyboardInterrupt:
            print("\n收到中断信号，正在关闭...")
        except Exception as e:
            print(f"运行时错误: {e}")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """清理资源"""
        elapsed_time = rospy.get_time() - self.start_time
        print(f"\n========== 测试总结 ==========")
        print(f"总运行时间: {elapsed_time:.1f}s")
        print(f"总激光回调: {self.laser_callback_count} 次")
        print(f"平均回调频率: {self.laser_callback_count/max(elapsed_time, 1):.1f} Hz")
        print(f"总检测点数: {self.total_points}")
        if self.min_distance_history:
            print(f"最近距离: 最小={min(self.min_distance_history):.3f}m, "
                  f"最大={max(self.min_distance_history):.3f}m")
        print("测试完成！")

def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='TurtleBot3 激光雷达测试工具')
    
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--robot_id', type=int, default=0,
                       help='机器人ID (0-4)，将自动生成话题名称 (默认: 0)')
    group.add_argument('--topic', type=str,
                       help='直接指定激光雷达话题名称，例如: /tb3_1/scan')
    
    parser.add_argument('--odom_topic', type=str,
                        help='里程计话题名称（可选，将根据激光话题自动推断）')
    parser.add_argument('--range', type=float, default=2.0,
                        help='障碍物检测最大距离（米） (默认: 2.0)')
    parser.add_argument('--interval', type=float, default=1.0,
                        help='统计信息输出间隔（秒） (默认: 1.0)')
    
    return parser.parse_args()

def main():
    """主函数"""
    args = parse_arguments()
    
    # 确定激光雷达话题
    if args.topic:
        laser_topic = args.topic
        # 从激光话题推断机器人ID
        if '/tb3_' in laser_topic:
            robot_id = int(laser_topic.split('/tb3_')[1].split('/')[0])
        else:
            robot_id = 0
    else:
        robot_id = args.robot_id
        laser_topic = f"/tb3_{robot_id}/scan"
    
    # 确定里程计话题
    if args.odom_topic:
        odom_topic = args.odom_topic
    else:
        odom_topic = f"/tb3_{robot_id}/odom"
    
    print(f"激光雷达测试器启动参数:")
    print(f"  机器人ID: {robot_id}")
    print(f"  激光话题: {laser_topic}")
    print(f"  里程话题: {odom_topic}")
    print(f"  检测范围: {args.range}m")
    print(f"  输出间隔: {args.interval}s")
    print()
    
    try:
        # 创建并运行测试器
        tester = LaserTester(
            laser_topic=laser_topic,
            odom_topic=odom_topic,
            robot_id=robot_id
        )
        tester.obstacle_detection_range = args.range
        tester.output_interval = args.interval
        tester.timer.shutdown()  # 关闭旧定时器
        tester.timer = rospy.Timer(rospy.Duration(args.interval), tester.output_statistics)
        
        tester.run()
        
    except rospy.ROSException as e:
        print(f"ROS错误: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"未知错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
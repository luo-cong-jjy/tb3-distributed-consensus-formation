#!/usr/bin/env python3
"""
简单的激光雷达原始数据查看器
直接显示激光雷达scan消息的原始内容
"""

import rospy
import numpy as np
from sensor_msgs.msg import LaserScan

def laser_debug_callback(msg):
    """显示激光雷达原始数据的详细信息"""
    print(f"\n========== 激光雷达原始数据 ==========")
    print(f"消息时间戳: {msg.header.stamp}")
    print(f"角度范围: [{np.degrees(msg.angle_min):.1f}°, {np.degrees(msg.angle_max):.1f}°]")
    print(f"角度增量: {np.degrees(msg.angle_increment):.3f}°")
    print(f"距离范围: [{msg.range_min:.3f}, {msg.range_max:.3f}]m")
    print(f"总扫描点数: {len(msg.ranges)}")
    
    # 统计距离值
    ranges = np.array(msg.ranges)
    valid_ranges = ranges[(ranges > 0.05) & (ranges < msg.range_max) & np.isfinite(ranges)]
    zero_count = np.sum(ranges == 0.0)
    inf_count = np.sum(np.isinf(ranges))
    nan_count = np.sum(np.isnan(ranges))
    
    print(f"零值数量: {zero_count}")
    print(f"无穷大值数量: {inf_count}")
    print(f"NaN值数量: {nan_count}")
    print(f"有效值数量: {len(valid_ranges)}")
    
    if len(valid_ranges) > 0:
        print(f"有效距离统计:")
        print(f"  最小值: {np.min(valid_ranges):.3f}m")
        print(f"  最大值: {np.max(valid_ranges):.3f}m")
        print(f"  平均值: {np.mean(valid_ranges):.3f}m")
        print(f"  中位数: {np.median(valid_ranges):.3f}m")
        
        # 显示一些样本数据
        print(f"前20个原始距离值:")
        sample_ranges = ranges[:20]
        print(f"  {[f'{r:.3f}' for r in sample_ranges]}")
        
        # 显示一些有效距离值
        print(f"前10个有效距离值:")
        sample_valid = valid_ranges[:10]
        print(f"  {[f'{r:.3f}' for r in sample_valid]}")
    
    print("=" * 50)

def main():
    rospy.init_node('laser_debug_viewer', anonymous=True)
    
    # 订阅激光雷达数据
    topic = "/tb3_0/scan"  # 可以根据需要修改
    print(f"订阅激光雷达话题: {topic}")
    print("等待激光雷达数据... (按Ctrl+C退出)")
    
    rospy.Subscriber(topic, LaserScan, laser_debug_callback)
    
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("\n程序退出")

if __name__ == "__main__":
    main()
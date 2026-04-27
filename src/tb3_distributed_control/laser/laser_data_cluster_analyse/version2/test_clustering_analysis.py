#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
聚类分析测试脚本 - 独立测试雷达聚类功能

功能：
1. 订阅任意机器人的雷达数据
2. 执行连续性聚类分析
3. 实时输出聚类统计信息
4. 可视化聚类结果（可选）

使用方法：
    rosrun tb3_distributed_control test_clustering_analysis.py

测试场景：
    启动仿真后运行此脚本，观察聚类结果是否合理
"""

import rospy
import numpy as np
import math
import time
from collections import defaultdict
from sensor_msgs.msg import LaserScan
from visualization_msgs.msg import Marker, MarkerArray
from geometry_msgs.msg import Point
import matplotlib.pyplot as plt


class ClusteringAnalysisTester:
    def __init__(self):
        rospy.init_node('clustering_analysis_tester', anonymous=True)
        
        # 获取测试参数
        self.robot_id = rospy.get_param('~robot_id', 0)  # 默认测试tb3_0
        self.visualize = rospy.get_param('~visualize', True)  # 是否发布可视化
        self.verbose = rospy.get_param('~verbose', False)  # 是否详细输出（默认关闭以提升性能）
        
        # 雷达参数（与控制节点保持一致）
        self.min_detection_range = 0.12
        self.max_detection_range = 3
        self.min_cluster_length = 0.001  # 5cm长度过滤阈值
        self.min_cluster_points = 1      # 单点噪声过滤阈值
        
        # 统计信息
        self.scan_count = 0
        self.cluster_stats = {
            'total_scans': 0,
            'avg_clusters': 0,
            'max_clusters': 0,
            'min_clusters': float('inf')
        }
        
        # 性能分析
        self.performance_stats = {
            'extract_valid': [],
            'clustering': [],
            'merge_wraparound': [],
            'filter_points': [],
            'filter_length': [],
            'logging': [],
            'visualization': [],
            'total_callback': []
        }
        self.performance_interval = rospy.get_param('~performance_interval', 50)  # 每N次扫描输出一次性能报告
        
        # 聚类结果记录（用于周期性摘要输出）
        self.recent_cluster_results = []  # 存储最近的聚类结果
        
        # ROS通信
        rospy.Subscriber(f"/tb3_{self.robot_id}/scan", LaserScan, self.laser_callback)
        
        if self.visualize:
            self.cluster_pub = rospy.Publisher(
                '/test_clustering/clusters', 
                MarkerArray, 
                queue_size=1
            )
        
        rospy.loginfo(f"🧪 聚类分析测试器已启动")
        rospy.loginfo(f"   测试机器人: tb3_{self.robot_id}")
        rospy.loginfo(f"   可视化: {'开启' if self.visualize else '关闭'}")
        rospy.loginfo(f"   详细输出: {'开启' if self.verbose else '关闭'} (⚠️ 详细日志会严重影响性能)")
        rospy.loginfo(f"   参数: min_range={self.min_detection_range}m, "
                     f"max_range={self.max_detection_range}m, "
                     f"min_length={self.min_cluster_length}m")

    def laser_callback(self, msg):
        """雷达数据回调 - 执行聚类分析"""
        t_callback_start = time.time()
        self.scan_count += 1
        
        # 1. 基于连续性分区
        t1 = time.time()
        clusters = self.cluster_by_continuity(msg)
        t2 = time.time()
        self.performance_stats['clustering'].append(t2 - t1)
        
        if len(clusters) == 0:
            if self.verbose:
                rospy.loginfo(f"[扫描 {self.scan_count}] 无有效分区")
            return
        
        # 2. 360°跨越处理
        t3 = time.time()
        clusters = self.merge_wraparound_clusters(clusters)
        t4 = time.time()
        self.performance_stats['merge_wraparound'].append(t4 - t3)
        
        # 3. 单点噪声过滤
        t5 = time.time()
        filtered_clusters = [c for c in clusters if len(c) >= self.min_cluster_points]
        t6 = time.time()
        self.performance_stats['filter_points'].append(t6 - t5)
        
        # 4. 长度过滤
        t7 = time.time()
        cluster_lengths = self.calculate_all_cluster_lengths(filtered_clusters)
        valid_clusters = []
        for i, cluster in enumerate(filtered_clusters):
            if cluster_lengths[i] >= self.min_cluster_length:
                valid_clusters.append(cluster)
        t8 = time.time()
        self.performance_stats['filter_length'].append(t8 - t7)
        
        # 5. 统计信息
        n_clusters = len(valid_clusters)
        self.update_statistics(n_clusters)
        
        # 记录聚类结果用于周期性输出
        cluster_info = {
            'scan_id': self.scan_count,
            'raw_clusters': len(clusters),
            'filtered_clusters': len(filtered_clusters),
            'valid_clusters': n_clusters,
            'cluster_details': [(len(c), cluster_lengths[i]) for i, c in enumerate(valid_clusters)]
        }
        self.recent_cluster_results.append(cluster_info)
        
        # 只保留最近的performance_interval条记录
        if len(self.recent_cluster_results) > self.performance_interval:
            self.recent_cluster_results.pop(0)
        
        # 6. 输出结果
        t_log_start = time.time()
        if self.verbose:
            rospy.loginfo(f"[扫描 {self.scan_count}] "
                         f"原始分区:{len(clusters)}, "
                         f"点数过滤后:{len(filtered_clusters)}, "
                         f"长度过滤后:{n_clusters}")
            
            # 输出每个聚类的详细信息
            for i, (cluster, length) in enumerate(zip(valid_clusters, 
                                                       [cluster_lengths[j] for j in range(len(cluster_lengths)) 
                                                        if cluster_lengths[j] >= self.min_cluster_length])):
                rospy.loginfo(f"  聚类{i}: 点数={len(cluster)}, 长度={length:.3f}m")
        t_log_end = time.time()
        self.performance_stats['logging'].append(t_log_end - t_log_start)
        
        # 7. 可视化（如果启用）
        if self.visualize:
            t9 = time.time()
            self.visualize_clusters(valid_clusters, msg.header)
            t10 = time.time()
            self.performance_stats['visualization'].append(t10 - t9)
        
        # 记录总耗时
        t_callback_end = time.time()
        self.performance_stats['total_callback'].append(t_callback_end - t_callback_start)
        
        # 定期输出性能报告
        if self.scan_count % self.performance_interval == 0:
            self.print_performance_report()

    def extract_valid_points(self, msg):
        """提取有效激光点（NumPy优化版）"""
        t_start = time.time()
        ranges = np.array(msg.ranges)
        n_points = len(ranges)
        
        indices = np.arange(n_points)
        angles = msg.angle_min + indices * msg.angle_increment
        
        min_range = max(msg.range_min, self.min_detection_range)
        max_range = min(msg.range_max, self.max_detection_range)
        
        valid_mask = (
            ~np.isnan(ranges) &
            ~np.isinf(ranges) &
            (ranges != 0.0) &
            (ranges >= min_range) &
            (ranges <= max_range)
        )
        
        valid_indices = indices[valid_mask]
        valid_angles = angles[valid_mask]
        valid_ranges = ranges[valid_mask]
        
        # 向量化计算笛卡尔坐标
        x = valid_ranges * np.cos(valid_angles)
        y = valid_ranges * np.sin(valid_angles)
        
        # 返回结构化数组（更高效）
        valid_points = np.empty(len(valid_indices), dtype=[
            ('index', 'i4'),
            ('angle', 'f8'),
            ('range', 'f8'),
            ('x', 'f8'),
            ('y', 'f8')
        ])
        valid_points['index'] = valid_indices
        valid_points['angle'] = valid_angles
        valid_points['range'] = valid_ranges
        valid_points['x'] = x
        valid_points['y'] = y
        
        t_end = time.time()
        self.performance_stats['extract_valid'].append(t_end - t_start)
        
        return valid_points

    def cluster_by_continuity(self, laser_data):
        """
        基于雷达数据连续性进行分区（NumPy优化版）
        
        分区条件：
        1. 索引不连续（有无效点）
        2. 🔥 距离跳变（相邻点距离差 > 阈值）
        """
        valid_points = self.extract_valid_points(laser_data)
        
        if len(valid_points) == 0:
            return []
        
        # 1. 找到索引断点（不连续的位置）
        indices = valid_points['index']
        index_breaks = np.where(np.diff(indices) != 1)[0] + 1
        
        # 2. 🔥 找到距离跳变点（相邻点距离差过大）
        ranges = valid_points['range']
        range_diffs = np.abs(np.diff(ranges))
        
        # 距离跳变阈值：相邻点距离差 > 6.8cm 就分区
        distance_jump_threshold = 0.068
        distance_breaks = np.where(range_diffs > distance_jump_threshold)[0] + 1
        
        # 3. 合并两种断点
        all_breaks = np.unique(np.concatenate([index_breaks, distance_breaks]))
        
        # 4. 使用np.split快速分割
        clusters = np.split(valid_points, all_breaks)
        
        return clusters

    def merge_wraparound_clusters(self, clusters):
        """处理360°跨越问题（NumPy优化版）"""
        if len(clusters) < 2:
            return clusters
        
        first_cluster = clusters[0]
        last_cluster = clusters[-1]
        
        if len(first_cluster) == 0 or len(last_cluster) == 0:
            return clusters
        
        first_angle = first_cluster[0]['angle']
        last_angle = last_cluster[-1]['angle']
        
        first_near_zero = -0.2 <= first_angle <= 0.5
        last_near_360 = 5.8 <= last_angle <= 6.5
        
        if not (first_near_zero and last_near_360):
            return clusters
        
        # 向量化计算距离
        dx = first_cluster[0]['x'] - last_cluster[-1]['x']
        dy = first_cluster[0]['y'] - last_cluster[-1]['y']
        spatial_distance = np.sqrt(dx**2 + dy**2)
        
        merge_threshold = 0.15
        
        if spatial_distance < merge_threshold:
            merged_cluster = np.concatenate([last_cluster, first_cluster])
            return [merged_cluster] + clusters[1:-1]
        
        return clusters

    def calculate_all_cluster_lengths(self, clusters):
        """计算所有分区的长度（NumPy优化版）"""
        if not clusters:
            return np.array([])
        
        lengths = np.zeros(len(clusters))
        
        for i, cluster in enumerate(clusters):
            if len(cluster) < 2:
                continue
            
            r1 = cluster[0]['range']
            r2 = cluster[-1]['range']
            angle1 = cluster[0]['angle']
            angle2 = cluster[-1]['angle']
            
            # 处理角度跨越
            angle_diff = angle2 - angle1
            if angle_diff < 0:
                angle_diff += 2 * np.pi
            
            # 余弦定理计算长度
            length_squared = r1**2 + r2**2 - 2*r1*r2*np.cos(angle_diff)
            lengths[i] = np.sqrt(max(length_squared, 0))
        
        return lengths

    def update_statistics(self, n_clusters):
        """更新统计信息"""
        self.cluster_stats['total_scans'] += 1
        self.cluster_stats['max_clusters'] = max(self.cluster_stats['max_clusters'], n_clusters)
        self.cluster_stats['min_clusters'] = min(self.cluster_stats['min_clusters'], n_clusters)
        
        # 滚动平均
        alpha = 0.1  # 平滑因子
        if self.cluster_stats['avg_clusters'] == 0:
            self.cluster_stats['avg_clusters'] = n_clusters
        else:
            self.cluster_stats['avg_clusters'] = (
                alpha * n_clusters + (1 - alpha) * self.cluster_stats['avg_clusters']
            )

    def visualize_clusters(self, clusters, header):
        """发布聚类可视化标记"""
        marker_array = MarkerArray()
        
        # 为每个聚类创建一个标记
        for cluster_id, cluster in enumerate(clusters):
            marker = Marker()
            marker.header = header
            marker.header.frame_id = f"tb3_{self.robot_id}/base_scan"
            marker.ns = "clusters"
            marker.id = cluster_id
            marker.type = Marker.LINE_STRIP
            marker.action = Marker.ADD
            
            # 设置颜色（根据聚类ID循环）
            colors = [
                (1.0, 0.0, 0.0),  # 红
                (0.0, 1.0, 0.0),  # 绿
                (0.0, 0.0, 1.0),  # 蓝
                (1.0, 1.0, 0.0),  # 黄
                (1.0, 0.0, 1.0),  # 紫
                (0.0, 1.0, 1.0),  # 青
            ]
            color = colors[cluster_id % len(colors)]
            marker.color.r = color[0]
            marker.color.g = color[1]
            marker.color.b = color[2]
            marker.color.a = 0.8
            
            marker.scale.x = 0.02  # 线宽
            
            # 添加点
            for point in cluster:
                p = Point()
                p.x = point['x']
                p.y = point['y']
                p.z = 0.0
                marker.points.append(p)
            
            marker_array.markers.append(marker)
        
        # 删除多余的旧标记
        for i in range(len(clusters), 50):
            marker = Marker()
            marker.header = header
            marker.header.frame_id = f"tb3_{self.robot_id}/base_scan"
            marker.ns = "clusters"
            marker.id = i
            marker.action = Marker.DELETE
            marker_array.markers.append(marker)
        
        self.cluster_pub.publish(marker_array)

    def print_performance_report(self):
        """打印性能分析报告"""
        rospy.loginfo("=" * 60)
        rospy.loginfo(f"⚡ 性能分析与聚类报告 (基于 {self.scan_count} 次扫描)")
        rospy.loginfo("=" * 60)
        
        # 先输出聚类结果统计
        self.print_cluster_summary()
        
        # 计算各步骤统计信息和总和
        total_sum = 0.0
        step_times = {}
        
        for step_name, times in self.performance_stats.items():
            if len(times) == 0 or step_name == 'total_callback':
                continue
            
            avg_time = np.mean(times) * 1000  # 转换为毫秒
            max_time = np.max(times) * 1000
            min_time = np.min(times) * 1000
            std_time = np.std(times) * 1000
            
            step_times[step_name] = avg_time
            total_sum += avg_time
            
            rospy.loginfo(f"{step_name:20s}: "
                         f"平均={avg_time:6.3f}ms, "
                         f"最大={max_time:6.3f}ms, "
                         f"最小={min_time:6.3f}ms, "
                         f"标准差={std_time:6.3f}ms")
        
        # 计算总耗时和未统计部分
        if len(self.performance_stats['total_callback']) > 0:
            total_avg = np.mean(self.performance_stats['total_callback']) * 1000
            unaccounted = total_avg - total_sum
            
            rospy.loginfo("-" * 60)
            rospy.loginfo(f"{'各部分时间总和':20s}: {total_sum:6.3f}ms")
            rospy.loginfo(f"{'总回调耗时':20s}: {total_avg:6.3f}ms")
            rospy.loginfo(f"{'未统计部分':20s}: {unaccounted:6.3f}ms ({unaccounted/total_avg*100:.1f}%)")
            
            # 计算各步骤占比
            rospy.loginfo("-" * 60)
            rospy.loginfo("时间占比分析:")
            for step_name in ['extract_valid', 'clustering', 'merge_wraparound', 
                             'filter_points', 'filter_length', 'logging', 'visualization']:
                if step_name in step_times:
                    percentage = (step_times[step_name] / total_avg) * 100
                    rospy.loginfo(f"  {step_name:18s}: {percentage:5.1f}%")
            
            rospy.loginfo("-" * 60)
            # 计算纯聚类分析耗时（排除可视化）
            pure_clustering_time = total_avg - step_times.get('visualization', 0.0)
            rospy.loginfo(f"{'纯聚类分析耗时':20s}: {pure_clustering_time:6.3f}ms")
            
            # 雷达频率分析（假设10Hz标准频率）
            expected_period = 100  # ms
            if total_avg < expected_period:
                utilization = (total_avg / expected_period) * 100
                rospy.loginfo(f"{'CPU利用率':20s}: {utilization:6.2f}% (10Hz基准)")
            else:
                rospy.logwarn(f"⚠️  回调耗时超过100ms，可能无法满足实时性要求！")
        
        rospy.loginfo("=" * 60)
    
    def print_cluster_summary(self):
        """打印最近一段时间的聚类结果摘要"""
        if len(self.recent_cluster_results) == 0:
            return
        
        rospy.loginfo("📊 聚类结果统计 (最近{0}次扫描)".format(len(self.recent_cluster_results)))
        rospy.loginfo("-" * 60)
        
        # 统计聚类数量分布
        raw_clusters = [r['raw_clusters'] for r in self.recent_cluster_results]
        filtered_clusters = [r['filtered_clusters'] for r in self.recent_cluster_results]
        valid_clusters = [r['valid_clusters'] for r in self.recent_cluster_results]
        
        rospy.loginfo(f"{'原始聚类数':20s}: 平均={np.mean(raw_clusters):.1f}, "
                     f"最大={max(raw_clusters)}, 最小={min(raw_clusters)}")
        rospy.loginfo(f"{'点数过滤后':20s}: 平均={np.mean(filtered_clusters):.1f}, "
                     f"最大={max(filtered_clusters)}, 最小={min(filtered_clusters)}")
        rospy.loginfo(f"{'长度过滤后':20s}: 平均={np.mean(valid_clusters):.1f}, "
                     f"最大={max(valid_clusters)}, 最小={min(valid_clusters)}")
        
        # 输出最后一次扫描的详细信息
        last_result = self.recent_cluster_results[-1]
        if last_result['valid_clusters'] > 0:
            rospy.loginfo("-" * 60)
            rospy.loginfo(f"[最新扫描 {last_result['scan_id']}] 聚类详情:")
            for i, (points, length) in enumerate(last_result['cluster_details']):
                rospy.loginfo(f"  聚类{i}: 点数={points}, 长度={length:.3f}m")
        
        rospy.loginfo("-" * 60)
    
    def print_summary(self):
        """打印统计摘要"""
        rospy.loginfo("=" * 50)
        rospy.loginfo("📊 聚类分析测试摘要")
        rospy.loginfo("=" * 50)
        rospy.loginfo(f"总扫描次数: {self.cluster_stats['total_scans']}")
        rospy.loginfo(f"平均聚类数: {self.cluster_stats['avg_clusters']:.2f}")
        rospy.loginfo(f"最大聚类数: {self.cluster_stats['max_clusters']}")
        rospy.loginfo(f"最小聚类数: {self.cluster_stats['min_clusters']}")
        rospy.loginfo("=" * 50)
        
        # 输出最终性能报告
        if self.cluster_stats['total_scans'] > 0:
            self.print_performance_report()


if __name__ == '__main__':
    try:
        tester = ClusteringAnalysisTester()
        rospy.spin()
        tester.print_summary()
    except rospy.ROSInterruptException:
        pass

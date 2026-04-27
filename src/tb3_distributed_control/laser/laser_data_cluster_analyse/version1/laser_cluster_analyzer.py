#!/usr/bin/env python3
"""
激光雷达数据聚类分析器
功能：
1. 订阅激光雷达数据 (例如 /tb3_0/scan)
2. 基于距离跳跃进行动态分区
3. 计算每个分区的实际长度
4. 区分静态障碍物和其他机器人
5. 根据雷达型号调整参数（雷达型号: LDS-01 或 LDS-02(默认)）
"""

import rospy
import numpy as np
import math
import time
from sensor_msgs.msg import LaserScan

class LaserClusterAnalyzer:
    def __init__(self, robot_namespace="/tb3_0", lidar_type="LDS-01"):
        """
        初始化激光雷达聚类分析器
        
        Args:
            robot_namespace: 机器人命名空间，例如 "/tb3_0"
            lidar_type: 雷达类型，支持 "LDS-01" 或 "LDS-02"
        """
        rospy.init_node('laser_cluster_analyzer', anonymous=True)
        
        self.robot_namespace = robot_namespace
        self.lidar_type = lidar_type
        

        
        # 雷达规格配置
        self.lidar_specs = {
            "LDS-01": {
                "min_range": 0.16,    # 最小检测距离 (m)
                "max_range": 3.5,     # 最大检测距离 (m)
                "resolution": 1.0,    # 角度分辨率 (度) - LDS-01较低精度
            },
            "LDS-02": {
                "min_range": 0.12,    # 最小检测距离 (m)
                "max_range": 8.0,     # 最大检测距离 (m)
                "resolution": 1.0,   # 角度分辨率 (度) - LDS-02高精度
            }
        }
        
        # 根据雷达类型设置参数
        if self.lidar_type not in self.lidar_specs:
            rospy.logwarn(f"未知雷达类型: {self.lidar_type}，使用默认LDS-02配置")
            self.lidar_type = "LDS-01"
        
        current_spec = self.lidar_specs[self.lidar_type]
        
        # 分区参数
        self.distance_jump_threshold = 0.069  # 距离跳跃阈值（机器人半径）

        # 仿真参数
        self.robot_min_length = 0.085  # 机器人识别最小长度
        self.robot_max_length = 0.110  # 机器人识别最大长度
        # 实物参数
        # self.robot_min_length = 0.035  # 机器人识别最小长度
        # self.robot_max_length = 0.06  # 机器人识别最大长度
        
        self.max_detection_range = 1.0  # 最大检测距离（米）
        self.min_detection_range = current_spec["min_range"]  # 根据雷达规格设置
        
        # 统计信息
        self.scan_count = 0
        
        # 性能监测
        self.total_processing_time = 0.0
        self.max_processing_time = 0.0
        
        # ROS订阅
        rospy.Subscriber(f"{robot_namespace}/scan", LaserScan, self.laser_callback)
        
        rospy.loginfo(f"🔍 激光雷达聚类分析器已启动 - {robot_namespace}/scan ({self.lidar_type})")
        
    def laser_callback(self, msg):
        """
        处理激光雷达数据，进行聚类分析
        """
        # 性能监测开始
        start_time = time.time()
        
        self.scan_count += 1
        
        # 简化调试信息（仅前2次扫描）
        if self.scan_count <= 2:
            print(f"🔍 扫描#{self.scan_count}: {len(msg.ranges)}点")
        
        # 提取有效的激光点
        valid_points = self.extract_valid_points(msg)
        
        if len(valid_points) == 0:
            rospy.logwarn(f"[扫描#{self.scan_count}] 没有检测到有效的激光点")
            return
        
        # 有效点统计
        if self.scan_count <= 2:
            print(f"  有效点: {len(valid_points)}")
        
        # 基于距离跳跃进行分区
        clusters = self.cluster_by_distance_jump(valid_points)
        
        # 分区统计
        if self.scan_count <= 2:
            print(f"  分区: {len(clusters)}个")
        
        # 检查首尾连接（处理360°跨越问题）
        original_cluster_count = len(clusters)
        clusters = self.merge_wraparound_clusters(clusters, valid_points)
        
        # 过滤单点分区（避免噪声）
        filtered_clusters = [cluster for cluster in clusters if len(cluster) >= 3]
        
        if self.scan_count <= 2:
            merged_info = "(已合并)" if len(clusters) != original_cluster_count else ""
            print(f"  最终分区: {len(filtered_clusters)}个{merged_info}\n")
        
        # 如果没有有效分区，输出调试信息
        if len(filtered_clusters) == 0:
            rospy.loginfo(f"[扫描#{self.scan_count}] 3.0m范围内未检测到有效障碍物分区")
            return
        
        # 计算每个分区的长度并分类
        self.analyze_clusters(filtered_clusters)
        
        # 性能监测结束
        processing_time = time.time() - start_time
        self.total_processing_time += processing_time
        self.max_processing_time = max(self.max_processing_time, processing_time)
        
        # 显示性能统计（每10次扫描）
        if self.scan_count % 10 == 0:
            avg_time = self.total_processing_time / self.scan_count
            print(f"🚀 性能统计 (第{self.scan_count}次扫描): 平均{avg_time*1000:.1f}ms, 频率{1/avg_time:.1f}Hz")
        
    def extract_valid_points(self, msg):
        """
        提取有效的激光点（NumPy向量化优化版本）
        
        Returns:
            List[dict]: 包含 {'index', 'angle', 'range'} 的列表
        """
        # NumPy向量化处理
        ranges = np.array(msg.ranges)
        n_points = len(ranges)
        
        # 计算所有角度（向量化）
        indices = np.arange(n_points)
        angles = msg.angle_min + indices * msg.angle_increment
        
        # 向量化过滤条件
        min_range = max(msg.range_min, self.min_detection_range)
        max_range = min(msg.range_max, self.max_detection_range)
        
        # 组合所有过滤条件（向量化布尔运算）
        valid_mask = (
            ~np.isnan(ranges) &           # 非NaN
            ~np.isinf(ranges) &           # 非无穷
            (ranges != 0.0) &             # 非零值
            (ranges >= min_range) &       # 大于最小距离
            (ranges <= max_range)         # 小于最大距离
        )
        
        # 提取有效数据
        valid_indices = indices[valid_mask]
        valid_angles = angles[valid_mask]
        valid_ranges = ranges[valid_mask]
        
        # 转换为列表格式（保持与原接口兼容）
        valid_points = []
        for i, angle, range_val in zip(valid_indices, valid_angles, valid_ranges):
            valid_points.append({
                'index': int(i),
                'angle': float(angle),
                'range': float(range_val)
            })
        
        return valid_points
    

    def cluster_by_distance_jump(self, points):
        """
        基于距离跳跃进行分区（改进版本）
        
        原理：
        - 相邻激光点之间的距离差超过阈值时，认为是不同的障碍物
        - 同时考虑角度跳跃和空间距离跳跃
        - 使用更智能的分区策略
        
        Args:
            points: 有效激光点列表
            
        Returns:
            List[List[dict]]: 分区后的点集列表
        """
        if len(points) == 0:
            return []
        
        if len(points) == 1:
            return [points]
        
        # 提取数组用于向量化计算
        ranges = np.array([p['range'] for p in points])
        angles = np.array([p['angle'] for p in points])
        
        # 计算相邻点的距离跳跃
        distance_jumps = np.abs(np.diff(ranges))
        
        # 计算相邻点的角度差
        angle_diffs = np.abs(np.diff(angles))
        
        # 计算相邻点在笛卡尔坐标系中的空间距离
        x_coords = ranges * np.cos(angles)
        y_coords = ranges * np.sin(angles)
        
        # 相邻点的空间距离
        spatial_distances = np.sqrt(np.diff(x_coords)**2 + np.diff(y_coords)**2)
        
        # 改进的分割条件：
        # 1. 距离跳跃大于阈值（传统方法）
        # 2. 角度跳跃过大（点之间角度间隔过大）
        # 3. 空间距离过大（在笛卡尔坐标系中的实际距离）
        split_mask = (
            (distance_jumps >= self.distance_jump_threshold) |  # 距离跳跃
            (angle_diffs >= 0.15) |  # 角度跳跃约8.6度（减小避免过度分割）
            (spatial_distances >= 0.1)  # 空间距离跳跃10cm
        )
        
        # 调试信息（仅前3次扫描）
        if self.scan_count <= 3:
            split_count = np.sum(split_mask)
            print(f"    分区: {split_count}个分割点")
        
        # 找到所有分割点的索引
        split_indices = np.where(split_mask)[0] + 1  # +1因为diff减少了一个元素
        
        # 添加起始和结束索引
        cluster_boundaries = np.concatenate([[0], split_indices, [len(points)]])
        
        # 根据边界分割成clusters
        clusters = []
        for i in range(len(cluster_boundaries) - 1):
            start_idx = cluster_boundaries[i]
            end_idx = cluster_boundaries[i + 1]
            cluster = points[start_idx:end_idx]
            if cluster:  # 确保cluster非空
                clusters.append(cluster)
        
        return clusters
    
    def merge_wraparound_clusters(self, clusters, valid_points):
        """
        处理360°跨越问题：检查第一个和最后一个分区是否应该合并
        
        原理：如果最后一个点（~359°）和第一个点（~0°）属于同一障碍物，
              它们会被错误分成两个分区，需要合并
        
        Args:
            clusters: 原始分区列表
            valid_points: 有效激光点列表
            
        Returns:
            List[List[dict]]: 合并后的分区列表
        """
        if len(clusters) < 2 or len(valid_points) < 2:
            return clusters
        
        first_cluster = clusters[0]
        last_cluster = clusters[-1]
        
        # 获取第一个分区的最后一个点和最后一个分区的第一个点（更准确的边界判断）
        first_cluster_last_point = first_cluster[-1] if first_cluster else None
        last_cluster_first_point = last_cluster[0] if last_cluster else None
        
        if not first_cluster_last_point or not last_cluster_first_point:
            return clusters
        
        # 获取全局第一个点和最后一个点
        global_first_point = valid_points[0]
        global_last_point = valid_points[-1]
        
        # 计算角度跨度：检查是否真正跨越360°边界
        first_angle = global_first_point['angle']
        last_angle = global_last_point['angle']
        
        # 调试信息
        rospy.logdebug(f"检查360°跨越: 第一个点角度={math.degrees(first_angle):.3f}°, 最后一个点角度={math.degrees(last_angle):.3f}°")
        
        # 计算真正的360°跨越：检查是否第一个分区在0°附近，最后一个分区在360°附近
        first_cluster_near_zero = first_angle >= -0.1 and first_angle <= 0.3  # 约0°附近(-6°到17°)
        last_cluster_near_360 = last_angle >= 6.0 and last_angle <= 6.3   # 约360°附近(344°到360°)
        
        # 计算跨越360°的角度差
        if first_cluster_near_zero and last_cluster_near_360:
            # 真正的360°跨越：从最后一个分区的角度到第一个分区的角度
            angle_diff = (2 * math.pi + first_angle) - last_angle
        else:
            # 普通角度差
            angle_diff = abs(last_angle - first_angle)
            if angle_diff > math.pi:
                angle_diff = 2 * math.pi - angle_diff
        
        # 距离差
        distance_jump = abs(global_first_point['range'] - global_last_point['range'])
        
        # 改进的合并条件：
        # 1. 必须是真正的360°跨越（第一个分区在0°附近，最后一个在360°附近）
        # 2. 角度差小于30度（跨越360°后的角度差）
        # 3. 距离差小于阈值（同一障碍物）
        should_merge = (
            first_cluster_near_zero and 
            last_cluster_near_360 and
            angle_diff < 0.52 and  # 约30度的跨越角度差
            distance_jump < self.distance_jump_threshold and
            len(first_cluster) >= 2 and 
            len(last_cluster) >= 2
        )
        
        if should_merge:
            if self.scan_count <= 2:
                print(f"  ✅ 合并跨越分区")
                
            # 合并：最后一个分区 + 第一个分区
            merged_cluster = last_cluster + first_cluster
            
            # 不要重新排序！保持原始的角度顺序
            # 360°跨越的分区应该保持：[...350°, 359°, 0°, 1°, 10°...]的自然顺序
            # 重新排序会破坏这个自然的跨越结构
            
            # 返回合并后的分区列表：合并分区 + 中间分区（排除首尾）
            return [merged_cluster] + clusters[1:-1]
        else:
            rospy.logdebug("❌ 不满足360°跨越合并条件，保持原始分区")
            if first_cluster_near_zero or last_cluster_near_360:
                rospy.logdebug(f"  详细原因: 第一个分区0°附近={first_cluster_near_zero}, 最后分区360°附近={last_cluster_near_360}")
                rospy.logdebug(f"  角度差={math.degrees(angle_diff):.3f}° (需<30°), 距离差={distance_jump:.3f}m (需<{self.distance_jump_threshold:.3f}m)")
        
        return clusters
    
    def filter_closest_points_in_cluster(self, cluster, max_points=10):
        """
        筛选分区中距离最近的N个点
        
        Args:
            cluster: 分区点集列表
            max_points: 保留的最近点数量，默认10个
            
        Returns:
            List[dict]: 筛选后的点集（按距离排序）
        """
        if len(cluster) <= max_points:
            # 如果点数不超过限制，返回原分区（按距离排序）
            return sorted(cluster, key=lambda p: p['range'])
        
        # 按距离排序，选择最近的max_points个点
        sorted_cluster = sorted(cluster, key=lambda p: p['range'])
        closest_points = sorted_cluster[:max_points]
        
        # 按原始角度顺序重新排列（保持扫描顺序）
        closest_points.sort(key=lambda p: p['angle'])
        
        return closest_points
    
    def filter_all_clusters(self, clusters, max_points_per_cluster=10):
        """
        对所有分区应用最近点筛选
        
        Args:
            clusters: 原始分区列表
            max_points_per_cluster: 每个分区保留的最近点数量
            
        Returns:
            List[List[dict]]: 筛选后的分区列表
            List[int]: 每个分区的原始点数（用于统计）
        """
        filtered_clusters = []
        original_counts = []
        
        for cluster in clusters:
            original_counts.append(len(cluster))
            filtered_cluster = self.filter_closest_points_in_cluster(cluster, max_points_per_cluster)
            filtered_clusters.append(filtered_cluster)
        
        return filtered_clusters, original_counts
    
    def analyze_clusters(self, clusters, original_point_counts=None):
        """
        分析每个分区的长度并分类为静态障碍物或机器人，最后筛选出最近的障碍点
        
        Args:
            clusters: 分区后的点集列表
            original_point_counts: 原始分区的点数列表（暂时未使用）
        """
        print("\n" + "="*80)
        print(f"[扫描#{self.scan_count}] 激光雷达聚类分析结果")
        print("="*80)

        
        # 检查是否有异常的全圆分区（360°跨越检查也要正确处理）
        for i, cluster in enumerate(clusters):
            first_angle = cluster[0]['angle']
            last_angle = cluster[-1]['angle']
            angle_span = last_angle - first_angle
            
            # 如果是360°跨越分区，重新计算角度跨度
            if angle_span < 0:  # 跨越360°边界
                angle_span = (2 * math.pi + last_angle) - first_angle
            
            # 检查是否有异常的全圆分区（超过90度可能有问题）
            if angle_span > math.pi / 2:  # 超过90度认为可能异常
                pass  # 移除警告信息
        
        robot_clusters = []
        static_clusters = []
        
        # 向量化批量计算所有分区的长度和平均距离
        cluster_lengths = self.calculate_all_cluster_lengths(clusters)
        cluster_avg_distances = [np.mean([p['range'] for p in cluster]) for cluster in clusters]
        
        for cluster_id, cluster in enumerate(clusters):
            # 使用预计算的长度
            length = cluster_lengths[cluster_id]
            
            # 使用预计算的平均距离
            avg_distance = cluster_avg_distances[cluster_id]
            
            # 角度跨度（正确处理360°跨越）
            first_angle = cluster[0]['angle']
            last_angle = cluster[-1]['angle']
            angle_span = last_angle - first_angle
            
            # 检查是否是360°跨越分区
            if angle_span < 0:  # 跨越360°边界，角度差为负
                # 重新计算真实的角度跨度
                angle_span = (2 * math.pi + last_angle) - first_angle
            
            # 分类：根据长度范围判断是机器人还是静态障碍物
            is_robot = self.robot_min_length <= length <= self.robot_max_length
            
            # 打印分区信息
            obstacle_type = "🤖 机器人" if is_robot else "🧱 静态障碍物"

            print(f"  点数量: {len(cluster)}")
            print(f"  实际长度: {length:.4f}m (余弦定理: 两端点直线距离)")
            print(f"  平均距离: {avg_distance:.4f}m")
            print(f"  角度跨度: {angle_span:.4f}rad ({math.degrees(angle_span):.3f}°)")

            print(f"  角度范围: [{math.degrees(cluster[0]['angle']):.3f}°, {math.degrees(cluster[-1]['angle']):.3f}°]")
            
            # 详细的分类依据
            if is_robot:
                print(f"  ✅ 判断依据: 长度 {length:.4f}m 在机器人识别范围 [{self.robot_min_length:.3f}m - {self.robot_max_length:.3f}m] 内")
                robot_clusters.append((cluster_id, cluster, length))
            else:
                print(f"  ❌ 判断依据: 长度 {length:.4f}m 超出机器人识别范围 [{self.robot_min_length:.3f}m - {self.robot_max_length:.3f}m]")
                static_clusters.append((cluster_id, cluster, length))
        
        # 统计汇总
        print("\n" + "-"*80)
        print(f"📊 分类统计:")
        print(f"  机器人数量: {len(robot_clusters)}")
        print(f"  静态障碍物数量: {len(static_clusters)}")
        
        # 🔍 最后步骤：为每个分区筛选最近的10个障碍点（用于后续处理）
        # 筛选最近的障碍点（每个分区最多10个点）
        if self.scan_count <= 2:
            print(f"📊 筛选最近10个障碍点:")
        filtered_robot_clusters = []
        filtered_static_clusters = []
        
        for cluster_id, cluster, length in robot_clusters:
            original_count = len(cluster)
            filtered_cluster = self.filter_closest_points_in_cluster(cluster, max_points=10)
            filtered_robot_clusters.append((cluster_id, filtered_cluster, length))
            if self.scan_count <= 2 and original_count > 10:
                print(f"  机器人分区#{cluster_id+1}: {original_count}点 → {len(filtered_cluster)}点")
            
        for cluster_id, cluster, length in static_clusters:
            original_count = len(cluster)
            filtered_cluster = self.filter_closest_points_in_cluster(cluster, max_points=10)
            filtered_static_clusters.append((cluster_id, filtered_cluster, length))
            if self.scan_count <= 2 and original_count > 10:
                print(f"  静态障碍物分区#{cluster_id+1}: {original_count}点 → {len(filtered_cluster)}点")
        
        total_original_points = sum(len(cluster) for _, cluster, _ in robot_clusters + static_clusters)
        total_filtered_points = sum(len(cluster) for _, cluster, _ in filtered_robot_clusters + filtered_static_clusters)
        # 💾 存储筛选结果为实例变量，供其他方法使用
        self.filtered_robot_clusters = filtered_robot_clusters  # [(cluster_id, filtered_points_list, length), ...]
        self.filtered_static_clusters = filtered_static_clusters  # [(cluster_id, filtered_points_list, length), ...]
        
        if self.scan_count <= 2:
            print(f"  总计: {total_original_points}点 → {total_filtered_points}点")
        

    
    def calculate_cluster_length(self, cluster):
        """
        计算分区的实际长度（使用余弦定理）
        
        原理：
        - 旧方法: 长度 = 平均距离 × 角度跨度 (假设弧形，不准确)
        - 新方法: 使用余弦定理计算两端点之间的直线距离
        
        余弦定理: c² = a² + b² - 2ab*cos(C)
        其中: a = r1 (第一个点距离), b = r2 (最后一个点距离), C = 角度差
        
        Args:
            cluster: 点集列表
            
        Returns:
            float: 分区长度（米）
        """
        if len(cluster) < 2:
            return 0.0
        
        # 获取两端点
        first_point = cluster[0]
        last_point = cluster[-1]
        
        r1 = first_point['range']  # 第一个点的距离
        r2 = last_point['range']   # 最后一个点的距离
        angle_diff = abs(last_point['angle'] - first_point['angle'])  # 角度差
        
        # 使用余弦定理计算两端点之间的直线距离
        # c² = r1² + r2² - 2*r1*r2*cos(angle_diff)
        length_squared = r1**2 + r2**2 - 2*r1*r2*math.cos(angle_diff)
        
        # 防止数值误差导致负数
        if length_squared < 0:
            length_squared = 0
        
        length = math.sqrt(length_squared)
        
        return length
    
    def calculate_all_cluster_lengths(self, clusters):
        """
        向量化批量计算所有分区的长度（改进版，正确处理360°跨越）
        
        Args:
            clusters: 分区列表
            
        Returns:
            List[float]: 每个分区的长度
        """
        if not clusters:
            return []
        
        lengths = []
        
        for cluster in clusters:
            if len(cluster) < 2:
                lengths.append(0.0)
                continue
                
            # 获取首尾点
            first_point = cluster[0]
            last_point = cluster[-1]
            
            r1 = first_point['range']
            r2 = last_point['range']
            angle1 = first_point['angle']
            angle2 = last_point['angle']
            
            # 检查是否是360°跨越分区
            # 如果 angle2 < angle1，说明跨越了360°边界
            if angle2 < angle1:  # 360°跨越分区
                # 计算真实的角度差（跨越360°）
                angle_diff = (2 * math.pi + angle2) - angle1
            else:
                # 普通分区：直接计算角度差
                angle_diff = abs(angle2 - angle1)
            
            # 统一使用余弦定理计算长度
            length_squared = r1**2 + r2**2 - 2*r1*r2*math.cos(angle_diff)
            length = math.sqrt(max(length_squared, 0))
            
            lengths.append(length)
        
        return lengths
    
    def get_closest_obstacle_points(self):
        """
        获取所有分区筛选后的最近障碍点
        
        Returns:
            dict: {
                'robot_obstacles': [(cluster_id, points_list, length), ...],
                'static_obstacles': [(cluster_id, points_list, length), ...],
                'all_closest_points': [point1, point2, ...]  # 所有最近点的扁平列表
            }
        """
        if not hasattr(self, 'filtered_robot_clusters'):
            rospy.logwarn("尚未进行障碍物分析，请先运行激光数据处理")
            return {
                'robot_obstacles': [],
                'static_obstacles': [],
                'all_closest_points': []
            }
        
        # 收集所有最近的障碍点
        all_closest_points = []
        
        # 添加机器人分区的最近点
        for _, points_list, _ in self.filtered_robot_clusters:
            all_closest_points.extend(points_list)
        
        # 添加静态障碍物分区的最近点
        for _, points_list, _ in self.filtered_static_clusters:
            all_closest_points.extend(points_list)
        
        return {
            'robot_obstacles': self.filtered_robot_clusters,
            'static_obstacles': self.filtered_static_clusters,
            'all_closest_points': all_closest_points
        }
    
    def get_closest_points_by_type(self, obstacle_type='all'):
        """
        根据障碍物类型获取最近的点
        
        Args:
            obstacle_type: 'robot', 'static', 或 'all'
            
        Returns:
            List[dict]: 点列表，每个点包含 {'index', 'angle', 'range'}
        """
        if not hasattr(self, 'filtered_robot_clusters'):
            return []
        
        points = []
        
        if obstacle_type in ['robot', 'all']:
            for _, points_list, _ in self.filtered_robot_clusters:
                points.extend(points_list)
        
        if obstacle_type in ['static', 'all']:
            for _, points_list, _ in self.filtered_static_clusters:
                points.extend(points_list)
        
        return points
    
    def run(self):
        """运行节点"""
        rospy.loginfo("激光雷达聚类分析器正在运行...")
        rospy.spin()


if __name__ == '__main__':
    try:
        # 从ROS参数获取配置
        robot_ns = rospy.get_param('~robot_namespace', '/tb3_0')
        lidar_type = rospy.get_param('~lidar_type', 'LDS-01')
        
        analyzer = LaserClusterAnalyzer(robot_namespace=robot_ns, lidar_type=lidar_type)
        analyzer.run()
        
    except rospy.ROSInterruptException:
        rospy.loginfo("激光雷达聚类分析器已停止")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
轨迹可视化节点 - 支持SDF障碍物绘制
功能：
1. 实时显示机器人轨迹和编队连线
2. 从指定SDF文件解析并绘制静态障碍物
3. 生成10张详细分析图表和统计报告
4. 支持避障分析、聚类分析和性能分析

使用方法：
1. 在脚本中直接修改OBSTACLE_MODE变量选择障碍物绘制模式：
   - 找到脚本第76行左右的：OBSTACLE_MODE = 'none'
   - 修改为以下选项之一：
     OBSTACLE_MODE = 'none'        # 不绘制障碍物（默认）
     OBSTACLE_MODE = 'simple'      # 绘制consensus_obstacle_1场景障碍物（4个障碍物），自动时间节点
     OBSTACLE_MODE = 'experiment'  # 绘制consensus_obstacle_real_experiment场景障碍物（3个障碍物），手动指定时刻
     OBSTACLE_MODE = 'experiment_line'  # 绘制consensus_obstacle_real_experiment_line场景障碍物（3个障碍物，直线轨迹）
   
2. 支持的障碍物配置：
   - 'none': 不绘制任何障碍物，适用于无障碍物环境测试
   - 'simple': 包含4个障碍物（2个圆形 + 1个矩形 + 1个小圆形），五边形时间节点自动分布
   - 'experiment': 包含3个障碍物（1个圆柱 + 2个正方形），五边形时间节点手动指定[30, 60, 90, 120]s
   - 'experiment_line': 包含3个障碍物（1个圆柱 + 2个正方形），五边形时间节点手动指定[9, 17, 25]s (直线轨迹)
   
3. 生成的图表文件：
   - trajectory_*.png (轨迹图，含障碍物和编队连线)
   - linear_velocity_*.png (线速度对比)
   - angular_velocity_*.png (角速度对比)
   - x_error_*.png (X方向误差)
   - y_error_*.png (Y方向误差) 
   - heading_error_*.png (航向角误差)
   - time_analysis_*.png (计算时间分析)
   - obstacle_distance_*.png (障碍物距离)
   - clustering_analysis_*.png (总聚类数统计)
   - avoidance_forces_*.png (避障向量)
   
4. 数据文件：
   - consensus_data_*.pkl (完整轨迹数据)
   - computation_stats_*.txt (计算性能统计报告)

注意：
- 默认为'none'模式（不绘制障碍物）
- 修改OBSTACLE_MODE变量后需要重新启动节点才能生效
- 障碍物配置为硬编码，无需world文件即可绘制
- 适用于对比不同场景下的编队控制性能

作者：分布式控制系统
"""
import rospy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.patches as patches
from matplotlib.patches import Ellipse, Rectangle, Circle
import pickle
import os
import xml.etree.ElementTree as ET
import math
from datetime import datetime
from tb3_distributed_control.msg import RobotHistoryData, LeaderHistoryData  # 导入自定义消息类型
import matplotlib.ticker as ticker
plt.switch_backend('Agg')  # 强制非交互后端，适配无GUI环境

def set_xaxis_to_show_max(max_time, nbins=10):
    """设置x轴刻度，确保最大值被显示
    
    Args:
        max_time: 最大时间值
        nbins: 刻度数量（默认10）
    """
    if max_time > 0:
        ax = plt.gca()
        ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=nbins, integer=False))
        plt.xlim([0, max_time])

# 动态路径获取所需的包
try:
    import rospkg
except ImportError:
    rospy.logwarn("rospkg未安装，将使用备用路径获取方案")

# 配置matplotlib字体支持（优先使用英文避免字体问题）
def configure_font():
    """Configure font, prioritize English to avoid font issues"""
    try:
        # Force English usage to avoid Chinese font missing issues
        plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Liberation Sans']
        plt.rcParams['axes.unicode_minus'] = False
        print("Font config: Using English titles (avoiding Chinese font issues)")
        return False  # Do not use Chinese
        
    except Exception as e:
        print("Font config failed: " + str(e))
        plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
        plt.rcParams['axes.unicode_minus'] = False
        return False

# 执行字体配置
USE_CHINESE = configure_font()

# 障碍物绘制模式配置 - 可手动修改此变量切换模式
# 'none': 不绘制障碍物
# 'simple': consensus_obstacle_1场景障碍物（4个障碍物）
# 'experiment': consensus_obstacle_real_experiment场景障碍物（4个障碍物）
# 'experiment_line': consensus_obstacle_real_experiment_line场景障碍物（3个障碍物，直线轨迹）

OBSTACLE_MODE = 'experiment'  # 默认不绘制障碍物

class ObstacleManager:
    """
    手动配置障碍物管理器
    
    功能：
    1. 根据指定模式手动配置障碍物
    2. 在轨迹图上绘制静态障碍物
    
    使用方法:
    obstacle_manager = ObstacleManager(mode='simple')
    obstacle_manager.draw_obstacles_on_plot(plt)
    """
    
    def __init__(self, mode='none'):
        """
        初始化障碍物管理器 - 手动配置版
        
        Args:
            mode: 障碍物模式 ('none', 'simple', 'experiment')
        """
        self.mode = mode
        self.obstacles = []
        
        self._load_obstacles_by_mode()
        rospy.loginfo(f"🎯 障碍物管理器初始化完成，模式: {mode}，加载 {len(self.obstacles)} 个障碍物")
    

    
    def _load_obstacles_by_mode(self):
        """根据模式加载障碍物信息"""
        if self.mode == 'none':
            self.obstacles = []
            rospy.loginfo("🚫 障碍物模式: none，不绘制障碍物")
        elif self.mode == 'simple':
            self.obstacles = self._get_simple_obstacles()
            rospy.loginfo(f"🟦 障碍物模式: simple (consensus_obstacle_1场景)")
        elif self.mode == 'experiment':
            self.obstacles = self._get_experiment_obstacles()
            rospy.loginfo(f"🟨 障碍物模式: experiment (consensus_obstacle_real_experiment场景)")
        elif self.mode == 'experiment_line':
            self.obstacles = self._get_experiment_line_obstacles()
            rospy.loginfo(f"🟩 障碍物模式: experiment_line (consensus_obstacle_real_experiment_line场景)")
        else:
            rospy.logwarn(f"未知障碍物模式: {self.mode}，默认不绘制障碍物")
            self.obstacles = []
    
    def _get_simple_obstacles(self):
        """手动配置的障碍物（对应 consensus_obstacle_1.world）"""
        return [
            {
                'type': 'circle',
                'name': 'obs_circle1',
                'pos': [1.7, 0.0],
                'radius': 0.3,
                'color': 'red',
                'alpha': 0.8
            },
            {
                'type': 'circle',  # 椭圆简化为圆形
                'name': 'obs_ellipse2', 
                'pos': [-3.0, 2.0],
                'radius': 0.4,
                'color': 'green',
                'alpha': 0.8
            },
            {
                'type': 'rectangle',
                'name': 'obs_rectangle3',
                'pos': [1.0, -1.5],
                'size': [1.0, 0.8],
                'rotation': 22.5,  # 对应SDF中的0.3927弧度
                'color': 'blue',
                'alpha': 0.8
            },
            {
                'type': 'circle',
                'name': 'obs_circle4',
                'pos': [0.5, 2.6],
                'radius': 0.15,
                'color': 'yellow',
                'alpha': 0.8
            }
        ]
    
    def _get_experiment_obstacles(self):
        """手动配置的障碍物（对应 consensus_obstacle_real_experiment.world ）"""
        return [
            # 圆柱障碍物 (0.0, 2.2) - 从world文件中提取的实际数据
            {
                'type': 'circle',
                'name': 'obs_circle',
                'pos': [-0.05, 2.2],  
                'radius': 0.12,
                'color': 'blue',
                'alpha': 0.8
            },
            # 方形障碍物1 (0.93, 1.5) - 从world文件中提取的实际数据
            {
                'type': 'rectangle',
                'name': 'obs_square1',
                'pos': [0.93, 1.5],  
                'size': [0.36, 0.36],
                'rotation': 0,
                'color': 'red',
                'alpha': 0.8
            },
            # 方形障碍物2 (2.15, 1.6) - 从world文件中提取的实际数据
            {
                'type': 'rectangle',
                'name': 'obs_square2',
                'pos': [2.15, 1.6],  
                'size': [0.36, 0.36],
                'rotation': 0,
                'color': 'red',
                'alpha': 0.8
            },
            # 方形障碍物3 (3.4, 0.5) - 从world文件中提取的实际数据
            {
                'type': 'rectangle',
                'name': 'obs_square3',
                'pos': [3.4, 0.5],  
                'size': [0.36, 0.36],
                'rotation': 0,
                'color': 'red',
                'alpha': 0.8    
            }
        ]
    
    def _get_experiment_line_obstacles(self):
        """手动配置的障碍物（对应 consensus_obstacle_real_experiment_line.world - 直线轨迹场景）"""
        return [
            # 方形障碍物1 (1.2, 1.3)
            {
                'type': 'circle',
                'name': 'obs_circle1',
                'pos': [1.2, 1.3],  
                'radius': 0.12,
                'color': 'blue',
                'alpha': 0.8
            },
            # 方形障碍物2 (1.7, 3.0)
            {
                'type': 'rectangle',
                'name': 'obs_square1',
                'pos': [1.7, 3.0],  
                'size': [0.36, 0.36],
                'rotation': 0,
                'color': 'red',
                'alpha': 0.8
            },
            # 方形障碍物3 (2.8, 2.1)
            {
                'type': 'rectangle',
                'name': 'obs_square2',
                'pos': [2.8, 2.1],  
                'size': [0.36, 0.36],
                'rotation': 0,
                'color': 'red',
                'alpha': 0.8    
            }
        ]
    
    def get_obstacles(self):
        """获取当前的障碍物列表"""
        return self.obstacles.copy()
    
    def draw_obstacles_on_plot(self, plt_figure):
        """在matplotlib图表上绘制所有障碍物"""
        if len(self.obstacles) == 0:
            rospy.loginfo("🎯 无障碍物需要绘制")
            return
            
        rospy.loginfo(f"🎯 开始绘制 {len(self.obstacles)} 个障碍物")
        for i, obstacle in enumerate(self.obstacles):
            self._draw_single_obstacle(plt_figure, obstacle)
        rospy.loginfo("🎯 障碍物绘制完成")
    
    def _draw_single_obstacle(self, plt_figure, obstacle):
        """绘制单个障碍物"""
        try:
            pos = obstacle['pos']
            color = obstacle.get('color', 'gray')
            alpha = obstacle.get('alpha', 0.7)  # 透明度
            
            if obstacle['type'] == 'circle':
                circle = Circle(pos, obstacle['radius'], 
                              color=color, alpha=alpha, zorder=5)
                plt_figure.gca().add_patch(circle)
                
            elif obstacle['type'] == 'ellipse':
                radius = obstacle['radius']
                rotation = obstacle.get('rotation', 0)
                ellipse = Ellipse(pos, radius[0]*2, radius[1]*2, 
                                angle=rotation, color=color, alpha=alpha, zorder=5)
                plt_figure.gca().add_patch(ellipse)
                
            elif obstacle['type'] == 'rectangle':
                size = obstacle['size']
                rotation = obstacle.get('rotation', 0)
                
                # 解决方案：使用matplotlib.patches.Rectangle，但要正确处理旋转
                # 由于Rectangle绕左下角旋转，我们需要计算旋转后的正确位置
                import matplotlib.patches as mpatches
                import matplotlib.transforms as transforms
                
                # 创建矩形（以中心为基准计算左下角位置）
                adjusted_pos = [pos[0] - size[0]/2, pos[1] - size[1]/2]
                rect = mpatches.Rectangle(adjusted_pos, size[0], size[1],
                                        color=color, alpha=alpha, zorder=5)
                
                # 如果有旋转，设置绕中心点旋转的变换
                if rotation != 0:
                    # 获取当前轴
                    ax = plt_figure.gca()
                    # 创建绕指定点旋转的变换
                    t = transforms.Affine2D().rotate_deg_around(pos[0], pos[1], rotation) + ax.transData
                    rect.set_transform(t)
                
                plt_figure.gca().add_patch(rect)
            
            # 添加障碍物标签（可选）
            if obstacle.get('show_label', False):
                plt_figure.text(pos[0], pos[1], obstacle.get('name', ''), 
                              ha='center', va='center', fontsize=8, zorder=6)
                
        except Exception as e:
            rospy.logwarn(f"⚠️ 绘制障碍物失败 {obstacle.get('name', 'unknown')}: {e}")
    


class ResultVisualizer:
    def _get_package_data_path(self):
        """动态获取包的data_collect目录路径，支持多种备用方案"""
        
        # 方案1：使用rospkg（推荐方案）
        try:
            import rospkg
            rospack = rospkg.RosPack()
            package_path = rospack.get_path('tb3_distributed_control')
            data_path = os.path.join(package_path, "data_collect")
            rospy.loginfo(f"🚀 方案1成功：rospkg获取包路径 -> {package_path}")
            return data_path
        except Exception as e:
            rospy.logwarn(f"方案1失败（rospkg）：{e}")
        
        # 方案2：从脚本路径推断包路径
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            # 脚本路径通常是：/path/to/package/scripts/visualize_results.py
            # 包根目录是：/path/to/package/
            package_root = os.path.dirname(script_dir)  # 向上一级到包根目录
            data_path = os.path.join(package_root, "data_collect")
            rospy.loginfo(f"🚀 方案2成功：脚本相对路径推断 -> {package_root}")
            return data_path
        except Exception as e:
            rospy.logwarn(f"方案2失败（脚本路径推断）：{e}")
        
        # 方案3：使用ROS参数服务器（如果launch文件设置了路径参数）
        try:
            if rospy.has_param('/data_collection_path'):
                data_path = rospy.get_param('/data_collection_path')
                rospy.loginfo(f"🚀 方案3成功：ROS参数服务器 -> {data_path}")
                return data_path
        except Exception as e:
            rospy.logwarn(f"方案3失败（ROS参数）：{e}")
        
        # 方案4：使用环境变量
        try:
            if 'ROS_WORKSPACE' in os.environ:
                workspace_path = os.environ['ROS_WORKSPACE']
                data_path = os.path.join(workspace_path, "src", "tb3_distributed_control", "data_collect")
                rospy.loginfo(f"🚀 方案4成功：环境变量ROS_WORKSPACE -> {workspace_path}")
                return data_path
        except Exception as e:
            rospy.logwarn(f"方案4失败（环境变量）：{e}")
        
        # 方案5：最后备用方案 - 用户主目录
        try:
            home_dir = os.path.expanduser("~")
            data_path = os.path.join(home_dir, "turtlebot3_consensus_data")
            rospy.logwarn(f"⚠️ 所有动态路径方案失败，使用最后备用方案：{data_path}")
            return data_path
        except Exception as e:
            rospy.logerr(f"所有路径获取方案均失败：{e}")
            # 最终应急方案
            return "/tmp/turtlebot3_consensus_data"

    def __init__(self):
        # 1. 动态获取包路径：tb3_distributed_control 包下的 data_collect 文件夹
        self.root_dir = self._get_package_data_path()
        os.makedirs(self.root_dir, exist_ok=True)  # 确保根目录存在
        
        # 2. 生成本次运行的唯一子文件夹名称（格式：2025-10-02-10-43-12-结果）
        # 注意：日期时间格式补零（如10月→10，2月→02；9点→09），避免格式混乱
        self.run_timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")  # 示例：2025-10-02-10-43-12
        self.run_dir = os.path.join(self.root_dir, f"{self.run_timestamp}-结果")  # 完整子文件夹路径
        os.makedirs(self.run_dir, exist_ok=True)  # 自动创建本次运行的子文件夹
        
        # 3. 初始化数据存储（领导者+5个机器人）- 使用话题数据结构
        # 注意：last_time初始化为-1.0，确保t=0.0的第一个数据点不会被过滤掉
        self.robots = {i: {'data': [], 'last_time': -1.0, 'zxeo_x': [], 'zxeo_y': []} for i in range(5)}
        self.leader = {'data': [], 'last_time': -1.0}
        
        # 🎯 初始化手动配置障碍物管理器
        # 修改 OBSTACLE_MODE 变量切换障碍物模式：'none', 'simple', 'experiment'
        self.obstacle_manager = ObstacleManager(mode=OBSTACLE_MODE)
        
        # 4. 注册关闭回调（保存数据+绘图，都存入子文件夹）
        rospy.on_shutdown(self.save_data)
        rospy.on_shutdown(self.plot_results)
        rospy.on_shutdown(self.generate_computation_statistics_only)  # 新增：仅生成计算时长统计报告
        
        # 🚀 ROS话题优化：订阅专用话题替代参数服务器轮询
        # 订阅领导者历史数据话题
        rospy.Subscriber("/leader/history", LeaderHistoryData, self.leader_data_callback)
        
        # 订阅5个机器人历史数据话题
        for robot_id in range(5):
            rospy.Subscriber(f"/tb3_{robot_id}/history", RobotHistoryData, 
                           self.robot_data_callback, callback_args=robot_id)
        
        rospy.loginfo(f"🚀 ROS话题优化版可视化节点启动成功！订阅6个专用数据话题，结果将保存到：{self.run_dir}")

    def leader_data_callback(self, msg):
        """🚀 ROS话题优化：接收领导者历史数据（替代参数服务器轮询）"""
        try:
            # 智能时间戳检查:区分节点重启和重复数据
            # 如果时间戳大幅回退(>1秒),认为是节点重启,重置last_time
            if msg.trajectory_time < self.leader['last_time'] - 1.0:
                rospy.logwarn(f"检测到领导者时间戳大幅回退({self.leader['last_time']:.2f} -> {msg.trajectory_time:.2f}),可能是节点重启,重置数据")
                self.leader['last_time'] = -1.0
            # 对于小幅回退或相等,视为重复数据并跳过
            elif msg.trajectory_time <= self.leader['last_time']:
                return  # 跳过重复数据
            
            self.leader['last_time'] = msg.trajectory_time
            
            # 转换为原有数据格式以兼容绘图代码
            leader_data = {
                't': msg.trajectory_time,
                'x0': msg.x0,
                'y0': msg.y0,
                'theta0': msg.theta0,
                'v0': msg.v0,
                'w0': msg.w0,
                'u0x': msg.u0x,
                'u0y': msg.u0y
            }
            
            self.leader['data'].append(leader_data)
            
            # 限制数据缓冲大小，避免内存无限增长
            if len(self.leader['data']) > 5000:
                self.leader['data'].pop(0)
                
        except Exception as e:
            rospy.logwarn(f"领导者数据回调错误：{e}")
    
    def robot_data_callback(self, msg, robot_id):
        """🚀 ROS话题优化：接收机器人历史数据（替代参数服务器轮询）"""
        try:
            # 防御式初始化：避免 shutdown 绘图阶段结构被重建后回调访问缺键
            if robot_id not in self.robots or not isinstance(self.robots[robot_id], dict):
                self.robots[robot_id] = {'data': [], 'last_time': -1.0, 'zxeo_x': [], 'zxeo_y': []}
            if 'last_time' not in self.robots[robot_id]:
                self.robots[robot_id]['last_time'] = -1.0
            if 'data' not in self.robots[robot_id]:
                self.robots[robot_id]['data'] = []
            if 'zxeo_x' not in self.robots[robot_id]:
                self.robots[robot_id]['zxeo_x'] = []
            if 'zxeo_y' not in self.robots[robot_id]:
                self.robots[robot_id]['zxeo_y'] = []

            # 智能时间戳检查:区分节点重启和重复数据
            # 如果时间戳大幅回退(>1秒),认为是节点重启,重置last_time
            if msg.trajectory_time < self.robots[robot_id]['last_time'] - 1.0:
                rospy.logwarn(f"检测到机器人{robot_id}时间戳大幅回退({self.robots[robot_id]['last_time']:.2f} -> {msg.trajectory_time:.2f}),可能是节点重启,重置数据")
                self.robots[robot_id]['last_time'] = -1.0
            # 对于小幅回退或相等,视为重复数据并跳过
            elif msg.trajectory_time <= self.robots[robot_id]['last_time']:
                return  # 跳过重复数据
            
            self.robots[robot_id]['last_time'] = msg.trajectory_time
            
            # 转换为原有数据格式以兼容绘图代码
            robot_data = {
                't': msg.trajectory_time,
                'xc': msg.xc,
                'yc': msg.yc,
                'thetac': msg.thetac,
                'vc': msg.vc,
                'wc': msg.wc,
                'xe': msg.xe,
                'ye': msg.ye,
                'thetae': msg.thetae,
                'xr': msg.xr,
                'yr': msg.yr,
                # 观测器估计数据
                'zxeo_x': msg.zxeo_x,
                'zxeo_y': msg.zxeo_y,
                # 避障相关数据（与msg文件顺序对齐）
                'raw_min_distance': msg.raw_min_obstacle_distance,
                'obstacle_distance': msg.closest_obstacle_distance,
                'total_clusters_count': msg.total_clusters_count,
                'avoidance_force_magnitude': msg.avoidance_force_magnitude,

                # 性能分析数据
                'computation_time': msg.computation_time,
                'full_cycle_time': msg.full_cycle_time
            }
            
            self.robots[robot_id]['data'].append(robot_data)
            # 单独存储观测器数据用于绘图
            self.robots[robot_id]['zxeo_x'].append(msg.zxeo_x)
            self.robots[robot_id]['zxeo_y'].append(msg.zxeo_y)
            
            # 限制数据缓冲大小，避免内存无限增长
            if len(self.robots[robot_id]['data']) > 5000:
                self.robots[robot_id]['data'].pop(0)
                
        except Exception as e:
            rospy.logwarn(f"机器人{robot_id}数据回调错误：{e}")

    def fetch_data(self, event):
        """🚀 已优化：使用话题订阅替代轮询，此方法保留以兼容旧版本"""
        # 使用话题订阅后此方法不再需要，数据通过回调自动接收
        pass

    def save_data(self):
        """🚀 话题优化版：保存本次运行的完整数据到子文件夹（pickle格式，不覆盖）"""
        # 转换话题数据为原有格式以兼容绘图代码
        converted_leader = None
        converted_robots = {}
        
        # 转换领导者数据
        if self.leader['data']:
            converted_leader = {}
            for key in ['t', 'x0', 'y0', 'theta0', 'v0', 'w0', 'u0x', 'u0y']:
                converted_leader[key] = [item[key] for item in self.leader['data']]
        
        # 转换机器人数据
        for robot_id in range(5):
            if self.robots[robot_id]['data']:
                converted_robots[robot_id] = {}
                for key in ['t', 'xc', 'yc', 'thetac', 'vc', 'wc', 'xe', 'ye', 'thetae', 'xr', 'yr', 'raw_min_distance', 'obstacle_distance', 'total_clusters_count', 'avoidance_force_magnitude', 'computation_time', 'full_cycle_time']:
                    converted_robots[robot_id][key] = [item[key] for item in self.robots[robot_id]['data']]
                # 添加观测器估计数据
                converted_robots[robot_id]['zxeo_x'] = self.robots[robot_id]['zxeo_x']
                converted_robots[robot_id]['zxeo_y'] = self.robots[robot_id]['zxeo_y']
            else:
                converted_robots[robot_id] = None
        
        # 检查数据完整性 - 只要有领导者数据且至少有一个机器人有数据就可以保存
        if converted_leader is None:
            rospy.logwarn("🚀 领导者数据为空，跳过保存")
            return
        
        # 检查是否有机器人数据
        has_robot_data = any(converted_robots[i] is not None for i in range(5))
        if not has_robot_data:
            rospy.logwarn("🚀 所有机器人数据为空，跳过保存")
            return
        
        # 🎯 计算实际编队中心（所有机器人位置的几何中心）
        formation_centroid = None
        try:
            # 收集所有有效机器人的位置数据
            robot_x_arrays = []
            robot_y_arrays = []
            for robot_id in range(5):
                if converted_robots[robot_id] is not None:
                    if 'xc' in converted_robots[robot_id] and 'yc' in converted_robots[robot_id]:
                        robot_x_arrays.append(converted_robots[robot_id]['xc'])
                        robot_y_arrays.append(converted_robots[robot_id]['yc'])
            
            # 如果有足够的机器人数据，计算编队中心
            if len(robot_x_arrays) >= 3:  # 至少需要3个机器人
                # 统一数据长度（取最短长度）
                min_length = min(len(x) for x in robot_x_arrays)
                robot_x_trunc = [x[:min_length] for x in robot_x_arrays]
                robot_y_trunc = [y[:min_length] for y in robot_y_arrays]
                
                # 计算每个时间点的中心位置（所有机器人位置的平均值）
                centroid_x = np.mean(robot_x_trunc, axis=0).tolist()
                centroid_y = np.mean(robot_y_trunc, axis=0).tolist()
                
                # 使用领导者的时间轴（或机器人的时间轴）
                if converted_leader and 't' in converted_leader:
                    centroid_t = converted_leader['t'][:min_length]
                elif converted_robots[0] is not None and 't' in converted_robots[0]:
                    centroid_t = converted_robots[0]['t'][:min_length]
                else:
                    centroid_t = list(range(min_length))  # 备用时间轴
                
                formation_centroid = {
                    't': centroid_t,
                    'xc': centroid_x,
                    'yc': centroid_y
                }
                rospy.loginfo(f"🎯 计算编队中心：包含{len(centroid_x)}个数据点，基于{len(robot_x_arrays)}个机器人")
            else:
                rospy.logwarn(f"🎯 机器人数据不足（{len(robot_x_arrays)}/5），无法计算编队中心")
        except Exception as e:
            rospy.logerr(f"🎯 计算编队中心失败：{e}")
            formation_centroid = None
        
        # 组织数据（包含时间戳和保存路径，便于后续回溯）
        data = {
            'run_time': self.run_timestamp,  # 本次运行时间戳
            'save_dir': self.run_dir,      # 本次结果保存路径
            'leader': converted_leader,         # 领导者数据（虚拟编队中心）
            'robots': converted_robots,         # 5个机器人数据
            'formation_centroid': formation_centroid,  # 🎯 实际编队中心（所有机器人位置的几何平均）
            'time_source': 'ROS_Topic_Optimized'  # 时间来源标识（话题优化版）
        }
        
        # 保存到子文件夹（文件名含时间戳，进一步避免误删）
        pickle_path = os.path.join(self.run_dir, f"consensus_data_{self.run_timestamp}.pkl")
        with open(pickle_path, 'wb') as f:
            pickle.dump(data, f)
        rospy.loginfo(f"🚀 话题数据已保存：{pickle_path}，包含{len(converted_leader['t'])}个领导者数据点")

    def clean_data_lengths(self, data_dict, reference_key='t'):
        """清理数据长度不匹配问题，以reference_key为基准截取其他数组"""
        if not data_dict or reference_key not in data_dict or not data_dict[reference_key]:
            return data_dict
        
        ref_length = len(data_dict[reference_key])
        cleaned_data = {}
        
        for key, values in data_dict.items():
            if values and isinstance(values, (list, np.ndarray)):
                if len(values) == ref_length:
                    cleaned_data[key] = values
                else:
                    # 截取到参考长度
                    min_len = min(ref_length, len(values))
                    cleaned_data[key] = values[:min_len] if isinstance(values, (list, np.ndarray)) else values
                    rospy.logwarn(f"数据长度不匹配：{key}原长度{len(values)}，已截取到{min_len}")
            else:
                cleaned_data[key] = values
        
        return cleaned_data

    def plot_results(self):
        """绘制6张图表，全部保存到本次运行的子文件夹中"""
        # 加载本次运行的数据（从子文件夹的pickle文件）
        pickle_path = os.path.join(self.run_dir, f"consensus_data_{self.run_timestamp}.pkl")
        if not os.path.exists(pickle_path):
            rospy.logerr(f"数据文件不存在：{pickle_path}")
            return
        with open(pickle_path, 'rb') as f:
            data = pickle.load(f)
        
        # 清理数据长度不匹配问题（使用局部变量，避免覆盖运行时回调缓冲）
        leader_plot = self.clean_data_lengths(data['leader'], 't')
        robots_plot = {}
        for rid, robot_data in data['robots'].items():
            if robot_data is not None:
                robots_plot[rid] = self.clean_data_lengths(robot_data, 't')
            else:
                robots_plot[rid] = None
        
        # 提取领导者的相对时间轴（作为所有图表的时间基准）
        leader_t = np.array(leader_plot['t'], dtype=np.float64) if leader_plot['t'] else np.array([])
        # 时间轴最大范围：向上取整到最接近的整数（179.9 -> 180）
        max_time = np.ceil(leader_t[-1]) if len(leader_t) > 0 else 120

        # -------------------------- 1. 编队轨迹图 --------------------------
        plt.figure(1, figsize=(8, 6))
        valid_robots = []
        robot_x_list = []
        robot_y_list = []
        
        # 绘制每个机器人的实际轨迹和理想轨迹
        for rid in robots_plot:
            robot = robots_plot[rid]
            if robot is not None and robot['xc'] and robot['yc'] and len(robot['xc']) == len(robot['t']):
                valid_robots.append(robot)
                robot_x_list.append(np.array(robot['xc']))
                robot_y_list.append(np.array(robot['yc']))
                
                # 绘制实际轨迹（实线）
                line_actual = plt.plot(robot['xc'], robot['yc'], linewidth=2, label=f'Robot {rid} Actual (solid)')[0]
                
                # 绘制理想轨迹（虚线，使用相同颜色）
                if robot.get('xr') and robot.get('yr') and len(robot['xr']) == len(robot['t']):
                    plt.plot(robot['xr'], robot['yr'], '--', linewidth=2, 
                            color=line_actual.get_color(), alpha=0.7, 
                            label=f'Robot {rid} Ideal (dashed)')
                else:
                    rospy.logwarn(f"tb3_{rid} 理想轨迹数据无效，跳过理想轨迹绘制")
            else:
                rospy.logwarn(f"tb3_{rid} 实际轨迹数据无效，跳过轨迹绘制")
        
        # 绘制领导者参考轨迹（预设的理想路径）
        if leader_plot['x0'] and leader_plot['y0']:
            plt.plot(leader_plot['x0'], leader_plot['y0'], '--', linewidth=2, 
                    label='Leader Reference Trajectory', alpha=0.7, color='purple')
        
        # 🎯 绘制实际编队中心（所有机器人位置的几何平均）- 使用save_data()中保存的数据
        if 'formation_centroid' in data and data['formation_centroid'] is not None:
            centroid = data['formation_centroid']
            if 'xc' in centroid and 'yc' in centroid:
                plt.plot(centroid['xc'], centroid['yc'], linewidth=2, 
                        color='deepskyblue', label='Formation Centroid', zorder=10)
        
        # 🚀 新增功能：在30秒到最后停止之间平均添加6个时间节点绘制机器人连线（正5边形）
        if len(valid_robots) == 5 and len(leader_t) > 0:
            # 根据OBSTACLE_MODE决定使用自动时间节点还是手动指定时刻
            if OBSTACLE_MODE == 'experiment':
                # experiment模式：手动指定3个时刻 + 自动添加最后时刻（适用于实物实验）
                manual_time_nodes = [20.0, 32.0, 48.0]  # 可以根据需要修改这些时刻
                time_nodes = manual_time_nodes + [max_time]  # 最后一个时刻自动获取
                # rospy.loginfo(f"{OBSTACLE_MODE}模式：使用手动指定的时间节点 {manual_time_nodes} + 自动结束时刻 {max_time:.1f}s")
            elif OBSTACLE_MODE == 'experiment_line':
                # experiment_line模式：手动指定2个时刻 + 自动添加最后时刻（直线轨迹）
                manual_time_nodes = [9.0, 17.0]  # 9秒、17秒
                time_nodes = manual_time_nodes + [max_time]  # 最后一个时刻自动获取
                # rospy.loginfo(f"{OBSTACLE_MODE}模式：使用手动指定的时间节点 {manual_time_nodes} + 自动结束时刻 {max_time:.1f}s")
            else:
                # 其他模式：自动在30秒到最后停止之间平均分布6个时间节点
                time_start = 30.0
                time_end = max_time
                
                if time_end > time_start:
                    # 在时间范围内平均分布6个时间节点
                    time_nodes = np.linspace(time_start, time_end, 6)
                    # rospy.loginfo(f"在轨迹图中添加6个时间节点的机器人连线：{time_nodes}")
                else:
                    time_nodes = []
                    rospy.logwarn(f"运行时间不足30秒，跳过机器人连线绘制 (总时间: {time_end:.1f}s)")
            
            # 为每个时间节点绘制机器人连线
            for i, target_time in enumerate(time_nodes):
                robot_positions_at_time = []
                
                # 找到所有机器人在该时间点的位置
                for rid in range(5):
                    robot = robots_plot.get(rid)
                    if robot is not None and robot['t'] and robot['xc'] and robot['yc']:
                        t_array = np.array(robot['t'])
                        x_array = np.array(robot['xc'])
                        y_array = np.array(robot['yc'])
                        
                        # 找到最接近目标时间的索引
                        time_diff = np.abs(t_array - target_time)
                        closest_idx = np.argmin(time_diff)
                        
                        # 只有当时间差小于合理范围时才使用该点
                        if time_diff[closest_idx] < 2.0:  # 允许2秒的误差
                            robot_positions_at_time.append((x_array[closest_idx], y_array[closest_idx]))
                        else:
                            robot_positions_at_time.append(None)
                
                # 如果5个机器人的位置都有效，绘制连线
                    valid_positions = [pos for pos in robot_positions_at_time if pos is not None]
                    if len(valid_positions) == 5:
                        # 提取x和y坐标
                        x_coords = [pos[0] for pos in robot_positions_at_time]
                        y_coords = [pos[1] for pos in robot_positions_at_time]
                        
                        # 绘制正5边形连线：按顺序连接，最后连回起点
                        polygon_x = x_coords + [x_coords[0]]  # 闭合多边形
                        polygon_y = y_coords + [y_coords[0]]
                        
                        # 根据模式调整颜色渐变参数
                        if OBSTACLE_MODE == 'experiment':
                            # experiment模式：4个节点的颜色渐变
                            total_nodes = 4
                        else:
                            # 其他模式：6个节点的颜色渐变
                            total_nodes = 6
                        
                        # 使用不同的颜色和透明度表示不同时间节点
                        alpha_value = min(1.0, 0.4 + 0.1 * i)  # 透明度从0.4到0.9渐变，确保不超过1.0
                        color_intensity = min(1.0, 0.3 + 0.7 * (i / (total_nodes - 1)))  # 颜色强度渐变，确保不超过1.0
                        
                        # 确保所有RGB值都在0-1范围内
                        red_value = min(1.0, max(0.0, color_intensity))
                        green_value = 0.0
                        blue_value = min(1.0, max(0.0, 1.0 - color_intensity))
                        
                        plt.plot(polygon_x, polygon_y, 
                                color=(red_value, green_value, blue_value),  # 从紫色到蓝色渐变
                                linewidth=1.5, 
                                alpha=alpha_value, 
                                label=None)  # 移除Formation时间标签，避免图例过大
                        
                        # 在机器人位置添加标记点，确保alpha值不超过1.0
                        scatter_alpha = min(1.0, alpha_value + 0.2)  # 限制alpha值在0-1范围内
                        plt.scatter(x_coords, y_coords, 
                                   s=25, 
                                   color=(red_value, green_value, blue_value), 
                                   alpha=scatter_alpha, 
                                   zorder=5)
                        
                        # rospy.loginfo(f"时间节点 {target_time:.1f}s: 成功绘制5边形连线")
                    else:
                        # 数据不完整时静默跳过，避免产生警告（这在早期时间节点是正常现象）
                        rospy.logdebug(f"时间节点 {target_time:.1f}s: 机器人位置数据不完整 ({len(valid_positions)}/5)，跳过该时间节点")
        else:
            rospy.logdebug(f"数据不完整，跳过机器人连线绘制 (有效机器人: {len(valid_robots)}/5)")
        
        # 🎯 绘制静态障碍物（新增功能）
        self.obstacle_manager.draw_obstacles_on_plot(plt)
        
        plt.axis('equal')
        plt.xlabel('X Coordinate (m)')
        plt.ylabel('Y Coordinate (m)')
        plt.legend(fontsize=4, loc='upper right')  # 缩小字体并固定位置
        plt.grid(True, alpha=0.3)
        plt.title(f'Formation Trajectory with Obstacles - Relative Time ({self.run_timestamp})')
        # 保存到子文件夹
        traj_path = os.path.join(self.run_dir, f"trajectory_{self.run_timestamp}.png")
        plt.savefig(traj_path, dpi=300, bbox_inches='tight')
        plt.close()  # 关闭图表，释放内存

        # -------------------------- 2. 线速度对比图 --------------------------
        plt.figure(2, figsize=(8, 4))
        for rid in robots_plot:
            robot = robots_plot[rid]
            if robot is not None and robot['t'] and robot['vc'] and len(robot['t']) == len(robot['vc']):
                t_robot = np.array(robot['t'])
                plt.plot(t_robot, robot['vc'], linewidth=2, label=f'v_{rid}')
        if leader_plot['t'] and leader_plot['v0']:
            plt.plot(leader_t, leader_plot['v0'], '--', linewidth=2, label='v_Leader')
        
        plt.xlim(0, max_time)
        plt.ylim(-0.3, 0.3)
        plt.xlabel('Trajectory Time (s, from node start)')
        plt.ylabel('Linear Velocity (m/s)')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.title(f'Linear Velocities - Relative Time ({self.run_timestamp})')
        set_xaxis_to_show_max(max_time)  # 确保最大值显示
        # 保存到子文件夹
        linear_vel_path = os.path.join(self.run_dir, f"linear_velocity_{self.run_timestamp}.png")
        plt.savefig(linear_vel_path, dpi=300, bbox_inches='tight')
        plt.close()

        # -------------------------- 3. 角速度对比图 --------------------------
        plt.figure(3, figsize=(8, 4))
        for rid in robots_plot:
            robot = robots_plot[rid]
            if robot is not None and robot['t'] and robot['wc'] and len(robot['t']) == len(robot['wc']):
                t_robot = np.array(robot['t'])
                plt.plot(t_robot, robot['wc'], linewidth=2, label=f'ω_{rid}')
        if leader_plot['t'] and leader_plot['w0']:
            plt.plot(leader_t, leader_plot['w0'], '--', linewidth=2, label='ω_Leader')
        
        plt.xlim(0, max_time)
        plt.ylim(-3.0, 3.0)
        plt.xlabel('Trajectory Time (s, from node start)')
        plt.ylabel('Angular Velocity (rad/s)')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.title(f'Angular Velocities - Relative Time ({self.run_timestamp})')
        set_xaxis_to_show_max(max_time)  # 确保最大值显示
        # 保存到子文件夹
        angular_vel_path = os.path.join(self.run_dir, f"angular_velocity_{self.run_timestamp}.png")
        plt.savefig(angular_vel_path, dpi=300, bbox_inches='tight')
        plt.close()

        # -------------------------- 4. X方向误差图 --------------------------
        plt.figure(4, figsize=(8, 4))
        for rid in robots_plot:
            robot = robots_plot[rid]
            if robot is not None and robot['t'] and robot['xe'] and len(robot['t']) == len(robot['xe']):
                t_robot = np.array(robot['t'])
                plt.plot(t_robot, robot['xe'], linewidth=2, label=f'xe_{rid}')
        
        plt.xlim(0, max_time)
        # plt.ylim(-1.0, 1.0)  # 纵轴范围调整为-1到1米
        plt.xlabel('Trajectory Time (s, from node start)')
        plt.ylabel('X Direction Error (m)')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.title(f'X Position Error - Relative Time ({self.run_timestamp})')
        set_xaxis_to_show_max(max_time)  # 确保最大值显示
        # 保存到子文件夹
        x_error_path = os.path.join(self.run_dir, f"x_error_{self.run_timestamp}.png")
        plt.savefig(x_error_path, dpi=300, bbox_inches='tight')
        plt.close()

        # -------------------------- 5. Y方向误差图 --------------------------
        plt.figure(5, figsize=(8, 4))
        for rid in robots_plot:
            robot = robots_plot[rid]
            if robot is not None and robot['t'] and robot['ye'] and len(robot['t']) == len(robot['ye']):
                t_robot = np.array(robot['t'])
                plt.plot(t_robot, robot['ye'], linewidth=2, label=f'ye_{rid}')
        
        plt.xlim(0, max_time)
        # plt.ylim(-1.0, 1.0)  # 纵轴范围调整为-1到1米
        plt.xlabel('Trajectory Time (s, from node start)')
        plt.ylabel('Y Direction Error (m)')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.title(f'Y Position Error - Relative Time ({self.run_timestamp})')
        set_xaxis_to_show_max(max_time)  # 确保最大值显示
        # 保存到子文件夹
        y_error_path = os.path.join(self.run_dir, f"y_error_{self.run_timestamp}.png")
        plt.savefig(y_error_path, dpi=300, bbox_inches='tight')
        plt.close()

        # -------------------------- 6. 航向角误差图 --------------------------
        plt.figure(6, figsize=(8, 4))
        for rid in robots_plot:
            robot = robots_plot[rid]
            if robot is not None and robot['t'] and robot['thetae'] and len(robot['t']) == len(robot['thetae']):
                t_robot = np.array(robot['t'])
                plt.plot(t_robot, robot['thetae'], linewidth=2, label=f'thetae_{rid}')
        
        plt.xlim(0, max_time)
        # plt.ylim(-np.pi, np.pi)  # 角度误差应该在合理范围内
        plt.xlabel('Trajectory Time (s, from node start)')
        plt.ylabel('Heading Angle Error (rad)')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.title(f'Heading Error - Relative Time ({self.run_timestamp})')
        set_xaxis_to_show_max(max_time)  # 确保最大值显示
        # 保存到子文件夹
        heading_error_path = os.path.join(self.run_dir, f"heading_error_{self.run_timestamp}.png")
        plt.savefig(heading_error_path, dpi=300, bbox_inches='tight')
        plt.close()

        # -------------------------- 7. 时间分析对比图（合并版）--------------------------
        plt.figure(7, figsize=(16, 10))  # 增大图片尺寸，提供更多空间
        
        # 定义颜色列表，确保每个机器人的虚线和实线使用相同颜色
        colors = ['blue', 'orange', 'green', 'red', 'purple']
        
        # 计算所有数据的最大值，用于动态设置纵轴范围
        max_time_value = 0
        
        # 绘制各机器人的时间数据
        for i, rid in enumerate(robots_plot):
            robot = robots_plot[rid]
            if (robot is not None and robot['t'] and robot.get('computation_time') and robot.get('full_cycle_time') and 
                len(robot['t']) == len(robot['computation_time']) == len(robot['full_cycle_time'])):
                
                t_robot = np.array(robot['t'])
                algo_time_ms = np.array(robot['computation_time']) * 1000  # 纯算法时间（毫秒）
                full_time_ms = np.array(robot['full_cycle_time']) * 1000  # 完整周期时间（毫秒）
                
                # 更新最大值
                max_time_value = max(max_time_value, max(algo_time_ms))  # 只考虑算法时间
                # max_time_value = max(max_time_value, max(full_time_ms))  # 暂时注释
                
                color = colors[i % len(colors)]
                
                # 绘制纯算法计算时间（增加线宽以便看清尖峰）
                plt.plot(t_robot, algo_time_ms, linewidth=0.8, color=color, 
                        alpha=0.7, label=f'Robot {rid} - Algorithm Only')
                
                # 标注最大值位置（如果超过80ms）
                max_algo_time = np.max(algo_time_ms)
                if max_algo_time > 80:
                    max_idx = np.argmax(algo_time_ms)
                    max_t = t_robot[max_idx]
                    plt.scatter(max_t, max_algo_time, color=color, s=50, marker='o', 
                               edgecolors='black', linewidths=1, zorder=10)
                    plt.text(max_t, max_algo_time + 5, f'{max_algo_time:.1f}ms', 
                            fontsize=8, ha='center', color=color, weight='bold')
                
                # 暂时注释完整周期时间
                # plt.plot(t_robot, full_time_ms, linewidth=2, color=color, 
                #         linestyle='-', alpha=0.8, label=f'Robot {rid} - Full Cycle')
        
        # 绘制0.1s控制周期基准线（100ms）
        plt.axhline(y=100, color='red', linestyle='-.', linewidth=3, alpha=0.95, 
                   label='Control Period (100ms)', zorder=10)
        
        # 动态计算纵轴上限，确保显示所有数据点
        y_max = max(200, max_time_value * 1.1)  # 至少200ms，或者最大值的1.1倍
        
        # 添加警告区域（超过100ms的部分）
        plt.axhspan(100, y_max, alpha=0.1, color='red', label='Overrun Zone')
        
        plt.xlim(0, max_time)
        plt.ylim(0, y_max)  # 动态设置纵轴范围以显示所有数据
        plt.xlabel('Trajectory Time (s, from node start)')
        plt.ylabel('Time (ms)')
        
        # 将图例放在右侧，避免遮挡数据
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
        plt.grid(True, alpha=0.3)
        plt.title(f'Time Analysis: Algorithm Time - {self.run_timestamp}')
        set_xaxis_to_show_max(max_time)  # 确保最大值显示
        
        # 生成简化统计信息并放在图的底部
        stats_lines = []
        overall_stats = {
            'algo_times': [], 'full_times': [], 'total_samples': 0
        }
        
        for rid in robots_plot:
            robot = robots_plot[rid]
            if robot is not None and robot.get('computation_time') and robot.get('full_cycle_time'):
                algo_times = np.array(robot['computation_time']) * 1000
                full_times = np.array(robot['full_cycle_time']) * 1000
                
                # 基本统计 - 算法时间
                avg_algo = np.mean(algo_times)
                min_algo = np.min(algo_times)
                max_algo = np.max(algo_times)
                
                # 基本统计 - 完整周期时间
                avg_full = np.mean(full_times)
                min_full = np.min(full_times)
                max_full = np.max(full_times)
                
                total_samples = len(full_times)
                
                # 累积全局统计
                overall_stats['algo_times'].extend(algo_times)
                overall_stats['full_times'].extend(full_times)
                overall_stats['total_samples'] += total_samples
                
                # 生成每个机器人的简化统计行
                stats_lines.append(
                    f"Robot {rid}:  Algorithm: {avg_algo:.1f}ms avg [{min_algo:.1f}-{max_algo:.1f}], "
                    f"Full Cycle: {avg_full:.1f}ms avg [{min_full:.1f}-{max_full:.1f}]"
                )
        
        # 添加全局统计摘要
        if overall_stats['total_samples'] > 0:
            algo_times_arr = np.array(overall_stats['algo_times'])
            full_times_arr = np.array(overall_stats['full_times'])
            
            global_algo_avg = np.mean(algo_times_arr)
            global_algo_min = np.min(algo_times_arr)
            global_algo_max = np.max(algo_times_arr)
            
            global_full_avg = np.mean(full_times_arr)
            global_full_min = np.min(full_times_arr)
            global_full_max = np.max(full_times_arr)
            
            stats_lines.append("")
            stats_lines.append("=== OVERALL PERFORMANCE SUMMARY ===")
            stats_lines.append(f"Algorithm Time:  {global_algo_avg:.1f}ms avg [{global_algo_min:.1f}-{global_algo_max:.1f}]")
            stats_lines.append(f"Full Cycle Time: {global_full_avg:.1f}ms avg [{global_full_min:.1f}-{global_full_max:.1f}]")
            stats_lines.append(f"Total Samples: {overall_stats['total_samples']}, Control Period: 100ms")
        
        # 将简化的统计信息放在图的底部
        stats_text = "\n".join(stats_lines)
        plt.figtext(0.02, 0.02, stats_text, fontsize=9, family='monospace',
                   bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgray', alpha=0.95),
                   verticalalignment='bottom')
        
        # 调整底部空间以适应统计信息
        plt.subplots_adjust(bottom=0.25, right=0.75)
        
        # 保存到子文件夹
        time_analysis_path = os.path.join(self.run_dir, f"time_analysis_{self.run_timestamp}.png")
        plt.savefig(time_analysis_path, dpi=300, bbox_inches='tight')
        plt.close()

        # -------------------------- 8. 障碍物最近点距离图 --------------------------
        plt.figure(8, figsize=(10, 6))
        
        # 收集所有有效距离数据以计算自适应范围
        all_distances = []
        
        # 🔧 可选：绘制雷达原始最小距离（默认注释掉）
        # for rid in self.robots:
        #     robot = self.robots[rid]
        #     if robot is not None and robot.get('raw_min_distance') and robot.get('t') and len(robot['raw_min_distance']) == len(robot['t']):
        #         robot_t = np.array(robot['t'])
        #         raw_distances = np.array(robot['raw_min_distance'])
        #         valid_mask = (raw_distances > 0) & (raw_distances < 50.0)
        #         if np.any(valid_mask):
        #             valid_times = robot_t[valid_mask]
        #             valid_distances = raw_distances[valid_mask]
        #             plt.plot(valid_times, valid_distances, ':', linewidth=1.0, 
        #                     label=f'Robot {rid} Raw Min Distance', alpha=0.5)
        
        # 绘制每个机器人的障碍物最近点距离（基于聚类分析）
        for rid in robots_plot:
            robot = robots_plot[rid]
            if robot is not None and robot.get('obstacle_distance') and robot.get('t') and len(robot['obstacle_distance']) == len(robot['t']):
                robot_t = np.array(robot['t'])
                obstacle_distance_data = np.array(robot['obstacle_distance'])
                
                # 过滤无效值和异常大值
                valid_mask = (obstacle_distance_data > 0) & (obstacle_distance_data < 50.0)
                if np.any(valid_mask):
                    valid_times = robot_t[valid_mask]
                    valid_distances = obstacle_distance_data[valid_mask]
                    
                    # 添加简单的移动平均平滑处理，减少跳变
                    if len(valid_distances) > 5:
                        from scipy import ndimage
                        try:
                            # 使用高斯滤波进行平滑
                            smoothed_distances = ndimage.gaussian_filter1d(valid_distances, sigma=2.0)
                            all_distances.extend(smoothed_distances)  # 收集数据用于自适应范围
                            plt.plot(valid_times, smoothed_distances, linewidth=1.5, label=f'Robot {rid} Obstacle Distance', alpha=0.8)
                        except:
                            # 如果scipy不可用，使用原始数据
                            all_distances.extend(valid_distances)
                            plt.plot(valid_times, valid_distances, linewidth=1.5, label=f'Robot {rid} Obstacle Distance', alpha=0.8)
                    else:
                        all_distances.extend(valid_distances)
                        plt.plot(valid_times, valid_distances, linewidth=1.5, label=f'Robot {rid} Obstacle Distance', alpha=0.8)
                else:
                    rospy.logwarn(f"tb3_{rid} 障碍物距离数据无效，跳过绘制")
            else:
                rospy.logwarn(f"tb3_{rid} 障碍物距离数据缺失，跳过绘制")
        
        # 添加安全和避障阈值线
        ord_avoid = 0.35  # 避障阈值
        ord_safe = 0.3    # 安全阈值
        
        plt.axhline(y=ord_safe, color='red', linestyle='--', linewidth=2, 
                   label=f'Safety threshold ({ord_safe}m)', alpha=0.8)
        plt.axhline(y=ord_avoid, color='orange', linestyle=':', linewidth=2, 
                   label=f'Avoidance threshold ({ord_avoid}m)', alpha=0.8)
        
        # 计算自适应纵轴范围
        if all_distances:
            min_distance = min(all_distances)
            max_distance = max(all_distances)
            y_margin = (max_distance - min_distance) * 0.1  # 10%的边距
            y_min = max(0, min_distance - y_margin)  # 下限不小于0
            y_max = max_distance + y_margin
            # 确保能显示阈值线
            y_max = max(y_max, ord_avoid + 0.1)
        else:
            y_min, y_max = 0, 2.0  # 默认范围
        
        plt.xlabel('Time (s)', fontsize=12)
        plt.ylabel('Distance to Closest Obstacle Point (m)', fontsize=12)
        plt.title('Distance to Closest Obstacle Point for Avoidance Calculation', fontsize=14)
        
        # 将图例放在图外右侧，避免遮挡线条
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8, framealpha=0.9)
        plt.grid(True, alpha=0.3)
        plt.ylim([y_min, y_max])  # 使用自适应范围
        set_xaxis_to_show_max(max_time)  # 确保最大值显示
        
        # 保存障碍物最近点距离图
        obstacle_distance_path = os.path.join(self.run_dir, f"obstacle_distance_{self.run_timestamp}.png")
        plt.savefig(obstacle_distance_path, dpi=300, bbox_inches='tight')
        plt.close()

        # -------------------------- 9. 聚类分析结果图 --------------------------
        plt.figure(9, figsize=(12, 6))  # 与其他图保持一致的大小
        
        # 聚类数量时间变化（显示完整时间轴）
        for rid in robots_plot:
            robot = robots_plot[rid]
            if (robot is not None and robot.get('total_clusters_count') 
                and robot.get('t') and len(robot['total_clusters_count']) == len(robot['t'])):
                
                robot_t = np.array(robot['t'])
                total_clusters = np.array(robot['total_clusters_count'])
                
                # 绘制总聚类数量
                plt.plot(robot_t, total_clusters, '-', linewidth=1.5, 
                        label=f'Robot {rid} - Total Clusters', alpha=0.8)
        
        plt.ylim([0, 8])  # 合理的聚类数量范围
        plt.xlabel('Time (s)', fontsize=12)
        plt.ylabel('Number of Clusters', fontsize=12)
        plt.title('Clustering Analysis Results - Total Clusters Over Time', fontsize=14)
        
        # 将图例放在图内右上角
        plt.legend(loc='upper right', fontsize=10, framealpha=0.9)
        plt.grid(True, alpha=0.3)
        set_xaxis_to_show_max(max_time)  # 确保最大值显示
        
        plt.tight_layout()
        
        # 保存聚类分析结果图
        clustering_analysis_path = os.path.join(self.run_dir, f"clustering_analysis_{self.run_timestamp}.png")
        plt.savefig(clustering_analysis_path, dpi=300, bbox_inches='tight')
        plt.close()

        # -------------------------- 10. 避障力图 --------------------------
        plt.figure(10, figsize=(12, 6))
        
        # 提取避障力数据
        for robot_id in range(5):
            if robot_id in robots_plot and robots_plot[robot_id] is not None:
                robot_data = robots_plot[robot_id]
                if 'avoidance_force_magnitude' in robot_data and robot_data['avoidance_force_magnitude']:
                    avoidance_force_mag = np.array(robot_data['avoidance_force_magnitude'], dtype=np.float64)
                    robot_t_array = np.array(robot_data['t'], dtype=np.float64) if robot_data['t'] else np.array([])
                    
                    # 显示整个时间范围的数据
                    if len(robot_t_array) > 0 and len(avoidance_force_mag) > 0:
                        if len(robot_t_array) > 0:
                            plt.plot(robot_t_array, avoidance_force_mag, 
                                   label=f'Robot {robot_id}', linewidth=1.5, alpha=0.8)
        
        plt.xlabel('Time (s)', fontsize=12)
        plt.ylabel('Force Magnitude', fontsize=12)
        title_text = 'Avoidance Forces - Full Timeline' if not USE_CHINESE else '避障力随时间变化 - 完整时间线'
        plt.title(title_text, fontsize=14)
        
        # 图例设置
        plt.legend(loc='upper right', fontsize=8, framealpha=0.9, 
                  ncol=3, columnspacing=1.0, handletextpad=0.5)
        plt.grid(True, alpha=0.3)
        set_xaxis_to_show_max(max_time)  # 确保最大值显示
        plt.tight_layout()
        
        # 保存避障力图
        avoidance_path = os.path.join(self.run_dir, f"avoidance_forces_{self.run_timestamp}.png")
        plt.savefig(avoidance_path, dpi=300, bbox_inches='tight')
        plt.close()

        # -------------------------- 11. 观测器估计效果图 --------------------------
        plt.figure(11, figsize=(14, 8))
        
        # 绘制领导者真实X坐标（深蓝色虚线）
        if leader_plot['t'] and leader_plot['x0']:
            leader_t = np.array(leader_plot['t'])
            leader_x = np.array(leader_plot['x0'])
            plt.plot(leader_t, leader_x, linestyle='--', color='darkblue', linewidth=2.5, 
                    label='x_Leader', alpha=0.9, zorder=10)
        
        # 绘制领导者真实Y坐标（深红色虚线）
        if leader_plot['t'] and leader_plot['y0']:
            leader_t = np.array(leader_plot['t'])
            leader_y = np.array(leader_plot['y0'])
            plt.plot(leader_t, leader_y, linestyle='--', color='darkred', linewidth=2.5, 
                    label='y_Leader', alpha=0.9, zorder=10)
        
        # 绘制5个机器人观测器估计的X和Y坐标（使用更鲜明的颜色）
        colors_obs = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']  # 蓝、橙、绿、红、紫
        
        for i, rid in enumerate(robots_plot):
            robot = robots_plot[rid]
            
            # 跳过空数据
            if robot is None:
                rospy.logwarn(f"机器人{rid}数据为空")
                continue
            
            # 检查观测器数据是否存在
            has_zxeo_x = 'zxeo_x' in robot and robot['zxeo_x'] and len(robot['zxeo_x']) > 0
            has_zxeo_y = 'zxeo_y' in robot and robot['zxeo_y'] and len(robot['zxeo_y']) > 0
            
            if not has_zxeo_x or not has_zxeo_y:
                rospy.logwarn(f"机器人{rid}缺少观测器数据: zxeo_x={has_zxeo_x}, zxeo_y={has_zxeo_y}")
                continue
            
            # 绘制X坐标估计（实线）
            if 't' in robot and len(robot['t']) > 0:
                robot_t = np.array(robot['t'])
                robot_zxeo_x = np.array(robot['zxeo_x'])
                # 确保数据长度一致
                min_len = min(len(robot_t), len(robot_zxeo_x))
                if min_len > 0:
                    plt.plot(robot_t[:min_len], robot_zxeo_x[:min_len], linestyle='-', color=colors_obs[i], 
                            linewidth=1.5, label=f'x_est_{rid}', alpha=0.8)
                    rospy.loginfo(f"✓ 已绘制机器人{rid}的X估计，数据点数: {min_len}")
            
            # 绘制Y坐标估计（点划线）
            if 't' in robot and len(robot['t']) > 0:
                robot_t = np.array(robot['t'])
                robot_zxeo_y = np.array(robot['zxeo_y'])
                # 确保数据长度一致
                min_len = min(len(robot_t), len(robot_zxeo_y))
                if min_len > 0:
                    plt.plot(robot_t[:min_len], robot_zxeo_y[:min_len], linestyle='-.', color=colors_obs[i], 
                            linewidth=1.5, label=f'y_est_{rid}', alpha=0.8)
                    rospy.loginfo(f"✓ 已绘制机器人{rid}的Y估计，数据点数: {min_len}")
        
        plt.xlim(0, max_time)
        plt.xlabel('Trajectory Time (s, from node start)', fontsize=12)
        plt.ylabel('Position (m)', fontsize=12)
        plt.title(f'Observer Estimation Performance - Relative Time ({self.run_timestamp})', fontsize=14)
        plt.legend(loc='upper right', fontsize=7, ncol=3, framealpha=0.9)
        plt.grid(True, alpha=0.3)
        set_xaxis_to_show_max(max_time)
        
        plt.tight_layout()
        
        # 保存观测器估计效果图
        observer_path = os.path.join(self.run_dir, f"observer_estimation_{self.run_timestamp}.png")
        plt.savefig(observer_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        rospy.loginfo("✓ 观测器估计效果图已保存")

        # -------------------------- 12. X和Y跟踪误差图 --------------------------
        plt.figure(12, figsize=(8, 6))
        
        # 绘制每个机器人的X和Y跟踪误差（xr-xc, yr-yc）
        # X方向使用红色，Y方向使用蓝色
        
        for i, rid in enumerate(robots_plot):
            robot = robots_plot[rid]
            
            # 跳过空数据
            if robot is None:
                rospy.logwarn(f"机器人{rid}数据为空")
                continue
            
            # 检查是否有必要的数据（xr, yr, xc, yc, t）
            has_xr = 'xr' in robot and robot['xr'] and len(robot['xr']) > 0
            has_yr = 'yr' in robot and robot['yr'] and len(robot['yr']) > 0
            has_xc = 'xc' in robot and robot['xc'] and len(robot['xc']) > 0
            has_yc = 'yc' in robot and robot['yc'] and len(robot['yc']) > 0
            has_t = 't' in robot and robot['t'] and len(robot['t']) > 0
            
            if not (has_xr and has_yr and has_xc and has_yc and has_t):
                rospy.logwarn(f"机器人{rid}缺少轨迹跟踪数据: xr={has_xr}, yr={has_yr}, xc={has_xc}, yc={has_yc}, t={has_t}")
                continue
            
            # 转换为numpy数组
            robot_t = np.array(robot['t'])
            robot_xr = np.array(robot['xr'])
            robot_yr = np.array(robot['yr'])
            robot_xc = np.array(robot['xc'])
            robot_yc = np.array(robot['yc'])
            
            # 确保数据长度一致
            min_len = min(len(robot_t), len(robot_xr), len(robot_yr), len(robot_xc), len(robot_yc))
            
            if min_len == 0:
                rospy.logwarn(f"机器人{rid}数据长度为0，跳过")
                continue
            
            # 截取一致长度的数据
            robot_t = robot_t[:min_len]
            robot_xr = robot_xr[:min_len]
            robot_yr = robot_yr[:min_len]
            robot_xc = robot_xc[:min_len]
            robot_yc = robot_yc[:min_len]
            
            # 计算跟踪误差：xr - xc, yr - yc
            x_tracking_error = robot_xr - robot_xc
            y_tracking_error = robot_yr - robot_yc
            
            # 绘制X方向跟踪误差（红色实线）
            plt.plot(robot_t, x_tracking_error, linestyle='-', color='red', 
                    linewidth=1.5, label=f'x_error_{rid}', alpha=0.8)
            
            # 绘制Y方向跟踪误差（蓝色实线）
            plt.plot(robot_t, y_tracking_error, linestyle='-', color='blue', 
                    linewidth=1.5, label=f'y_error_{rid}', alpha=0.8)
            
            rospy.loginfo(f"✓ 已绘制机器人{rid}的跟踪误差，数据点数: {min_len}")
        
        # 添加零误差参考线
        plt.axhline(y=0, color='black', linestyle=':', linewidth=1.5, alpha=0.5, label='Zero Error')
        
        plt.xlim(0, max_time)
        plt.xlabel('Trajectory Time (s, from node start)', fontsize=12)
        plt.ylabel('Tracking Error (m)', fontsize=12)
        plt.title(f'X & Y Tracking Error (xr-xc, yr-yc) - Relative Time ({self.run_timestamp})', fontsize=14)
        plt.legend(loc='upper right', fontsize=8, ncol=2, framealpha=0.9)
        plt.grid(True, alpha=0.3)
        set_xaxis_to_show_max(max_time)
        
        plt.tight_layout()
        
        # 保存跟踪误差图
        tracking_error_path = os.path.join(self.run_dir, f"tracking_error_xy_{self.run_timestamp}.png")
        plt.savefig(tracking_error_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        rospy.loginfo("✓ X和Y跟踪误差图已保存")
        
        rospy.loginfo(f"所有图表已保存到子文件夹：{self.run_dir}")
        info_msg = f"本次运行结果汇总：\n1. 数据文件：{pickle_path}\n2. 图表文件：共12张（轨迹、速度、误差、时间分析、障碍物距离、聚类分析、避障力分析、观测器估计、跟踪误差）\n3. 计算时长统计报告将在节点关闭时生成"
        if not USE_CHINESE:
            info_msg = f"Run Results Summary:\n1. Data file: {pickle_path}\n2. Chart files: 12 charts (trajectory, velocity, error, time analysis, obstacle distance, clustering analysis, avoidance forces, observer estimation, tracking error)\n3. Computation statistics report will be generated when node shuts down"
        rospy.loginfo(info_msg)

    def generate_computation_statistics_only(self):
        """仅生成计算时长统计报告（不重复绘制图表）"""
        if not self.robots or all(r is None for r in self.robots.values()):
            rospy.logwarn("没有机器人数据，跳过计算时长分析")
            return
        
        # 🚀 话题优化：数据通过话题自动接收，无需手动获取
        # 原代码：self.fetch_data(None)  # 已移除
        
        # 生成统计摘要
        self.generate_computation_statistics()
        
        rospy.loginfo(f"计算时长统计报告已生成：{self.run_dir}")

    def generate_computation_statistics(self):
        """生成计算时长统计摘要"""
        summary_file = os.path.join(self.run_dir, f"computation_stats_{self.run_timestamp}.txt")
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write("TurtleBot3 分布式控制计算时长分析报告\n")
            f.write("=" * 50 + "\n")
            f.write(f"分析时间：{self.run_timestamp}\n")
            f.write(f"控制周期基准：100ms (0.1s)\n\n")
            
            overall_stats = []
            
            for rid in range(5):
                if self.robots[rid] is None or 'computation_time' not in self.robots[rid]:
                    continue
                    
                comp_times = np.array(self.robots[rid]['computation_time']) * 1000  # 转换为毫秒
                
                if len(comp_times) == 0:
                    continue
                
                # 基本统计
                avg_time = np.mean(comp_times)
                median_time = np.median(comp_times)
                std_time = np.std(comp_times)
                min_time = np.min(comp_times)
                max_comp_time = np.max(comp_times)
                
                # 超时统计
                overruns = np.sum(comp_times > 100)
                overrun_percentage = (overruns / len(comp_times)) * 100
                
                # 性能分级
                if avg_time < 50:
                    performance = "优秀"
                elif avg_time < 80:
                    performance = "良好"
                elif avg_time < 100:
                    performance = "中等"
                else:
                    performance = "需要优化"
                
                overall_stats.append(avg_time)
                
                f.write(f"机器人 tb3_{rid} 统计信息：\n")
                f.write(f"  样本数量：{len(comp_times)}\n")
                f.write(f"  平均时长：{avg_time:.2f} ms\n")
                f.write(f"  中位时长：{median_time:.2f} ms\n")
                f.write(f"  标准差：  {std_time:.2f} ms\n")
                f.write(f"  最小时长：{min_time:.2f} ms\n")
                f.write(f"  最大时长：{max_comp_time:.2f} ms\n")
                f.write(f"  超时次数：{overruns} / {len(comp_times)}\n")
                f.write(f"  超时率：  {overrun_percentage:.1f}%\n")
                f.write(f"  性能评级：{performance}\n")
                f.write("-" * 30 + "\n")
            
            # 系统整体统计
            if overall_stats:
                f.write("系统整体表现：\n")
                f.write(f"  系统平均计算时长：{np.mean(overall_stats):.2f} ms\n")
                f.write(f"  系统最大计算时长：{np.max(overall_stats):.2f} ms\n")
                f.write(f"  系统计算时长差异：{np.std(overall_stats):.2f} ms\n")
                
                if np.max(overall_stats) > 100:
                    f.write("  ⚠️  警告：存在超过控制周期的计算时长\n")
                else:
                    f.write("  ✅ 所有机器人计算时长均在控制周期内\n")


if __name__ == "__main__":
    try:
        rospy.init_node("ros_sim_time_visualizer_with_timestamp")
        visualizer = ResultVisualizer()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
    except Exception as e:
        rospy.logerr(f"节点运行异常：{str(e)}")
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
论文效果图绘制脚本：直线实验！！！

功能：
1. 读取指定的PKL数据文件
2. 绘制适合论文发表的高质量图表
3. 支持自定义图表样式和布局

使用方法：
1. 修改PKL_FILE_PATH为你要分析的pkl文件路径
2. 运行脚本: python3 paper_plot.py
3. 生成的图表保存在当前目录的output文件夹中

作者：分布式控制系统
日期：2025-12-22
"""

import pickle
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Circle, Rectangle, ConnectionPatch
from matplotlib.lines import Line2D
import os
from datetime import datetime

# ==================== 配置区域 ====================
# 修改这里指定要读取的PKL文件路径
# 支持三种路径格式：
# 1. 相对于脚本的路径: "./8字形一致性编队仿真及避障实验数据/consensus_data_xxx.pkl"
# 2. 相对于上级目录: "../data_collect/2025-12-22-xxx/consensus_data_xxx.pkl"
# 3. 绝对路径: "/home/gdut/完整路径/consensus_data_xxx.pkl"
# PKL_FILE_PATH = "./8字形一致性编队及避障实验数据（实物：直线+S形）/line/consensus_data_2026-04-15-16-10-07.pkl"
PKL_FILE_PATH = "./8字形一致性编队及避障实验数据（实物：直线+S形）/S/consensus_data_2026-04-21-17-35-21.pkl"




# 障碍物配置（根据实验场景选择）
OBSTACLE_MODE = 'experiment_s'  # 'none', 'simple', 'experiment', 'experiment_line', 'experiment_s'

# 图表样式配置
PAPER_STYLE = {
    # ==================== 画布尺寸设置 ====================
    # 双栏论文单栏宽度通常约 3.5 英寸，适合插入LaTeX文档
    'figure_size_single': (3.05, 1.95),      # 单图尺寸：宽3.05寸，高1.95寸
    'figure_size_trajectory': (4.0, 4.0),  # 轨迹图尺寸：稍微高一点便于显示完整轨迹
    
    # ==================== 字体大小设置 ====================
    'font_size': 9,       # 正文字体大小：9pt（坐标轴标签）
    'label_size': 8,       # 刻度标签字体：8pt（比正文小，更精细）
    'legend_size': 8,     # 图例字体大小：8pt（更清晰易读）
        # ==================== 图例样式设置 ====================
    'legend_handlelength': 1.8,    # 图例示例线条长度（默认2.0，越小越紧凑）
    'legend_handletextpad': 0.2,   # 图例标记与文字间距
    'legend_columnspacing': 0.4,   # 图例列间距
    'legend_labelspacing': 0.2,    # 图例行间距
    'legend_borderpad': 0.2,       # 图例框边缘空白
        # ==================== 线条粗细设置 ====================
    'line_width': 1.0,         # 普通数据线宽度：1.0pt（清晰不模糊）
    'line_width_thick': 1.0,   # 强调线宽度：1.0pt（质心轨迹、领导者等）
    
    # ==================== 输出质量设置 ====================
    'dpi': 600,            # 分辨率：600DPI（打印级质量）
    'use_grid': True,      # 是否显示网格：True显示，False隐藏
    'use_latex': False,    # LaTeX渲染：True需安装LaTeX，False使用STIX字体
    
    # ==================== 时间轴设置 ====================
    'time_tick_interval': 8,  # 时间轴刻度间隔（秒）
}

# Inset bounds config for observer estimation error plots.
# Each tuple is: (x_min, x_max, y_min, y_max)
OBSERVER_ERROR_X_INSET_BOUNDS = (0.0, 5.0, -0.1, 0.4)
OBSERVER_ERROR_Y_INSET_BOUNDS = (0.0, 5.0, -0.1, 0.1)

# 输出文件夹
OUTPUT_DIR = "./output_redraw_results/praph"
# ==================================================


class PaperPlotter:
    """论文图表绘制器"""
    
    def __init__(self, pkl_file_path):
        """初始化绘图器"""
        # 获取脚本所在目录
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # 展开路径中的~符号
        pkl_file_path = os.path.expanduser(pkl_file_path)
        
        # 如果是相对路径，则基于脚本目录解析
        if not os.path.isabs(pkl_file_path):
            self.pkl_file = os.path.abspath(os.path.join(script_dir, pkl_file_path))
        else:
            self.pkl_file = os.path.abspath(pkl_file_path)
        
        self.data = None
        
        # 输出目录也基于脚本目录
        output_dir = os.path.expanduser(OUTPUT_DIR)
        if not os.path.isabs(output_dir):
            self.output_dir = os.path.abspath(os.path.join(script_dir, output_dir))
        else:
            self.output_dir = os.path.abspath(output_dir)
        
        # 创建输出目录
        os.makedirs(self.output_dir, exist_ok=True)
        
        # 配置matplotlib样式
        self._configure_matplotlib()
        
        # 加载数据
        self._load_data()
        
    def _configure_matplotlib(self):
        """配置matplotlib样式以适合论文"""
        # 强制使用衬线字体 (Times New Roman 风格)
        config = {
            # ==================== 字体配置 ====================
            "font.family": "serif",  # 字体族：serif衬线字体（学术风格）
            "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],  # 优先字体列表
            "font.size": PAPER_STYLE['font_size'],           # 默认字体大小
            "axes.labelsize": PAPER_STYLE['font_size'],      # 坐标轴标签字体大小
            "xtick.labelsize": PAPER_STYLE['label_size'],    # X轴刻度标签字体大小
            "ytick.labelsize": PAPER_STYLE['label_size'],    # Y轴刻度标签字体大小
            "legend.fontsize": PAPER_STYLE['legend_size'],   # 图例字体大小
            
            # ==================== 线条粗细配置 ====================
            "axes.linewidth": 0.6,                          # 坐标轴边框线宽：0.6pt（精细）
            "grid.linewidth": 0.5,                          # 网格线宽：0.5pt（更精细）
            "lines.linewidth": PAPER_STYLE['line_width'],   # 默认数据线宽
            "xtick.major.width": 0.5,                       # X轴刻度线粗细：0.5pt（比坐标轴细）
            "ytick.major.width": 0.5,                       # Y轴刻度线粗细：0.5pt（比坐标轴细）
            
            # ==================== 刻度线设置 ====================
            "xtick.major.size": 2.0,                        # X轴刻度线长度：2pt
            "ytick.major.size": 2.0,                        # Y轴刻度线长度：2pt
            "xtick.direction": "in",                        # X轴刻度方向：朝内
            "ytick.direction": "in",                        # Y轴刻度方向：朝内
            "xtick.top": True,                              # 显示顶部X轴刻度
            "ytick.right": True,                            # 显示右侧Y轴刻度
            
            # ==================== 数学公式字体 ====================
            "mathtext.fontset": "stix",                     # 数学字体：STIX（类LaTeX效果）
            
            # ==================== 图例边框设置 ====================
            "legend.framealpha": 1.0,                       # 图例背景透明度：完全不透明
            "legend.edgecolor": "black",                     # 图例边框颜色：黑色
            "legend.fancybox": False,                        # 图例边框样式：方形
            "patch.linewidth": 0.6,                         # 补丁边框线宽：0.6pt（图例边框）
        }
        plt.rcParams.update(config)
        
    def _load_data(self):
        """加载PKL数据文件"""
        if not os.path.exists(self.pkl_file):
            raise FileNotFoundError(f"PKL文件不存在: {self.pkl_file}")
        
        with open(self.pkl_file, 'rb') as f:
            self.data = pickle.load(f)
        
        print(f"✅ 成功加载数据文件: {self.pkl_file}")
        print(f"   运行时间: {self.data['run_time']}")
        print(f"   数据来源: {self.data['time_source']}")
    
    def _get_obstacles(self):
        """获取障碍物配置"""
        # 优先从数据文件中读取障碍物信息
        if 'obstacles' in self.data and self.data['obstacles']:
            return self.data['obstacles']
        
        # 如果数据文件中没有，则使用配置的模式
        if OBSTACLE_MODE == 'experiment':
            return [
                {'type': 'circle', 'pos': [0.0, 2.0], 'radius': 0.12, 'color': 'red', 'alpha': 1.0},
                {'type': 'rectangle', 'pos': [0.93, 1.5], 'size': [0.36, 0.36], 'rotation': 0, 'color': 'red', 'alpha': 1.0},
                {'type': 'rectangle', 'pos': [2.15, 1.6], 'size': [0.36, 0.36], 'rotation': 0, 'color': 'red', 'alpha': 1.0},
                {'type': 'rectangle', 'pos': [3.5, 0.5], 'size': [0.36, 0.36], 'rotation': 0, 'color': 'red', 'alpha': 1.0}
            ]
        elif OBSTACLE_MODE == 'simple':
            return [
                {'type': 'circle', 'pos': [1.7, 0.0], 'radius': 0.3, 'color': 'red', 'alpha': 1.0},
                {'type': 'circle', 'pos': [-3.0, 2.0], 'radius': 0.4, 'color': 'red', 'alpha': 1.0},
                {'type': 'rectangle', 'pos': [1.0, -1.5], 'size': [1.0, 0.8], 'rotation': 22.5, 'color': 'red', 'alpha': 1.0},
                {'type': 'circle', 'pos': [0.5, 2.6], 'radius': 0.15, 'color': 'red', 'alpha': 1.0}
            ]
        elif OBSTACLE_MODE == 'experiment_line':
            return [
                # 对齐 world: fhk_xie_line_real_consensus_obstacle.world
                {'type': 'circle', 'pos': [0.9, 1.1], 'radius': 0.12, 'color': 'blue', 'alpha': 1.0},
                {'type': 'rectangle', 'pos': [1.0, 2.4], 'size': [0.36, 0.36], 'rotation': 0, 'color': 'green', 'alpha': 1.0},
                {'type': 'rectangle', 'pos': [2.4, 1.7], 'size': [0.36, 0.36], 'rotation': 0, 'color': 'green', 'alpha': 1.0}
            ]
        elif OBSTACLE_MODE == 'experiment_s':
            return [
                # 对齐 world: fhk_s_improve_real_consensus_obstacle_real_experiment.world
                {'type': 'circle', 'pos': [1.05, 0.12], 'radius': 0.12, 'color': 'blue', 'alpha': 1.0},
                {'type': 'rectangle', 'pos': [3.56, 1.62], 'size': [0.36, 0.36], 'rotation': 45.0, 'color': 'green', 'alpha': 1.0},
                {'type': 'rectangle', 'pos': [1.8, 2.1], 'size': [0.36, 0.36], 'rotation': 0, 'color': 'green', 'alpha': 1.0},
                {'type': 'rectangle', 'pos': [-0.1, 2.1], 'size': [0.36, 0.36], 'rotation': 0, 'color': 'green', 'alpha': 1.0}
            ]
        else:
            return []
    
    def _draw_obstacles(self, ax):
        """在图表上绘制障碍物"""
        obstacles = self._get_obstacles()
        for obs in obstacles:
            color = obs.get('color', 'red')
            alpha = obs.get('alpha', 1.0)
            if obs['type'] == 'circle':
                circle = Circle(obs['pos'], obs['radius'], 
                              color=color, alpha=alpha, zorder=1, linewidth=0)
                ax.add_patch(circle)
            elif obs['type'] == 'rectangle':
                pos = obs['pos']
                size = obs['size']
                rotation = obs.get('rotation', 0)
                adjusted_pos = [pos[0] - size[0]/2, pos[1] - size[1]/2]
                rect = Rectangle(adjusted_pos, size[0], size[1],
                               color=color, alpha=alpha, zorder=1, linewidth=0)
                if rotation != 0:
                    import matplotlib.transforms as transforms
                    t = transforms.Affine2D().rotate_deg_around(pos[0], pos[1], rotation) + ax.transData
                    rect.set_transform(t)
                ax.add_patch(rect)
    
    def _common_plot_setup(self, ax, xlabel, ylabel, legend_loc='best'):
        """通用图表设置"""
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        if PAPER_STYLE['use_grid']:
            ax.grid(True, linestyle='-', alpha=0.3)  # 网格线：实线，透明度30%
        # 图例样式设置：半透明背景，无花哨边框，黑色边框
        ax.legend(loc=legend_loc, framealpha=0.5, fancybox=False, edgecolor='black',
                 handletextpad=PAPER_STYLE['legend_handletextpad'], 
                 columnspacing=PAPER_STYLE['legend_columnspacing'], 
                 labelspacing=PAPER_STYLE['legend_labelspacing'], 
                 borderpad=PAPER_STYLE['legend_borderpad'], 
                 handlelength=PAPER_STYLE['legend_handlelength'])
    
    def _setup_time_axis(self, ax, all_times):
        """
        统一设置时间轴范围和刻度
        
        Args:
            ax: matplotlib轴对象
            all_times: 所有时间数据的列表
        """
        if not all_times:
            return
        
        max_time = float(np.nanmax(np.asarray(all_times, dtype=float)))
        if (not np.isfinite(max_time)) or (max_time <= 0.0):
            ax.set_xlim(0.0, 1.0)
            ax.set_xticks([0, 0, 1, 1])
            ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: f'{int(np.floor(x + 0.5))}'))
            return

        # 统一要求：0到最大时间，5个等间距刻度（包含最大刻度）
        # 即：除0和最大刻度外，中间再等分3个刻度值
        max_tick = int(np.floor(max_time + 0.5))
        max_tick = max(1, max_tick)
        ax.set_xlim(0.0, float(max_tick))

        tick_vals = np.linspace(0.0, float(max_tick), 5)
        tick_ints = [int(np.floor(v + 0.5)) for v in tick_vals]
        ax.set_xticks(tick_ints)
        ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: f'{int(np.floor(x + 0.5))}'))

    def _interp_robot_xy_at_time(self, robot, target_time, max_time_gap=0.25):
        """在统一目标时刻插值机器人位置，确保编队连线来自同一时刻数据。"""
        if (robot is None) or ('t' not in robot) or ('xc' not in robot) or ('yc' not in robot):
            return None

        t_raw = np.asarray(robot['t'], dtype=float)
        x_raw = np.asarray(robot['xc'], dtype=float)
        y_raw = np.asarray(robot['yc'], dtype=float)

        n = min(len(t_raw), len(x_raw), len(y_raw))
        if n < 2:
            return None

        t = t_raw[:n]
        x = x_raw[:n]
        y = y_raw[:n]

        valid = np.isfinite(t) & np.isfinite(x) & np.isfinite(y)
        t = t[valid]
        x = x[valid]
        y = y[valid]
        if t.size < 2:
            return None

        order = np.argsort(t)
        t = t[order]
        x = x[order]
        y = y[order]

        t_unique, unique_idx = np.unique(t, return_index=True)
        x_unique = x[unique_idx]
        y_unique = y[unique_idx]
        if t_unique.size < 2:
            return None

        if (target_time < t_unique[0]) or (target_time > t_unique[-1]):
            return None

        closest_gap = float(np.min(np.abs(t_unique - target_time)))
        if closest_gap > max_time_gap:
            return None

        x_interp = float(np.interp(target_time, t_unique, x_unique))
        y_interp = float(np.interp(target_time, t_unique, y_unique))
        return (x_interp, y_interp)
    
    def plot_trajectory(self, show_ideal=True, show_formation_lines=True):
        """
        绘制编队轨迹图（论文主图）
        
        Args:
            show_ideal: 是否显示理想轨迹
            show_formation_lines: 是否显示编队连线
        """
        # 使用专门的轨迹图尺寸
        fig, ax = plt.subplots(figsize=PAPER_STYLE['figure_size_trajectory'])
        
        leader = self.data['leader']
        robots = self.data['robots']
        
        # 绘制障碍物 (放在最底层)
        self._draw_obstacles(ax)
        
        # 绘制领导者轨迹（深红色虚线）
        ax.plot(leader['x0'], leader['y0'], color='darkred', linestyle='--', 
               linewidth=0.6,  # 细线宽0.6pt
               label=r'$Robot_L$', alpha=1.0, zorder=6)  # 完全不透明，层级6
        
        # 定义颜色方案
        colors = ['#1f77b4', '#ff7f0e', '#ffcc00', '#9467bd', '#2ca02c']
        
        # 绘制机器人轨迹
        for i in range(5):
            robot = robots[i]
            
            if robot:
                # 实际轨迹（实线）
                ax.plot(robot['xc'], robot['yc'], 
                       color=colors[i], linewidth=PAPER_STYLE['line_width'],  # 标准线宽1.0pt
                       label=r'$Robot_{{{}}}$'.format(i+1), alpha=1.0, zorder=4)  # 完全不透明，最高层级
                
                # # 理想轨迹（虚线，已注释）
                # if show_ideal and robot.get('xr') and robot.get('yr'):
                #     ax.plot(robot['xr'], robot['yr'], 
                #            color=colors[i], linestyle='--', linewidth=PAPER_STYLE['line_width'], 
                #            alpha=0.5, zorder=2)  # 透明度50%，层级2（背景）
        
        # 绘制编队中心线（所有机器人位置的几何中心）
        if 'formation_centroid' in self.data and self.data['formation_centroid'] is not None:
            # 从数据文件中直接读取已计算的中心线
            centroid = self.data['formation_centroid']
            if 'xc' in centroid and 'yc' in centroid:
                ax.plot(centroid['xc'], centroid['yc'], 
                       color='deepskyblue', linewidth=0.6,  # 细线宽0.6pt
                       label=r'$Centroid$', alpha=1.0, zorder=5)  # 完全不透明，层级5
        else:
            # 如果数据文件中没有，则实时计算中心线
            robot_x_arrays = []
            robot_y_arrays = []
            for i in range(5):
                if robots[i]:
                    robot_x_arrays.append(np.array(robots[i]['xc']))
                    robot_y_arrays.append(np.array(robots[i]['yc']))
            
            if len(robot_x_arrays) > 0:
                # 计算所有机器人的平均位置作为编队中心
                min_length = min(len(arr) for arr in robot_x_arrays)
                robot_x_trunc = [arr[:min_length] for arr in robot_x_arrays]
                robot_y_trunc = [arr[:min_length] for arr in robot_y_arrays]
                
                centroid_x = np.mean(robot_x_trunc, axis=0)
                centroid_y = np.mean(robot_y_trunc, axis=0)
                
                ax.plot(centroid_x, centroid_y, 
                       color='deepskyblue', linewidth=0.6,  # 细线宽0.6pt
                       label=r'$Centroid$', alpha=1.0, zorder=5)  # 完全不透明，层级5
        
        # 绘制编队连线（在特定时刻）
        if show_formation_lines:
            leader_t = np.array(leader['t'])
            # 使用共同可用末时刻，避免ceil导致目标时刻超出机器人最后采样点
            available_ends = [float(leader_t[-1])]
            for rid in range(5):
                robot = robots[rid]
                if robot and ('t' in robot) and (len(robot['t']) > 0):
                    available_ends.append(float(np.asarray(robot['t'], dtype=float)[-1]))
            max_time = min(available_ends) if available_ends else float(leader_t[-1])
            
            if OBSTACLE_MODE == 'experiment':
                time_nodes = [30.0, 60.0, 90.0, max_time]
            elif OBSTACLE_MODE == 'experiment_line':
                time_nodes = [5.0, max_time]
            elif OBSTACLE_MODE == 'experiment_s':
                time_nodes = [17.8, 36.0, 55.0, max_time]
                #  time_nodes = [17.8, 55.0, max_time]
            else:
                time_nodes = np.linspace(30.0, max_time, 6)
            
            for i, target_time in enumerate(time_nodes):
                positions = []
                for rid in range(5):
                    pos = self._interp_robot_xy_at_time(robots[rid], float(target_time), max_time_gap=0.25)
                    if pos is not None:
                        positions.append(pos)
                
                if len(positions) == 5:
                    x_coords = [pos[0] for pos in positions]
                    y_coords = [pos[1] for pos in positions]
                    polygon_x = x_coords + [x_coords[0]]
                    polygon_y = y_coords + [y_coords[0]]
                    
                          # 编队连线：细线，灰色，最高层级
                    ax.plot(polygon_x, polygon_y, color=[0.4, 0.5, 0.6],  # RGB灰色值
                              linewidth=1.0, zorder=7)  # 细线1.0pt，最高层级（前景）
        
        # ==================== 图表布局设置 ====================
        ax.set_xlabel('X coordinate (m)')  # X轴标签
        ax.set_ylabel('Y coordinate (m)', fontsize=9)  # Y轴标签
        
        # 图例设置：黑色边框、50%透明背景、与坐标轴线宽一致
        legend = ax.legend(loc='upper left', framealpha=0.5, fancybox=False, edgecolor='black',
                 handletextpad=PAPER_STYLE['legend_handletextpad'], 
                 columnspacing=PAPER_STYLE['legend_columnspacing'], 
                 labelspacing=PAPER_STYLE['legend_labelspacing'], 
                 borderpad=PAPER_STYLE['legend_borderpad'], 
                 handlelength=PAPER_STYLE['legend_handlelength'])
        
        # 修改图例中线条的宽度（保持正常粗细1.0pt，不受实际绘图线宽影响）
        for line in legend.get_lines():
            line.set_linewidth(1.0)
        
        # 添加网格线
        if PAPER_STYLE['use_grid']:
            ax.grid(True, linestyle='-', alpha=0.3)
        
        # 坐标轴比例：保持X-Y等比例显示（重要！避免轨迹变形）
        # 不再手动设置x/y范围，使用数据自适应缩放
        ax.set_aspect('equal', adjustable='box')
        plt.tight_layout()  # 自动调整布局，避免标签被裁剪
        
        # 保存
        output_file = os.path.join(self.output_dir, 'trajectory.png')
        plt.savefig(output_file, dpi=PAPER_STYLE['dpi'], bbox_inches='tight')
        print(f"✅ 轨迹图已保存: {output_file}")
        plt.close()
    
    def plot_x_error(self):
        """绘制X方向跟踪误差图"""
        fig, ax = plt.subplots(figsize=PAPER_STYLE['figure_size_single'])
        
        robots = self.data['robots']
        colors = ['#1f77b4', '#ff7f0e', '#ffcc00', '#9467bd', '#2ca02c']
        
        for i in range(5):
            robot = robots[i]
            if robot:
                t = np.array(robot['t'])
                xe = np.array(robot['xe'])
                
                ax.plot(t, xe, color=colors[i], linewidth=PAPER_STYLE['line_width'], 
                       label=f'$\mathit{{Robot}}_{{{i+1}}}$', alpha=1.0)
        
        # 设置x轴范围
        all_times = []
        for i in range(5):
            if robots[i]:
                all_times.extend(robots[i]['t'])
        # 统一设置时间轴
        self._setup_time_axis(ax, all_times)
        
        ax.set_xlabel('Time(s)', fontsize=PAPER_STYLE['font_size'])
        ax.set_ylabel('$x_i - x_L - p_{ix}^d$ (m)', fontsize=9)
        ax.set_ylim(-1, 1)
        # 设置y轴刻度为0.5间隔
        import matplotlib.ticker as ticker
        ax.yaxis.set_major_locator(ticker.MultipleLocator(0.5))
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f'{x:g}'))
        ax.legend(loc='lower right', framealpha=0.5, fancybox=False, edgecolor='black',
                 handletextpad=PAPER_STYLE['legend_handletextpad'], 
                 columnspacing=PAPER_STYLE['legend_columnspacing'], 
                 labelspacing=PAPER_STYLE['legend_labelspacing'], 
                 borderpad=PAPER_STYLE['legend_borderpad'], 
                 handlelength=PAPER_STYLE['legend_handlelength'], 
                 ncol=2)
        
        if PAPER_STYLE['use_grid']:
            ax.grid(True, linestyle='-', alpha=0.3)
        
        plt.tight_layout()
        
        output_file = os.path.join(self.output_dir, 'x_error.png')
        plt.savefig(output_file, dpi=PAPER_STYLE['dpi'], bbox_inches='tight')
        print(f"✅ X方向误差图已保存: {output_file}")
        plt.close()
    
    def plot_y_error(self):
        """绘制Y方向跟踪误差图"""
        fig, ax = plt.subplots(figsize=PAPER_STYLE['figure_size_single'])
        
        robots = self.data['robots']
        colors = ['#1f77b4', '#ff7f0e', '#ffcc00', '#9467bd', '#2ca02c']
        
        robot_plot_order = [4, 0, 1, 2, 3]  # Robot_5先画，放在最底层
        for i in robot_plot_order:
            robot = robots[i]
            if robot:
                t = np.array(robot['t'])
                ye = np.array(robot['ye'])

                line_zorder = 2 if i == 4 else 4
                ax.plot(t, ye, color=colors[i], linewidth=PAPER_STYLE['line_width'], 
                       label=f'$\mathit{{Robot}}_{{{i+1}}}$', alpha=1.0, zorder=line_zorder)
        
        # 设置x轴范围
        all_times = []
        for i in range(5):
            if robots[i]:
                all_times.extend(robots[i]['t'])
        # 统一设置时间轴
        self._setup_time_axis(ax, all_times)
        
        ax.set_xlabel('Time(s)', fontsize=PAPER_STYLE['font_size'])
        ax.set_ylabel('$y_i - y_L - p_{iy}^d$ (m)', fontsize=9)
        ax.set_ylim(-1, 1)
        # 设置y轴刻度为0.5间隔
        import matplotlib.ticker as ticker
        ax.yaxis.set_major_locator(ticker.MultipleLocator(0.5))
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f'{x:g}'))
        ax.legend(loc='lower right', framealpha=0.5, fancybox=False, edgecolor='black',
                 handletextpad=PAPER_STYLE['legend_handletextpad'], 
                 columnspacing=PAPER_STYLE['legend_columnspacing'], 
                 labelspacing=PAPER_STYLE['legend_labelspacing'], 
                 borderpad=PAPER_STYLE['legend_borderpad'], 
                 handlelength=PAPER_STYLE['legend_handlelength'], 
                 ncol=2)
        
        if PAPER_STYLE['use_grid']:
            ax.grid(True, linestyle='-', alpha=0.3)
        
        plt.tight_layout()
        
        output_file = os.path.join(self.output_dir, 'y_error.png')
        plt.savefig(output_file, dpi=PAPER_STYLE['dpi'], bbox_inches='tight')
        print(f"✅ Y方向误差图已保存: {output_file}")
        plt.close()
    
    def plot_tracking_errors(self):
        """绘制跟踪误差图（X和Y方向）- 已废弃，保留用于兼容"""
        self.plot_x_error()
        self.plot_y_error()

    def plot_cpl_control_inputs(self):
        """分别绘制CPL控制输入图（x方向与y方向）"""
        robots = self.data['robots']
        colors = ['#1f77b4', '#ff7f0e', '#ffcc00', '#9467bd', '#2ca02c']

        # 与主控制节点保持一致：固定采样时间t1=0.1s
        t1 = 0.1
        initial_positions = [
            # 实物直线位置
            # 虚拟领导者位置(-0.15, 0.15 )
            [0.20, 0.00],
            [-0.30, 0.50],
            [-0.50, 1.00],
            [-0.50, 0.00],
            [0.20, -0.30]
        ]

        all_times = []
        cpl_inputs = {}
        for i in range(5):
            robot = robots[i]
            if not robot or ('t' not in robot) or ('xr' not in robot) or ('yr' not in robot):
                continue

            t = np.array(robot['t'])
            xr = np.array(robot['xr'])
            yr = np.array(robot['yr'])
            min_len = min(len(t), len(xr), len(yr))
            if min_len <= 0:
                continue

            t = t[:min_len]
            xr = xr[:min_len]
            yr = yr[:min_len]

            ux = np.zeros(min_len)
            uy = np.zeros(min_len)

            # 第一个采样点使用初始参考位置补算
            ux[0] = (xr[0] - initial_positions[i][0]) / t1
            uy[0] = (yr[0] - initial_positions[i][1]) / t1
            if min_len > 1:
                ux[1:] = np.diff(xr) / t1
                uy[1:] = np.diff(yr) / t1

            cpl_inputs[i] = {'t': t, 'ux': ux, 'uy': uy}
            all_times.extend(t.tolist())

        def _plot_single_direction(value_key, ylabel, output_name):
            fig, ax = plt.subplots(figsize=PAPER_STYLE['figure_size_single'])

            if value_key == 'uy':
                robot_plot_order = [4, 0, 1, 2, 3]  # 仅uy图将Robot_5放在最底层
            else:
                robot_plot_order = [0, 1, 2, 3, 4]

            for i in robot_plot_order:
                if i not in cpl_inputs:
                    continue
                t = cpl_inputs[i]['t']
                values = cpl_inputs[i][value_key]
                line_zorder = 2 if (value_key == 'uy' and i == 4) else 4
                ax.plot(t, values, color=colors[i], linewidth=PAPER_STYLE['line_width'],
                        linestyle='-', label=f'$\\mathit{{Robot}}_{{{i+1}}}$', alpha=1.0, zorder=line_zorder)

            self._setup_time_axis(ax, all_times)

            ax.set_xlabel('Time(s)', fontsize=PAPER_STYLE['font_size'])
            ax.set_ylabel(ylabel, fontsize=9)
            ax.set_ylim(-1, 1)

            import matplotlib.ticker as ticker
            ax.yaxis.set_major_locator(ticker.MultipleLocator(0.5))
            ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f'{x:g}'))
            ax.legend(loc='upper right', framealpha=0.5, fancybox=False, edgecolor='black',
                     handletextpad=PAPER_STYLE['legend_handletextpad'],
                     columnspacing=PAPER_STYLE['legend_columnspacing'],
                     labelspacing=PAPER_STYLE['legend_labelspacing'],
                     borderpad=PAPER_STYLE['legend_borderpad'],
                     handlelength=PAPER_STYLE['legend_handlelength'],
                     ncol=2)

            if PAPER_STYLE['use_grid']:
                ax.grid(True, linestyle='-', alpha=0.3)

            plt.tight_layout()

            output_file = os.path.join(self.output_dir, output_name)
            plt.savefig(output_file, dpi=PAPER_STYLE['dpi'], bbox_inches='tight')
            print(f"✅ CPL控制输入图已保存: {output_file}")
            plt.close()

        _plot_single_direction('ux', '$u_{xi}$ of CPL', 'cpl_control_input_x.png')
        _plot_single_direction('uy', '$u_{yi}$ of CPL', 'cpl_control_input_y.png')
    
    def plot_linear_velocity(self):
        """绘制线速度图"""
        fig, ax = plt.subplots(figsize=PAPER_STYLE['figure_size_single'])
        
        leader = self.data['leader']
        robots = self.data['robots']
        colors = ['#1f77b4', '#ff7f0e', '#ffcc00', '#9467bd', '#2ca02c']
        
        # 领导者速度
        leader_t = np.array(leader['t'])
        ax.plot(leader_t, leader['v0'], 'k--', linewidth=PAPER_STYLE['line_width_thick'], 
                label='$v_L$', alpha=0.8)
        
        # 机器人速度
        for i in range(5):
            robot = robots[i]
            if robot:
                t = np.array(robot['t'])
                ax.plot(t, robot['vc'], color=colors[i], linewidth=PAPER_STYLE['line_width'], 
                        label='$v_{{{}}}$'.format(i+1), alpha=1.0)
        
        ax.set_xlabel('Time(s)', fontsize=PAPER_STYLE['font_size'])
        ax.set_ylabel('Linear velocities (m/s)', fontsize=9)
        # ax.set_ylim(-0.4, 0.4)  # 设置Y轴范围：-0.4到+0.4
        ax.set_ylim(-1.0, 1.0)  # 设置Y轴范围：-1.0到+1.0
        # 设置y轴刻度为0.5间隔
        import matplotlib.ticker as ticker
        ax.yaxis.set_major_locator(ticker.MultipleLocator(0.5))
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f'{x:g}'))
        ax.legend(loc='lower right', framealpha=0.5, fancybox=False, edgecolor='black',
                 handletextpad=PAPER_STYLE['legend_handletextpad'], columnspacing=PAPER_STYLE['legend_columnspacing'], labelspacing=PAPER_STYLE['legend_labelspacing'], borderpad=PAPER_STYLE['legend_borderpad'], handlelength=PAPER_STYLE['legend_handlelength'], ncol=2)
        
        # 设置x轴范围和标签
        all_times = list(leader_t)
        for i in range(5):
            if robots[i]:
                all_times.extend(robots[i]['t'])
        # 统一设置时间轴
        self._setup_time_axis(ax, all_times)
        
        if PAPER_STYLE['use_grid']:
            ax.grid(True, linestyle="-", alpha=0.3)
        
        plt.tight_layout()
        
        output_file = os.path.join(self.output_dir, 'linear_velocity.png')
        plt.savefig(output_file, dpi=PAPER_STYLE['dpi'], bbox_inches='tight')
        print(f"✅ 线速度图已保存: {output_file}")
        plt.close()
    
    def plot_angular_velocity(self):
        """绘制角速度图"""
        fig, ax = plt.subplots(figsize=PAPER_STYLE['figure_size_single'])
        
        leader = self.data['leader']
        robots = self.data['robots']
        colors = ['#1f77b4', '#ff7f0e', '#ffcc00', '#9467bd', '#2ca02c']
        
        # 领导者速度
        leader_t = np.array(leader['t'])
        ax.plot(leader_t, leader['w0'], 'k--', linewidth=PAPER_STYLE['line_width_thick'], 
                label='$\omega_L$', alpha=0.8)
        
        # 机器人速度
        # 论文多线图常见做法：先画“希望在底层”的曲线，再画其余曲线，并显式指定zorder
        robot_plot_order = [4, 0, 1, 2, 3]  # Robot_5先画，放在最底层
        for i in robot_plot_order:
            robot = robots[i]
            if robot:
                t = np.array(robot['t'])
                line_zorder = 2 if i == 4 else 4
                ax.plot(t, robot['wc'], color=colors[i], linewidth=PAPER_STYLE['line_width'], 
                        label='$\omega_{{{}}}$'.format(i+1), alpha=1.0, zorder=line_zorder)
        
        ax.set_xlabel('Time(s)', fontsize=PAPER_STYLE['font_size'])
        ax.set_ylabel('Angular velocities (rad/s)', fontsize=9)
        ax.set_ylim(-4, 4)  # 设置Y轴范围：-4到+4
        # 设置y轴刻度为2间隔
        import matplotlib.ticker as ticker
        ax.yaxis.set_major_locator(ticker.MultipleLocator(2))
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f'{x:g}'))
        handles, labels = ax.get_legend_handles_labels()
        legend_order = ['$\\omega_L$', '$\\omega_{1}$', '$\\omega_{2}$', '$\\omega_{3}$', '$\\omega_{4}$', '$\\omega_{5}$']
        ordered_handles = []
        ordered_labels = []
        for name in legend_order:
            if name in labels:
                idx = labels.index(name)
                ordered_handles.append(handles[idx])
                ordered_labels.append(name)

        ax.legend(ordered_handles, ordered_labels,
                 loc='upper right', framealpha=0.5, fancybox=False, edgecolor='black',
                 handletextpad=PAPER_STYLE['legend_handletextpad'], columnspacing=PAPER_STYLE['legend_columnspacing'], labelspacing=PAPER_STYLE['legend_labelspacing'], borderpad=PAPER_STYLE['legend_borderpad'], handlelength=PAPER_STYLE['legend_handlelength'], ncol=2)
        
        # 设置x轴范围和标签
        all_times = list(leader_t)
        for i in range(5):
            if robots[i]:
                all_times.extend(robots[i]['t'])
        # 统一设置时间轴
        self._setup_time_axis(ax, all_times)
        
        if PAPER_STYLE['use_grid']:
            ax.grid(True, linestyle="-", alpha=0.3)
        
        plt.tight_layout()
        
        output_file = os.path.join(self.output_dir, 'angular_velocity.png')
        plt.savefig(output_file, dpi=PAPER_STYLE['dpi'], bbox_inches='tight')
        print(f"✅ 角速度图已保存: {output_file}")
        plt.close()
    
    def plot_velocities(self):
        """绘制速度对比图 - 已废弃，保留用于兼容"""
        self.plot_linear_velocity()
        self.plot_angular_velocity()
    
    def plot_obstacle_distance(self):
        """绘制障碍物距离图"""
        fig, ax = plt.subplots(figsize=PAPER_STYLE['figure_size_single'])
        
        robots = self.data['robots']
        colors = ['#1f77b4', '#ff7f0e', '#ffcc00', '#9467bd', '#2ca02c']
        
        for i in range(5):
            robot = robots[i]
            if robot and robot.get('obstacle_distance'):
                t = np.array(robot['t'])
                dist = np.array(robot['obstacle_distance'])
                
                # 过滤无效值
                valid_mask = (dist > 0) & (dist < 50.0)
                if np.any(valid_mask):
                    ax.plot(t[valid_mask], dist[valid_mask], 
                           color=colors[i], linewidth=PAPER_STYLE['line_width'], 
                           label=f'$Robot_{{{i+1}}}$', alpha=1.0)
        
        # # 添加安全阈值线（已注释）
        # ax.axhline(y=0.37, color='red', linestyle='--', linewidth=PAPER_STYLE['line_width'], 
        #           label=r'$Safety\ Threshold$', alpha=0.8)
        # ax.axhline(y=0.42, color='orange', linestyle=':', linewidth=PAPER_STYLE['line_width'], 
        #           label=r'$Avoidance\ Threshold$', alpha=0.8)
        
        ax.set_xlabel('Time(s)', fontsize=PAPER_STYLE['font_size'])
        ax.set_ylabel('Distance to Obstacle (m)', fontsize=9)
        ax.set_ylim(0, 1)  # 设置Y轴范围：0到+1m
        # 设置y轴刻度格式化器，去掉不必要的.0
        import matplotlib.ticker as ticker
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f'{x:g}'))
        ax.legend(loc='upper right', framealpha=0.5, fancybox=False, edgecolor='black',
                 handletextpad=PAPER_STYLE['legend_handletextpad'], columnspacing=PAPER_STYLE['legend_columnspacing'], labelspacing=PAPER_STYLE['legend_labelspacing'], borderpad=PAPER_STYLE['legend_borderpad'], handlelength=PAPER_STYLE['legend_handlelength'], ncol=2)
        
        # 设置x轴范围和标签
        all_times = []
        for i in range(5):
            if robots[i] and robots[i].get('obstacle_distance'):
                all_times.extend(robots[i]['t'])
        # 统一设置时间轴
        self._setup_time_axis(ax, all_times)
        
        if PAPER_STYLE['use_grid']:
            ax.grid(True, linestyle="-", alpha=0.3)
        
        plt.tight_layout()
        
        output_file = os.path.join(self.output_dir, 'obstacle_distance.png')
        plt.savefig(output_file, dpi=PAPER_STYLE['dpi'], bbox_inches='tight')
        print(f"✅ 障碍物距离图已保存: {output_file}")
        plt.close()
    
    def plot_computation_time(self):
        """绘制计算时间分析图"""
        fig, ax = plt.subplots(figsize=PAPER_STYLE['figure_size_single'])
        
        robots = self.data['robots']
        colors = ['#1f77b4', '#ff7f0e', '#ffcc00', '#9467bd', '#2ca02c']
        all_comp_time_ms = []
        
        for i in range(5):
            robot = robots[i]
            if robot and robot.get('computation_time'):
                t = np.array(robot['t'])
                comp_time_ms = np.array(robot['computation_time']) * 1000
                valid_comp_time_ms = comp_time_ms[np.isfinite(comp_time_ms)]
                if valid_comp_time_ms.size > 0:
                    all_comp_time_ms.extend(valid_comp_time_ms.tolist())
                
                ax.plot(t, comp_time_ms, color=colors[i], linewidth=PAPER_STYLE['line_width'], 
                       label=f'$Robot_{{{i+1}}}$', alpha=1.0)
        
        # 控制周期基准线
        ax.axhline(y=100, color='red', linestyle='-.', linewidth=PAPER_STYLE['line_width'], 
                  label=r'$T_s$', alpha=0.9)
        
        ax.set_xlabel('Time(s)', fontsize=PAPER_STYLE['font_size'])
        ax.set_ylabel('Computation Time (ms)', fontsize=9)
        ax.set_ylim(0, 200)  # 设置Y轴范围：0-200ms
        # 设置y轴刻度为50间隔
        import matplotlib.ticker as ticker
        ax.yaxis.set_major_locator(ticker.MultipleLocator(50))
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f'{x:g}'))
        if all_comp_time_ms:
            min_comp = np.min(all_comp_time_ms)
            max_comp = np.max(all_comp_time_ms)
            mean_comp = np.mean(all_comp_time_ms)
            stat_labels = [
                f'Min: {min_comp:.1f} ms',
                f'Max: {max_comp:.1f} ms',
                f'Mean: {mean_comp:.1f} ms'
            ]
        else:
            stat_labels = ['Min: N/A', 'Max: N/A', 'Mean: N/A']

        handles, labels = ax.get_legend_handles_labels()
        main_order = [
            '$Robot_{1}$', '$Robot_{2}$', '$Robot_{3}$',
            '$Robot_{4}$', '$Robot_{5}$', '$T_s$'
        ]
        main_handles = []
        main_labels = []
        for name in main_order:
            if name in labels:
                idx = labels.index(name)
                main_handles.append(handles[idx])
                main_labels.append(name)

        legend_main = ax.legend(main_handles, main_labels,
                 loc='upper left', bbox_to_anchor=(0.01, 0.99),
                 framealpha=0.5, fancybox=False, edgecolor='black',
                 handletextpad=PAPER_STYLE['legend_handletextpad'],
                 columnspacing=PAPER_STYLE['legend_columnspacing'],
                 labelspacing=PAPER_STYLE['legend_labelspacing'],
                 borderpad=PAPER_STYLE['legend_borderpad'],
                 handlelength=PAPER_STYLE['legend_handlelength'], ncol=2,
                 fontsize=PAPER_STYLE['legend_size'])
        ax.add_artist(legend_main)

        stat_handles = [Line2D([], [], linestyle='None', linewidth=0, color='none') for _ in stat_labels]
        ax.legend(stat_handles, stat_labels,
                 loc='upper left', bbox_to_anchor=(0.56, 0.99),
                 framealpha=0.5, fancybox=False, edgecolor='black',
                 handletextpad=0.0, columnspacing=0.0,
                 labelspacing=PAPER_STYLE['legend_labelspacing'],
                 borderpad=PAPER_STYLE['legend_borderpad'],
                 handlelength=0.0, ncol=1,
                 fontsize=PAPER_STYLE['legend_size'])
        
        # 设置x轴范围和标签
        all_times = []
        for i in range(5):
            if robots[i] and robots[i].get('computation_time'):
                all_times.extend(robots[i]['t'])
        # 统一设置时间轴
        self._setup_time_axis(ax, all_times)
        
        if PAPER_STYLE['use_grid']:
            ax.grid(True, linestyle="-", alpha=0.3)
        
        plt.tight_layout()
        
        output_file = os.path.join(self.output_dir, 'computation_time.png')
        plt.savefig(output_file, dpi=PAPER_STYLE['dpi'], bbox_inches='tight')
        print(f"✅ 计算时间分析图已保存: {output_file}")
        plt.close()
    
    def plot_heading_error(self):
        """绘制航向角误差图"""
        fig, ax = plt.subplots(figsize=PAPER_STYLE['figure_size_single'])
        
        robots = self.data['robots']
        colors = ['#1f77b4', '#ff7f0e', '#ffcc00', '#9467bd', '#2ca02c']
        
        for i in range(5):
            robot = robots[i]
            if robot and robot.get('thetae'):
                t = np.array(robot['t'])
                thetae = np.array(robot['thetae'])
                
                ax.plot(t, thetae, color=colors[i], linewidth=PAPER_STYLE['line_width'], 
                       label=f'$\\mathit{{Robot}}_{{{i+1}}}$', alpha=1.0)
        
        # 设置x轴范围
        all_times = []
        for i in range(5):
            if robots[i] and robots[i].get('thetae'):
                all_times.extend(robots[i]['t'])
        # 统一设置时间轴
        self._setup_time_axis(ax, all_times)
        
        ax.set_xlabel('Time(s)', fontsize=PAPER_STYLE['font_size'])
        ax.set_ylabel('$\\theta_i - \\theta_L$ (rad)', fontsize=9)
        ax.set_ylim(-4, 4)  # 设置Y轴范围：-4到+4
        # 设置y轴刻度为2间隔
        import matplotlib.ticker as ticker
        ax.yaxis.set_major_locator(ticker.MultipleLocator(2))
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f'{x:g}'))
        ax.legend(loc='upper right', framealpha=0.5, fancybox=False, edgecolor='black',
                 handletextpad=PAPER_STYLE['legend_handletextpad'], 
                 columnspacing=PAPER_STYLE['legend_columnspacing'], 
                 labelspacing=PAPER_STYLE['legend_labelspacing'], 
                 borderpad=PAPER_STYLE['legend_borderpad'], 
                 handlelength=PAPER_STYLE['legend_handlelength'], 
                 ncol=2)
        
        if PAPER_STYLE['use_grid']:
            ax.grid(True, linestyle="-", alpha=0.3)
        
        plt.tight_layout()
        
        output_file = os.path.join(self.output_dir, 'heading_error.png')
        plt.savefig(output_file, dpi=PAPER_STYLE['dpi'], bbox_inches='tight')
        print(f"✅ 航向角误差图已保存: {output_file}")
        plt.close()

    def plot_heading_angle(self):
        """绘制机器人与领导者朝向角图"""
        fig, ax = plt.subplots(figsize=PAPER_STYLE['figure_size_single'])

        leader = self.data['leader']
        robots = self.data['robots']
        colors = ['#1f77b4', '#ff7f0e', '#ffcc00', '#9467bd', '#2ca02c']

        leader_t = None
        leader_theta0 = None
        if leader and leader.get('t') and leader.get('theta0'):
            leader_t = np.asarray(leader['t'], dtype=float)
            leader_theta0 = np.asarray(leader['theta0'], dtype=float)
            n = min(len(leader_t), len(leader_theta0))
            if n > 1:
                leader_t = leader_t[:n]
                leader_theta0 = leader_theta0[:n]
                valid = np.isfinite(leader_t) & np.isfinite(leader_theta0)
                leader_t = leader_t[valid]
                leader_theta0 = leader_theta0[valid]
                if leader_t.size > 1:
                    order = np.argsort(leader_t)
                    leader_t = leader_t[order]
                    leader_theta0 = leader_theta0[order]
                    leader_t, unique_idx = np.unique(leader_t, return_index=True)
                    leader_theta0 = leader_theta0[unique_idx]
                else:
                    leader_t = None
                    leader_theta0 = None
            else:
                leader_t = None
                leader_theta0 = None

            # 若源数据存在，则绘制领导者朝向角
            if leader_t is not None and leader_theta0 is not None and leader_t.size > 0:
                ax.plot(leader_t, leader_theta0, linestyle='--', color='black',
                    linewidth=PAPER_STYLE['line_width_thick'], label='$Robot_L$', alpha=0.9)

        for i in range(5):
            robot = robots[i]
            if not robot or ('t' not in robot):
                continue

            t = np.asarray(robot['t'], dtype=float)
            theta = None

            if robot.get('thetac') is not None and len(robot.get('thetac', [])) > 0:
                theta_raw = np.asarray(robot['thetac'], dtype=float)
                n = min(len(t), len(theta_raw))
                if n > 0:
                    t_use = t[:n]
                    theta = theta_raw[:n]
            elif robot.get('thetae') is not None and len(robot.get('thetae', [])) > 0 and leader_t is not None:
                thetae_raw = np.asarray(robot['thetae'], dtype=float)
                n = min(len(t), len(thetae_raw))
                if n > 0:
                    t_use = t[:n]
                    thetae = thetae_raw[:n]
                    in_range = (t_use >= leader_t[0]) & (t_use <= leader_t[-1])
                    t_use = t_use[in_range]
                    thetae = thetae[in_range]
                    if t_use.size > 0:
                        theta = thetae + np.interp(t_use, leader_t, leader_theta0)

            if theta is None:
                continue

            valid = np.isfinite(t_use) & np.isfinite(theta)
            t_use = t_use[valid]
            theta = theta[valid]
            if t_use.size == 0:
                continue

            ax.plot(t_use, theta, color=colors[i], linewidth=PAPER_STYLE['line_width'],
                    label=f'$\\mathit{{Robot}}_{{{i+1}}}$', alpha=1.0)

        all_times = []
        if leader_t is not None and leader_t.size > 0:
            all_times.extend(leader_t.tolist())
        for i in range(5):
            if robots[i] and robots[i].get('t'):
                all_times.extend(robots[i]['t'])
        self._setup_time_axis(ax, all_times)

        ax.set_xlabel('Time(s)', fontsize=PAPER_STYLE['font_size'])
        ax.set_ylabel('$\\theta_i$ (rad)', fontsize=9)
        ax.set_ylim(-4, 4)

        import matplotlib.ticker as ticker
        ax.yaxis.set_major_locator(ticker.MultipleLocator(2))
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f'{x:g}'))
        ax.legend(loc='lower right', framealpha=0.5, fancybox=False, edgecolor='black',
                 handletextpad=PAPER_STYLE['legend_handletextpad'],
                 columnspacing=PAPER_STYLE['legend_columnspacing'],
                 labelspacing=PAPER_STYLE['legend_labelspacing'],
                 borderpad=PAPER_STYLE['legend_borderpad'],
                 handlelength=PAPER_STYLE['legend_handlelength'],
                 ncol=2)

        if PAPER_STYLE['use_grid']:
            ax.grid(True, linestyle='-', alpha=0.3)

        plt.tight_layout()

        output_file = os.path.join(self.output_dir, 'heading_angle.png')
        plt.savefig(output_file, dpi=PAPER_STYLE['dpi'], bbox_inches='tight')
        print(f"✅ 航向角图已保存: {output_file}")
        plt.close()
    
    def plot_avoidance_forces(self):
        """绘制避障力图"""
        fig, ax = plt.subplots(figsize=PAPER_STYLE['figure_size_single'])
        
        robots = self.data['robots']
        colors = ['#1f77b4', '#ff7f0e', '#ffcc00', '#9467bd', '#2ca02c']
        
        for i in range(5):
            robot = robots[i]
            if robot and robot.get('avoidance_force_magnitude'):
                t = np.array(robot['t'])
                force = np.array(robot['avoidance_force_magnitude'])
                
                ax.plot(t, force, color=colors[i], linewidth=PAPER_STYLE['line_width'], 
                       label=f'$Robot_{{{i+1}}}$', alpha=1.0)
        
        ax.set_xlabel('Time(s)', fontsize=PAPER_STYLE['font_size'])
        ax.set_ylabel('Force Magnitude', fontsize=9)
        ax.set_ylim(0, 1)  # 设置Y轴范围：0到+1
        # 设置y轴刻度格式化器，去掉不必要的.0
        import matplotlib.ticker as ticker
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f'{x:g}'))
        ax.legend(loc='lower right', framealpha=0.5, fancybox=False, edgecolor='black',
                 handletextpad=PAPER_STYLE['legend_handletextpad'], columnspacing=PAPER_STYLE['legend_columnspacing'], labelspacing=PAPER_STYLE['legend_labelspacing'], borderpad=PAPER_STYLE['legend_borderpad'], handlelength=PAPER_STYLE['legend_handlelength'], ncol=2)
        
        # 设置x轴范围和标签
        all_times = []
        for i in range(5):
            if robots[i] and robots[i].get('avoidance_force_magnitude'):
                all_times.extend(robots[i]['t'])
        # 统一设置时间轴
        self._setup_time_axis(ax, all_times)
        
        if PAPER_STYLE['use_grid']:
            ax.grid(True, linestyle="-", alpha=0.3)
        
        plt.tight_layout()
        
        output_file = os.path.join(self.output_dir, 'avoidance_forces.png')
        plt.savefig(output_file, dpi=PAPER_STYLE['dpi'], bbox_inches='tight')
        print(f"✅ 避障力图已保存: {output_file}")
        plt.close()

    def plot_observer_estimation(self):
        """绘制观测器估计效果图（共12条轨迹）"""
        fig, ax = plt.subplots(figsize=PAPER_STYLE['figure_size_single'])

        leader = self.data['leader']
        robots = self.data['robots']

        # 绘制领导者真实X坐标（深蓝色虚线）
        if leader and leader.get('x0'):
            leader_t = np.array(leader['t'])
            leader_x = np.array(leader['x0'])
            ax.plot(leader_t, leader_x, linestyle='--', color='darkblue',
                    linewidth=PAPER_STYLE['line_width'], label='$x_L$', alpha=1.0, zorder=6)

        # 绘制领导者真实Y坐标（深红色虚线）
        if leader and leader.get('y0'):
            leader_t = np.array(leader['t'])
            leader_y = np.array(leader['y0'])
            ax.plot(leader_t, leader_y, linestyle='--', color='darkred',
                    linewidth=PAPER_STYLE['line_width'], label='$y_L$', alpha=1.0, zorder=6)

        # 机器人颜色方案（与其他图保持一致）
        colors = ['#1f77b4', '#ff7f0e', '#ffcc00', '#9467bd', '#2ca02c']

        # 绘制5个机器人观测器估计的X和Y坐标
        for i in range(5):
            robot = robots[i]
            if robot is None:
                continue

            # 检查观测器数据是否存在
            has_zxeo_x = 'zxeo_x' in robot and robot['zxeo_x'] and len(robot['zxeo_x']) > 0
            has_zxeo_y = 'zxeo_y' in robot and robot['zxeo_y'] and len(robot['zxeo_y']) > 0

            if not has_zxeo_x or not has_zxeo_y:
                continue

            # 绘制X坐标估计（实线，带标签）
            if 't' in robot and len(robot['t']) > 0:
                robot_t = np.array(robot['t'])
                robot_zxeo_x = np.array(robot['zxeo_x'])
                min_len = min(len(robot_t), len(robot_zxeo_x))
                if min_len > 0:
                    ax.plot(robot_t[:min_len], robot_zxeo_x[:min_len], linestyle='-',
                            color=colors[i], linewidth=PAPER_STYLE['line_width'],
                            label=f'$\\zeta_{{{i+1},x/y}}$', alpha=1.0, zorder=4)

            # 绘制Y坐标估计（实线，不显示标签）
            if 't' in robot and len(robot['t']) > 0:
                robot_t = np.array(robot['t'])
                robot_zxeo_y = np.array(robot['zxeo_y'])
                min_len = min(len(robot_t), len(robot_zxeo_y))
                if min_len > 0:
                    ax.plot(robot_t[:min_len], robot_zxeo_y[:min_len], linestyle='-',
                            color=colors[i], linewidth=PAPER_STYLE['line_width'], alpha=1.0, zorder=4)

        # 设置x轴范围和标签
        all_times = list(leader['t']) if leader else []
        for i in range(5):
            if robots[i] and robots[i].get('t'):
                all_times.extend(robots[i]['t'])
        # 统一设置时间轴
        self._setup_time_axis(ax, all_times)

        ax.set_xlabel('Time(s)', fontsize=PAPER_STYLE['font_size'])
        ax.set_ylabel('Coordinate value (m)', fontsize=9)
        ax.set_ylim(-1, 6)
        # 设置y轴刻度格式化器，去掉不必要的.0
        import matplotlib.ticker as ticker
        ax.yaxis.set_major_locator(ticker.MultipleLocator(1.0))
        ax.set_yticks(np.arange(-1, 7, 1))
        ax.legend(loc='upper right', framealpha=0.5, fancybox=False, edgecolor='black',
                  handletextpad=PAPER_STYLE['legend_handletextpad'],
                  columnspacing=PAPER_STYLE['legend_columnspacing'],
                  labelspacing=PAPER_STYLE['legend_labelspacing'],
                  borderpad=PAPER_STYLE['legend_borderpad'],
                  handlelength=PAPER_STYLE['legend_handlelength'],
                  ncol=3, fontsize=PAPER_STYLE['legend_size'])

        if PAPER_STYLE['use_grid']:
            ax.grid(True, linestyle='-', alpha=0.3)

        # 添加放大子图显示前面的渐进收敛过程
        axins = ax.inset_axes([0.12, 0.7, 0.175, 0.175])

        # 使用“数据起始时刻 + 1s”作为放大窗口
        zoom_duration = 1.0
        start_times = []
        if leader and leader.get('t') and len(leader['t']) > 0:
            start_times.append(float(leader['t'][0]))
        for i in range(5):
            if robots[i] and robots[i].get('t') and len(robots[i]['t']) > 0:
                start_times.append(float(robots[i]['t'][0]))
        zoom_time_start = min(start_times) if start_times else 0.0
        zoom_time_end = zoom_time_start + zoom_duration

        def _window_curve_with_edges(t_data, y_data, x_start, x_end):
            n = min(len(t_data), len(y_data))
            if n < 2:
                return np.array([]), np.array([])

            t_arr = np.asarray(t_data[:n], dtype=float)
            y_arr = np.asarray(y_data[:n], dtype=float)
            valid = np.isfinite(t_arr) & np.isfinite(y_arr)
            t_arr = t_arr[valid]
            y_arr = y_arr[valid]
            if t_arr.size < 2:
                return np.array([]), np.array([])

            order = np.argsort(t_arr)
            t_arr = t_arr[order]
            y_arr = y_arr[order]
            t_unique, unique_idx = np.unique(t_arr, return_index=True)
            y_unique = y_arr[unique_idx]
            if t_unique.size < 2:
                return np.array([]), np.array([])

            in_window = (t_unique >= x_start) & (t_unique <= x_end)
            x_plot = t_unique[in_window]
            y_plot = y_unique[in_window]

            if t_unique[0] <= x_start <= t_unique[-1]:
                y_start = np.interp(x_start, t_unique, y_unique)
                if x_plot.size == 0 or not np.isclose(x_plot[0], x_start):
                    x_plot = np.insert(x_plot, 0, x_start)
                    y_plot = np.insert(y_plot, 0, y_start)
                else:
                    y_plot[0] = y_start

            if t_unique[0] <= x_end <= t_unique[-1]:
                y_end = np.interp(x_end, t_unique, y_unique)
                if x_plot.size == 0 or not np.isclose(x_plot[-1], x_end):
                    x_plot = np.append(x_plot, x_end)
                    y_plot = np.append(y_plot, y_end)
                else:
                    y_plot[-1] = y_end

            return x_plot, y_plot

        # 绘制领导者数据
        if leader and leader.get('x0'):
            leader_t = np.array(leader['t'])
            leader_x = np.array(leader['x0'])
            x_plot, y_plot = _window_curve_with_edges(leader_t, leader_x, zoom_time_start, zoom_time_end)
            if x_plot.size > 0:
                axins.plot(x_plot, y_plot, linestyle='--', color='darkblue',
                           linewidth=PAPER_STYLE['line_width']*0.8, alpha=0.9, zorder=6)

        if leader and leader.get('y0'):
            leader_t = np.array(leader['t'])
            leader_y = np.array(leader['y0'])
            x_plot, y_plot = _window_curve_with_edges(leader_t, leader_y, zoom_time_start, zoom_time_end)
            if x_plot.size > 0:
                axins.plot(x_plot, y_plot, linestyle='--', color='darkred',
                           linewidth=PAPER_STYLE['line_width']*0.8, alpha=0.9, zorder=6)

        # 绘制机器人数据
        for i in range(5):
            robot = robots[i]
            if robot is None:
                continue

            has_zxeo_x = 'zxeo_x' in robot and robot['zxeo_x'] and len(robot['zxeo_x']) > 0
            has_zxeo_y = 'zxeo_y' in robot and robot['zxeo_y'] and len(robot['zxeo_y']) > 0
            if not has_zxeo_x or not has_zxeo_y:
                continue

            if 't' in robot and len(robot['t']) > 0:
                robot_t = np.array(robot['t'])
                robot_zxeo_x = np.array(robot['zxeo_x'])
                robot_zxeo_y = np.array(robot['zxeo_y'])

                min_len_x = min(len(robot_t), len(robot_zxeo_x))
                min_len_y = min(len(robot_t), len(robot_zxeo_y))

                if min_len_x > 0:
                    x_plot, y_plot = _window_curve_with_edges(
                        robot_t[:min_len_x], robot_zxeo_x[:min_len_x], zoom_time_start, zoom_time_end
                    )
                    if x_plot.size > 0:
                        axins.plot(x_plot, y_plot, linestyle='-', color=colors[i],
                                   linewidth=PAPER_STYLE['line_width']*0.8, alpha=0.8, zorder=4)

                if min_len_y > 0:
                    x_plot, y_plot = _window_curve_with_edges(
                        robot_t[:min_len_y], robot_zxeo_y[:min_len_y], zoom_time_start, zoom_time_end
                    )
                    if x_plot.size > 0:
                        axins.plot(x_plot, y_plot, linestyle='-', color=colors[i],
                                   linewidth=PAPER_STYLE['line_width']*0.8, alpha=0.8, zorder=4)

        # 设置放大区域范围
        x_min, x_max = zoom_time_start, zoom_time_end
        y_min = -0.1
        y_max = 0.3
        axins.set_xlim(x_min, x_max)
        axins.set_ylim(y_min, y_max)

        # 子图只显示横纵轴最小值和最大值刻度
        axins.set_xticks([x_min, x_max])
        axins.set_yticks([y_min, y_max])
        axins.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f'{x - zoom_time_start:g}'))
        axins.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, p: f'{y:g}'))
        axins.tick_params(axis='x', labelsize=PAPER_STYLE['label_size']-2)
        axins.tick_params(axis='y', labelsize=PAPER_STYLE['label_size']-2)
        axins.tick_params(top=False, right=False)

        if PAPER_STYLE['use_grid']:
            axins.grid(True, linestyle='-', alpha=0.3)

        # 主图放大框
        box_y_min = -0.1
        zoom_rect = Rectangle((x_min, box_y_min), x_max - x_min, y_max - box_y_min,
                              fill=False, edgecolor='red', linewidth=0.8, alpha=0.8)
        ax.add_patch(zoom_rect)

        # 连接线
        conn1 = ConnectionPatch(
            xyA=(x_min, y_max), coordsA='data', axesA=ax,
            xyB=(0.0, 0.5), coordsB='axes fraction', axesB=axins,
            color='red', linewidth=0.8, alpha=0.8
        )
        ax.add_artist(conn1)

        conn2 = ConnectionPatch(
            xyA=(x_max, box_y_min), coordsA='data', axesA=ax,
            xyB=(0.5, 0.0), coordsB='axes fraction', axesB=axins,
            color='red', linewidth=0.8, alpha=0.8
        )
        ax.add_artist(conn2)

        plt.tight_layout()

        output_file = os.path.join(self.output_dir, 'observer_estimation.png')
        plt.savefig(output_file, dpi=PAPER_STYLE['dpi'], bbox_inches='tight')
        print(f"✅ 观测器估计效果图已保存: {output_file}")
        plt.close()

    def plot_observer_estimation_errors(self):
        """分别绘制观测器x/y估计误差图（估计值 - 领导者真实值）"""
        leader = self.data['leader']
        robots = self.data['robots']
        colors = ['#1f77b4', '#ff7f0e', '#ffcc00', '#9467bd', '#2ca02c']

        if not leader or ('t' not in leader):
            return

        leader_t_raw = np.asarray(leader['t'], dtype=float)

        def _prepare_leader_series(value_key):
            if value_key not in leader:
                return None, None
            leader_v_raw = np.asarray(leader[value_key], dtype=float)
            n = min(len(leader_t_raw), len(leader_v_raw))
            if n < 2:
                return None, None

            t = leader_t_raw[:n]
            v = leader_v_raw[:n]
            valid = np.isfinite(t) & np.isfinite(v)
            t = t[valid]
            v = v[valid]
            if t.size < 2:
                return None, None

            order = np.argsort(t)
            t = t[order]
            v = v[order]

            t_unique, unique_idx = np.unique(t, return_index=True)
            v_unique = v[unique_idx]
            if t_unique.size < 2:
                return None, None
            return t_unique, v_unique

        def _collect_robot_errors(robot_value_key, leader_value_key):
            leader_t, leader_v = _prepare_leader_series(leader_value_key)
            if leader_t is None:
                return {}, []

            error_data = {}
            all_times = []
            for i in range(5):
                robot = robots[i]
                if robot is None or ('t' not in robot) or (robot_value_key not in robot):
                    continue

                rt_raw = np.asarray(robot['t'], dtype=float)
                rv_raw = np.asarray(robot[robot_value_key], dtype=float)
                n = min(len(rt_raw), len(rv_raw))
                if n < 1:
                    continue

                rt = rt_raw[:n]
                rv = rv_raw[:n]
                valid = np.isfinite(rt) & np.isfinite(rv)
                rt = rt[valid]
                rv = rv[valid]
                if rt.size < 1:
                    continue

                in_range = (rt >= leader_t[0]) & (rt <= leader_t[-1])
                rt = rt[in_range]
                rv = rv[in_range]
                if rt.size < 1:
                    continue

                leader_interp = np.interp(rt, leader_t, leader_v)
                err = rv - leader_interp

                error_data[i] = {'t': rt, 'e': err}
                all_times.extend(rt.tolist())

            return error_data, all_times

        def _window_curve_with_edges(t_data, y_data, x_start, x_end):
            """裁剪到窗口并在边界插值补点，确保曲线可画到x_start/x_end。"""
            n = min(len(t_data), len(y_data))
            if n < 2:
                return np.array([]), np.array([])

            t_arr = np.asarray(t_data[:n], dtype=float)
            y_arr = np.asarray(y_data[:n], dtype=float)
            valid = np.isfinite(t_arr) & np.isfinite(y_arr)
            t_arr = t_arr[valid]
            y_arr = y_arr[valid]
            if t_arr.size < 2:
                return np.array([]), np.array([])

            order = np.argsort(t_arr)
            t_arr = t_arr[order]
            y_arr = y_arr[order]

            t_unique, unique_idx = np.unique(t_arr, return_index=True)
            y_unique = y_arr[unique_idx]
            if t_unique.size < 2:
                return np.array([]), np.array([])

            in_window = (t_unique >= x_start) & (t_unique <= x_end)
            x_plot = t_unique[in_window]
            y_plot = y_unique[in_window]

            if t_unique[0] <= x_start <= t_unique[-1]:
                y_start = np.interp(x_start, t_unique, y_unique)
                if x_plot.size == 0 or not np.isclose(x_plot[0], x_start):
                    x_plot = np.insert(x_plot, 0, x_start)
                    y_plot = np.insert(y_plot, 0, y_start)
                else:
                    y_plot[0] = y_start

            if t_unique[0] <= x_end <= t_unique[-1]:
                y_end = np.interp(x_end, t_unique, y_unique)
                if x_plot.size == 0 or not np.isclose(x_plot[-1], x_end):
                    x_plot = np.append(x_plot, x_end)
                    y_plot = np.append(y_plot, y_end)
                else:
                    y_plot[-1] = y_end

            return x_plot, y_plot

        def _plot_single(error_data, all_times, ylabel, output_name, inset_bounds):
            fig, ax = plt.subplots(figsize=PAPER_STYLE['figure_size_single'])
            all_err_values = []
            per_robot_mae = [np.nan] * 5

            for i in range(5):
                if i not in error_data:
                    continue
                t = error_data[i]['t']
                e = error_data[i]['e']
                all_err_values.extend(e.tolist())
                valid_robot_errs = np.asarray(e, dtype=float)
                valid_robot_errs = valid_robot_errs[np.isfinite(valid_robot_errs)]
                if valid_robot_errs.size > 0:
                    per_robot_mae[i] = float(np.mean(np.abs(valid_robot_errs)))
                ax.plot(t, e, color=colors[i], linewidth=PAPER_STYLE['line_width'],
                        label=f'$\\mathit{{Robot}}_{{{i+1}}}$', alpha=1.0)

            self._setup_time_axis(ax, all_times)

            ax.set_xlabel('Time(s)', fontsize=PAPER_STYLE['font_size'])
            ax.set_ylabel(ylabel, fontsize=9)
            ax.set_ylim(-1, 1)

            import matplotlib.ticker as ticker
            ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f'{x:g}'))
            ax.legend(loc='upper right', framealpha=0.5, fancybox=False, edgecolor='black',
                     handletextpad=PAPER_STYLE['legend_handletextpad'],
                     columnspacing=PAPER_STYLE['legend_columnspacing'],
                     labelspacing=PAPER_STYLE['legend_labelspacing'],
                     borderpad=PAPER_STYLE['legend_borderpad'],
                     handlelength=PAPER_STYLE['legend_handlelength'],
                     ncol=2)

            if PAPER_STYLE['use_grid']:
                ax.grid(True, linestyle='-', alpha=0.3)

            if all_times and inset_bounds is not None:
                x_min = float(inset_bounds[0])
                x_max = float(inset_bounds[1])
                y_min = float(inset_bounds[2])
                y_max = float(inset_bounds[3])

                if x_max > x_min and y_max > y_min:
                    axins = ax.inset_axes([0.23, 0.75, 0.175, 0.175])
                    has_curve = False

                    for i in range(5):
                        if i not in error_data:
                            continue
                        t = np.asarray(error_data[i]['t'], dtype=float)
                        e = np.asarray(error_data[i]['e'], dtype=float)
                        x_plot, y_plot = _window_curve_with_edges(t, e, x_min, x_max)
                        if x_plot.size == 0:
                            continue
                        has_curve = True
                        axins.plot(
                            x_plot,
                            y_plot,
                            linestyle='-',
                            color=colors[i],
                            linewidth=PAPER_STYLE['line_width'] * 0.8,
                            alpha=0.9,
                            zorder=4,
                        )

                    if has_curve:
                        axins.set_xlim(x_min, x_max)
                        axins.set_ylim(y_min, y_max)
                        axins.set_xticks([x_min, x_max])

                        y_ticks = [y_min, y_max]
                        show_zero_tick = y_min < 0.0 < y_max or np.isclose(y_min, 0.0) or np.isclose(y_max, 0.0)
                        if show_zero_tick:
                            y_ticks_with_zero = [y_min, 0.0, y_max]
                            axins.set_yticks(y_ticks_with_zero)

                            def ytick_formatter(y, _):
                                if np.isclose(y, y_min) or np.isclose(y, y_max):
                                    return f'{float(y):g}'
                                return ''

                            axins.yaxis.set_major_formatter(ticker.FuncFormatter(ytick_formatter))
                        else:
                            axins.set_yticks(y_ticks)
                            axins.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: f'{float(y):g}'))

                        axins.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{x:g}'))
                        axins.tick_params(axis='x', labelsize=PAPER_STYLE['label_size'] - 2)
                        axins.tick_params(axis='y', labelsize=PAPER_STYLE['label_size'] - 2)
                        axins.tick_params(top=False, right=False)

                        for spine in axins.spines.values():
                            spine.set_edgecolor('red')

                        if PAPER_STYLE['use_grid']:
                            axins.grid(True, linestyle='-', alpha=0.3)

                        zoom_rect = Rectangle(
                            (x_min, y_min),
                            x_max - x_min,
                            y_max - y_min,
                            fill=False,
                            edgecolor='red',
                            linewidth=0.4,
                            alpha=0.8,
                            linestyle=(0, (4, 2)),
                        )
                        ax.add_patch(zoom_rect)

                        conn1 = ConnectionPatch(
                            xyA=(x_min, y_max), coordsA='data', axesA=ax,
                            xyB=(0.0, 0.5), coordsB='axes fraction', axesB=axins,
                            color='red', linewidth=0.4, alpha=0.8,
                            linestyle=(0, (4, 2)),
                        )
                        ax.add_artist(conn1)

                        conn2 = ConnectionPatch(
                            xyA=(x_max, y_min), coordsA='data', axesA=ax,
                            xyB=(0.5, 0.0), coordsB='axes fraction', axesB=axins,
                            color='red', linewidth=0.4, alpha=0.8,
                            linestyle=(0, (4, 2)),
                        )
                        ax.add_artist(conn2)

            plt.tight_layout()

            output_file = os.path.join(self.output_dir, output_name)
            plt.savefig(output_file, dpi=PAPER_STYLE['dpi'], bbox_inches='tight')
            print(f"✅ 观测器估计误差图已保存: {output_file}")
            plt.close()

            valid_errs = np.asarray(all_err_values, dtype=float)
            valid_errs = valid_errs[np.isfinite(valid_errs)]
            if valid_errs.size == 0:
                return np.nan, per_robot_mae
            return float(np.mean(np.abs(valid_errs))), per_robot_mae

        def _analyze_error_debug(error_data, axis_name):
            """打印误差突增时刻与持续高误差区间统计。"""
            print(f"\n🔎 {axis_name}方向观测器误差调试统计")

            def _find_high_segments(t_arr, e_abs, threshold, min_duration):
                above = e_abs >= threshold
                segments = []
                idx = 0
                n = len(t_arr)
                while idx < n:
                    if not above[idx]:
                        idx += 1
                        continue
                    start_idx = idx
                    while idx + 1 < n and above[idx + 1]:
                        idx += 1
                    end_idx = idx

                    t_start = float(t_arr[start_idx])
                    t_end = float(t_arr[end_idx])
                    duration = max(0.0, t_end - t_start)
                    if duration >= min_duration:
                        seg_vals = e_abs[start_idx:end_idx + 1]
                        segments.append({
                            'start': t_start,
                            'end': t_end,
                            'duration': duration,
                            'peak': float(np.max(seg_vals)),
                            'mean': float(np.mean(seg_vals)),
                        })
                    idx += 1
                return segments

            def _merge_intervals(intervals):
                if not intervals:
                    return []
                intervals_sorted = sorted(intervals, key=lambda x: x[0])
                merged = [list(intervals_sorted[0])]
                for s, e in intervals_sorted[1:]:
                    last = merged[-1]
                    if s <= last[1]:
                        last[1] = max(last[1], e)
                    else:
                        merged.append([s, e])
                return [(float(s), float(e)) for s, e in merged]

            all_intervals = []
            analyzed_robot_count = 0

            for i in range(5):
                if i not in error_data:
                    continue

                t = np.asarray(error_data[i]['t'], dtype=float)
                e = np.asarray(error_data[i]['e'], dtype=float)
                valid = np.isfinite(t) & np.isfinite(e)
                t = t[valid]
                e = e[valid]
                if t.size < 3:
                    continue

                order = np.argsort(t)
                t = t[order]
                e = e[order]
                t, unique_idx = np.unique(t, return_index=True)
                e = e[unique_idx]
                if t.size < 3:
                    continue

                analyzed_robot_count += 1
                e_abs = np.abs(e)

                dt = np.diff(t)
                dt = dt[dt > 1e-9]
                median_dt = float(np.median(dt)) if dt.size > 0 else 0.1
                min_duration = max(0.6, 5.0 * median_dt)

                # 高误差阈值：鲁棒统计 + 百分位下限
                median_abs = float(np.median(e_abs))
                mad_abs = float(np.median(np.abs(e_abs - median_abs)))
                p90_abs = float(np.percentile(e_abs, 90))
                high_threshold = max(median_abs + 3.0 * mad_abs, p90_abs, 0.05)

                # 突增阈值：同时考虑斜率和瞬时跳变量
                d_abs = np.diff(e_abs)
                d_abs_dt = d_abs / np.maximum(np.diff(t), 1e-9)
                slope_thr = max(float(np.percentile(d_abs_dt, 97)), 0.08)
                jump_thr = max(float(np.percentile(d_abs, 97)), 0.015)

                spike_indices = np.where((d_abs_dt >= slope_thr) & (d_abs >= jump_thr))[0]
                top_spikes = sorted(spike_indices, key=lambda k: d_abs_dt[k], reverse=True)[:5]

                print(f"  Robot_{i+1}: high阈值={high_threshold:.4f}m, 最小持续时长={min_duration:.2f}s")

                if top_spikes:
                    print("    突增时刻Top5:")
                    for k in top_spikes:
                        t_evt = float(t[k + 1])
                        print(
                            f"      t={t_evt:.2f}s, |e|:{e_abs[k]:.4f}->{e_abs[k+1]:.4f}m, "
                            f"jump={d_abs[k]:.4f}m, slope={d_abs_dt[k]:.4f}m/s"
                        )
                else:
                    print("    突增时刻Top5: 无显著突增")

                segments = _find_high_segments(t, e_abs, high_threshold, min_duration)
                if segments:
                    total_high_duration = sum(seg['duration'] for seg in segments)
                    print(f"    持续高误差区间({len(segments)}段, 总时长={total_high_duration:.2f}s):")
                    for seg in segments:
                        print(
                            f"      [{seg['start']:.2f}, {seg['end']:.2f}]s, "
                            f"dur={seg['duration']:.2f}s, mean={seg['mean']:.4f}m, peak={seg['peak']:.4f}m"
                        )
                        all_intervals.append((seg['start'], seg['end']))
                else:
                    print("    持续高误差区间: 无")

            if analyzed_robot_count == 0:
                print("  无可用于统计的误差数据")
                return

            merged = _merge_intervals(all_intervals)
            if merged:
                union_duration = sum(e - s for s, e in merged)
                print(f"  跨机器人并集高误差时间段({len(merged)}段, 并集总时长={union_duration:.2f}s):")
                for s, e in merged:
                    print(f"    [{s:.2f}, {e:.2f}]s, dur={e - s:.2f}s")
            else:
                print("  跨机器人并集高误差时间段: 无")

        x_error_data, x_all_times = _collect_robot_errors('zxeo_x', 'x0')
        mean_x, per_robot_mae_x = _plot_single(
            x_error_data,
            x_all_times,
            '$\\zeta_{i,x} - x_L$ (m)',
            'observer_estimation_error_x.png',
            OBSERVER_ERROR_X_INSET_BOUNDS,
        )
        _analyze_error_debug(x_error_data, 'X')

        y_error_data, y_all_times = _collect_robot_errors('zxeo_y', 'y0')
        mean_y, per_robot_mae_y = _plot_single(
            y_error_data,
            y_all_times,
            '$\\zeta_{i,y} - y_L$ (m)',
            'observer_estimation_error_y.png',
            OBSERVER_ERROR_Y_INSET_BOUNDS,
        )
        _analyze_error_debug(y_error_data, 'Y')

        if np.isfinite(mean_x):
            print(f"📊 平均绝对观测器估计误差(x): {mean_x:.6f} m")
        else:
            print("📊 平均绝对观测器估计误差(x): N/A")

        if np.isfinite(mean_y):
            print(f"📊 平均绝对观测器估计误差(y): {mean_y:.6f} m")
        else:
            print("📊 平均绝对观测器估计误差(y): N/A")

        for i in range(5):
            value_x = per_robot_mae_x[i]
            value_y = per_robot_mae_y[i]
            text_x = f"{value_x:.6f} m" if np.isfinite(value_x) else "N/A"
            text_y = f"{value_y:.6f} m" if np.isfinite(value_y) else "N/A"
            print(f"📌 Robot_{i+1} 绝对平均估计误差: x={text_x}, y={text_y}")

    def plot_trigger_events(self):
        """绘制事件触发图（按机器人编号分层的触发时刻）。"""
        robots = self.data['robots']
        colors = ['#1f77b4', '#ff7f0e', '#ffcc00', '#9467bd', '#2ca02c']

        # 统计：规划层与跟踪层触发占比（触发点数/有效采样点数）
        planning_trigger_counts = [0] * 5
        planning_valid_counts = [0] * 5
        tracking_trigger_counts = [0] * 5
        tracking_valid_counts = [0] * 5

        fig, (ax1, ax2) = plt.subplots(
            2, 1,
            figsize=(PAPER_STYLE['figure_size_single'][0], PAPER_STYLE['figure_size_single'][1] * 1.9),
            sharex=True,
        )

        all_times = []

        # 规划层触发
        for i in range(5):
            robot = robots[i]
            if robot is None or ('t' not in robot) or ('trigger_time_p' not in robot):
                continue

            t = np.asarray(robot['t'], dtype=float)
            trig = np.asarray(robot['trigger_time_p'], dtype=float)
            n = min(len(t), len(trig))
            if n == 0:
                continue

            t = t[:n]
            trig = trig[:n]
            # 分母应为总时间采样点数（图上的总采样），不受trig为NaN影响
            valid_samples = np.isfinite(t)
            planning_valid_counts[i] += int(np.count_nonzero(valid_samples))

            valid = np.isfinite(t) & np.isfinite(trig) & (trig > 0)
            planning_trigger_counts[i] += int(np.count_nonzero(valid))
            if np.any(valid):
                y_lane = np.full(np.count_nonzero(valid), i + 1, dtype=float)
                ax1.scatter(t[valid], y_lane, s=0.5, marker='o', color=colors[i], alpha=0.8,
                            label=f'$\\mathit{{Robot}}_{{{i+1}}}$')
                all_times.extend(t[valid].tolist())

        ax1.set_ylabel('Robot', fontsize=9)
        ax1.set_yticks(np.arange(1, 6, 1))
        ax1.set_ylim(0, 6)
        if PAPER_STYLE['use_grid']:
            ax1.grid(True, linestyle='-', alpha=0.3)
        ax1.set_title('Trajectories planning', fontsize=PAPER_STYLE['font_size'])

        # 跟踪层触发
        for i in range(5):
            robot = robots[i]
            if robot is None or ('t' not in robot) or ('trigger_time' not in robot):
                continue

            t = np.asarray(robot['t'], dtype=float)
            trig = np.asarray(robot['trigger_time'], dtype=float)
            n = min(len(t), len(trig))
            if n == 0:
                continue

            t = t[:n]
            trig = trig[:n]
            # 分母应为总时间采样点数（图上的总采样），不受trig为NaN影响
            valid_samples = np.isfinite(t)
            tracking_valid_counts[i] += int(np.count_nonzero(valid_samples))

            valid = np.isfinite(t) & np.isfinite(trig) & (trig > 0)
            tracking_trigger_counts[i] += int(np.count_nonzero(valid))
            if np.any(valid):
                y_lane = np.full(np.count_nonzero(valid), i + 1, dtype=float)
                ax2.scatter(t[valid], y_lane, s=0.5, marker='o', color=colors[i], alpha=0.8,
                            label=f'$\\mathit{{Robot}}_{{{i+1}}}$')
                all_times.extend(t[valid].tolist())

        ax2.set_xlabel('Time(s)', fontsize=PAPER_STYLE['font_size'])
        ax2.set_ylabel('Robot', fontsize=9)
        ax2.set_yticks(np.arange(1, 6, 1))
        ax2.set_ylim(0, 6)
        ax2.set_title('Consensus tracking', fontsize=PAPER_STYLE['font_size'])
        if PAPER_STYLE['use_grid']:
            ax2.grid(True, linestyle='-', alpha=0.3)

        self._setup_time_axis(ax2, all_times)
        plt.tight_layout()

        output_file = os.path.join(self.output_dir, 'trigger_events.png')
        plt.savefig(output_file, dpi=PAPER_STYLE['dpi'], bbox_inches='tight')
        print(f"✅ 事件触发散点图已保存: {output_file}")
        plt.close()

        # ===== 终端打印：触发占比统计 =====
        planning_total_trigger = int(sum(planning_trigger_counts))
        planning_total_valid = int(sum(planning_valid_counts))
        tracking_total_trigger = int(sum(tracking_trigger_counts))
        tracking_total_valid = int(sum(tracking_valid_counts))

        def _ratio_text(num, den):
            if den <= 0:
                return "N/A"
            return f"{num}/{den} ({100.0 * num / den:.2f}%)"

        print("📈 事件触发占比统计")
        print(f"  规划层总体: {_ratio_text(planning_total_trigger, planning_total_valid)}")
        for i in range(5):
            print(
                f"    Robot_{i+1}: "
                f"{_ratio_text(planning_trigger_counts[i], planning_valid_counts[i])}"
            )

        print(f"  跟踪层总体: {_ratio_text(tracking_total_trigger, tracking_total_valid)}")
        for i in range(5):
            print(
                f"    Robot_{i+1}: "
                f"{_ratio_text(tracking_trigger_counts[i], tracking_valid_counts[i])}"
            )

    def plot_dos_topology(self):
        """绘制固定分段 DoS 攻击通道时序图。"""
        leader = self.data.get('leader', None)
        if not leader or ('t' not in leader) or len(leader['t']) == 0:
            print("⚠️ 领导者时间数据为空，跳过DoS时序图")
            return

        t_end = float(np.ceil(np.max(np.asarray(leader['t'], dtype=float))))
        t_end = max(0.0, t_end)

        fig, ax = plt.subplots(figsize=(PAPER_STYLE['figure_size_single'][0], PAPER_STYLE['figure_size_single'][1] * 1.4))

        # 按场景切换DoS配置：S场景使用70s版本，其它场景沿用原30s版本
        if OBSTACLE_MODE == 'experiment_s':
            dos_segments = [
                (0.0, 5.0,   {'ch1': 1, 'ch2': 1, 'ch3': 1, 'ch4': 1}),
                (5.0, 7.0,   {'ch1': 1, 'ch2': 0, 'ch3': 0, 'ch4': 1}),
                (7.0, 11.0,  {'ch1': 1, 'ch2': 1, 'ch3': 1, 'ch4': 1}),
                (11.0, 14.0, {'ch1': 0, 'ch2': 1, 'ch3': 0, 'ch4': 1}),
                (14.0, 15.0, {'ch1': 1, 'ch2': 1, 'ch3': 1, 'ch4': 1}),
                (18.0, 19.0, {'ch1': 1, 'ch2': 0, 'ch3': 1, 'ch4': 1}),
                (20.0, 24.0, {'ch1': 1, 'ch2': 1, 'ch3': 1, 'ch4': 1}),
                (24.0, 25.0, {'ch1': 0, 'ch2': 1, 'ch3': 1, 'ch4': 0}),
                (27.0, 32.0, {'ch1': 1, 'ch2': 1, 'ch3': 1, 'ch4': 1}),
                (32.0, 34.0, {'ch1': 1, 'ch2': 1, 'ch3': 1, 'ch4': 0}),
                (35.0, 39.0, {'ch1': 1, 'ch2': 1, 'ch3': 1, 'ch4': 1}),
                (39.0, 41.0, {'ch1': 0, 'ch2': 0, 'ch3': 0, 'ch4': 1}),
                (41.0, 43.0, {'ch1': 1, 'ch2': 0, 'ch3': 1, 'ch4': 1}),
                (45.0, 50.0, {'ch1': 1, 'ch2': 1, 'ch3': 1, 'ch4': 1}),
                (50.0, 51.0, {'ch1': 1, 'ch2': 1, 'ch3': 1, 'ch4': 0}),
                (54.0, 57.0, {'ch1': 1, 'ch2': 1, 'ch3': 1, 'ch4': 1}),
                (57.0, 59.0, {'ch1': 0, 'ch2': 0, 'ch3': 1, 'ch4': 1}),
                (59.0, 61.0, {'ch1': 1, 'ch2': 1, 'ch3': 1, 'ch4': 1}),
                (61.0, 64.0, {'ch1': 1, 'ch2': 1, 'ch3': 1, 'ch4': 0}),
                (64.0, 67.0, {'ch1': 1, 'ch2': 1, 'ch3': 1, 'ch4': 1}),
                (67.0, 70.0, {'ch1': 1, 'ch2': 1, 'ch3': 0, 'ch4': 1}),
                (70.0, 1e9,  {'ch1': 1, 'ch2': 1, 'ch3': 1, 'ch4': 1}),
            ]
        else:
            dos_segments = [
                (0.0, 5.0,  {'ch1': 1, 'ch2': 1, 'ch3': 1, 'ch4': 1}),
                (5.0, 8.0,  {'ch1': 0, 'ch2': 1, 'ch3': 0, 'ch4': 0}),
                (8.0, 12.0, {'ch1': 1, 'ch2': 1, 'ch3': 1, 'ch4': 1}),
                (12.0, 15.0, {'ch1': 1, 'ch2': 1, 'ch3': 0, 'ch4': 1}),
                (15.0, 22.0, {'ch1': 1, 'ch2': 1, 'ch3': 1, 'ch4': 1}),
                (22.0, 26.0, {'ch1': 1, 'ch2': 0, 'ch3': 1, 'ch4': 1}),
                (26.0, 28.0, {'ch1': 1, 'ch2': 1, 'ch3': 1, 'ch4': 1}),
                (28.0, 30.0, {'ch1': 1, 'ch2': 0, 'ch3': 1, 'ch4': 1}),
                (30.0, 1e9, {'ch1': 1, 'ch2': 1, 'ch3': 1, 'ch4': 1}),
            ]

        def get_state(t_now, ch):
            if ch == 'ch0':
                return 1
            for ts, te, states in dos_segments:
                if ts <= t_now < te:
                    return states[ch]
            return 1

        channels = ['ch0', 'ch1', 'ch2', 'ch3', 'ch4']
        colors = {
            'ch0': '#1f77b4',
            'ch1': '#ff7f0e',
            'ch2': '#f2b01e',
            'ch3': '#9467bd',
            'ch4': '#2ca02c',
        }

        key_times = {0.0, t_end}
        for ts, te, _ in dos_segments:
            if 0.0 <= ts <= t_end:
                key_times.add(ts)
            if 0.0 <= te <= t_end:
                key_times.add(te)
        knots = sorted(key_times)

        # 通道状态显示规则：
        # - ch1~ch4：正常在各自S位，攻击时共用同一个A位
        # - ch0：leader链路始终可用，固定在最高S位
        shared_a_level = 2.3
        # 通道线间距统一为0.3（含A到第一条S）
        s_level = {'ch0': 3.8, 'ch1': 3.5, 'ch2': 3.2, 'ch3': 2.9, 'ch4': 2.6}
        for ch in channels:
            y = []
            for t0 in knots:
                state = get_state(t0 + 1e-9, ch) if t0 < t_end else get_state(max(0.0, t_end - 1e-9), ch)
                if ch == 'ch0':
                    y.append(s_level[ch])
                else:
                    y.append(s_level[ch] if state == 1 else shared_a_level)
            ax.step(knots, y, where='post', linewidth=PAPER_STYLE['line_width'], color=colors[ch], label=ch)

        attack_label_used = False
        for ts, te, states in dos_segments:
            if ts >= t_end:
                continue
            left = max(0.0, ts)
            right = min(t_end, te)
            if right <= left:
                continue
            under_attack = not all(states[ch] == 1 for ch in ['ch1', 'ch2', 'ch3', 'ch4'])
            if under_attack:
                if not attack_label_used:
                    ax.axvspan(left, right, color='lightgray', alpha=0.35, label='attack interval')
                    attack_label_used = True
                else:
                    ax.axvspan(left, right, color='lightgray', alpha=0.35)

        ax.set_xlim(0, t_end)
        # 顶部留白用于放置图例，避免遮挡最上方S线
        ax.set_ylim(2.1, 4.6)
        ax.set_yticks([2.3, 2.6, 2.9, 3.2, 3.5, 3.8])
        ax.set_yticklabels(['A', 'S', 'S', 'S', 'S', 'S'])
        ax.set_xlabel('Time(s)', fontsize=PAPER_STYLE['font_size'])
        ax.set_ylabel('Channel state', fontsize=9)
        if PAPER_STYLE['use_grid']:
            ax.grid(True, linestyle='-', alpha=0.3)
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, 0.93), framealpha=0.5, fancybox=False, edgecolor='black',
                  handletextpad=PAPER_STYLE['legend_handletextpad'],
                  columnspacing=PAPER_STYLE['legend_columnspacing'],
                  labelspacing=PAPER_STYLE['legend_labelspacing'],
                  borderpad=PAPER_STYLE['legend_borderpad'],
                  handlelength=PAPER_STYLE['legend_handlelength'],
                  ncol=3)

        self._setup_time_axis(ax, [0.0, t_end])
        plt.tight_layout()

        output_file = os.path.join(self.output_dir, 'dos_topology.png')
        plt.savefig(output_file, dpi=PAPER_STYLE['dpi'], bbox_inches='tight')
        print(f"✅ DoS攻击时序图已保存: {output_file}")
        plt.close()
    
    def generate_all_plots(self):
        """生成所有论文图表"""
        print("\n" + "="*60)
        print("开始生成论文效果图...")
        print("="*60 + "\n")
        
        self.plot_trajectory(show_ideal=True, show_formation_lines=True)
        self.plot_x_error()
        self.plot_y_error()
        self.plot_cpl_control_inputs()
        self.plot_heading_error()
        self.plot_heading_angle()
        self.plot_linear_velocity()
        self.plot_angular_velocity()
        self.plot_obstacle_distance()
        self.plot_avoidance_forces()
        self.plot_computation_time()
        self.plot_observer_estimation()
        self.plot_observer_estimation_errors()
        self.plot_trigger_events()
        self.plot_dos_topology()
        
        print("\n" + "="*60)
        print(f"✅ 所有图表已生成完成！")
        print(f"📁 输出目录: {os.path.abspath(self.output_dir)}")
        print("="*60 + "\n")


if __name__ == "__main__":
    try:
        # 创建绘图器实例
        plotter = PaperPlotter(PKL_FILE_PATH)
        
        # 生成所有图表
        plotter.generate_all_plots()
        
        print("🎉 完成！现在你可以在output文件夹中找到生成的图表。")
        
    except FileNotFoundError as e:
        print(f"❌ 错误: {e}")
        print(f"请检查PKL_FILE_PATH是否正确: {PKL_FILE_PATH}")
    except Exception as e:
        print(f"❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()

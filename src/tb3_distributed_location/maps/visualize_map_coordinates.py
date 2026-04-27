#!/usr/bin/env python3
"""
地图坐标系可视化工具
功能：显示地图的坐标系、原点、坐标轴方向和刻度

使用方法1（推荐）：直接修改下面的配置区域，然后运行脚本
  python3 visualize_map_coordinates.py

使用方法2：使用命令行参数
  python3 visualize_map_coordinates.py [map_yaml_file] [--range X_MIN X_MAX Y_MIN Y_MAX]
"""

# ============================================================================
# 配置区域 - 直接修改这里的参数，然后运行脚本即可
# ============================================================================

# 地图文件名
MAP_YAML_FILE = '419_map_line.yaml'

# 显示模式选择：
# 'full'    - 显示完整地图（19.2m x 19.2m）
# 'local'   - 显示局部区域（自定义范围）
# 'experiment' - 实验区域（推荐：包含原点周围的实验区域）
DISPLAY_MODE = 'local'  # 改成 'full', 'local', 或 'experiment'

# 局部显示范围配置（仅在 DISPLAY_MODE='local' 时生效）
LOCAL_RANGE = {
    'x_min': -3,  # X轴最小值（米）
    'x_max': 6,   # X轴最大值（米）
    'y_min': -2,  # Y轴最小值（米）
    'y_max': 5    # Y轴最大值（米）
}

# 实验区域配置（仅在 DISPLAY_MODE='experiment' 时生效）
# 假设实验区域为 5.4m x 4.8m，从原点附近开始
EXPERIMENT_RANGE = {
    'x_min': -1,
    'x_max': 6,
    'y_min': -1,
    'y_max': 5
}

# ============================================================================
# 以下为程序代码，一般不需要修改
# ============================================================================

import cv2
import numpy as np
import yaml
import matplotlib.pyplot as plt
import sys
import os
import argparse

def visualize_map_coordinates(yaml_file='419_map_line.yaml', display_range=None):
    """可视化地图坐标系"""
    
    # 如果是相对路径，则相对于脚本所在目录
    if not os.path.isabs(yaml_file):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        yaml_file = os.path.join(script_dir, yaml_file)
    
    # 检查文件是否存在
    if not os.path.exists(yaml_file):
        print(f"Error: Cannot find file {yaml_file}")
        print(f"Script directory: {os.path.dirname(os.path.abspath(__file__))}")
        return
    
    # 读取地图配置
    with open(yaml_file, 'r') as f:
        config = yaml.safe_load(f)
    
    # 获取图片路径 (处理相对路径)
    image_path = config['image']
    if not os.path.isabs(image_path):
        yaml_dir = os.path.dirname(os.path.abspath(yaml_file))
        image_path = os.path.join(yaml_dir, image_path.lstrip('./'))
    
    # 读取地图图片
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print(f"Error: Cannot read map image {image_path}")
        return
    
    img_rgb = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    img_rgb = cv2.flip(img_rgb, 0)  # Flip Y axis for ROS coordinate system
    
    # 获取配置参数
    origin_x, origin_y, origin_theta = config['origin']
    resolution = config['resolution']
    height, width = img.shape
    
    # 计算地图实际覆盖范围
    max_x = origin_x + width * resolution
    max_y = origin_y + height * resolution
    
    # 确定显示范围
    if display_range is not None:
        # 使用用户指定的范围
        display_x_min, display_x_max, display_y_min, display_y_max = display_range
        # 确保显示范围在地图范围内
        display_x_min = max(display_x_min, origin_x)
        display_x_max = min(display_x_max, max_x)
        display_y_min = max(display_y_min, origin_y)
        display_y_max = min(display_y_max, max_y)
    else:
        # 显示完整地图
        display_x_min = origin_x
        display_x_max = max_x
        display_y_min = origin_y
        display_y_max = max_y
    
    # 创建图形 (白色背景)
    fig, ax = plt.subplots(figsize=(16, 14), facecolor='white')
    ax.set_facecolor('white')
    
    # 显示地图 (完全不透明)
    extent = [origin_x, max_x, origin_y, max_y]
    ax.imshow(img_rgb, extent=extent, origin='lower', alpha=1.0)
    
    # 设置显示范围
    ax.set_xlim(display_x_min, display_x_max)
    ax.set_ylim(display_y_min, display_y_max)
    
    # 动态计算刻度范围 (根据显示范围)
    x_range = np.arange(int(np.ceil(display_x_min)), int(np.floor(display_x_max)) + 1, 1)
    y_range = np.arange(int(np.ceil(display_y_min)), int(np.floor(display_y_max)) + 1, 1)
    
    # 绘制网格线 (每1米)
    for x in x_range:
        if x != 0:  # 0轴单独绘制
            ax.axvline(x=x, color='gray', linestyle=':', linewidth=0.8, alpha=0.5, zorder=1)
    
    for y in y_range:
        if y != 0:
            ax.axhline(y=y, color='gray', linestyle=':', linewidth=0.8, alpha=0.5, zorder=1)
    
    # 绘制主坐标轴 (只在0在显示范围内时)
    if display_y_min <= 0 <= display_y_max:
        ax.axhline(y=0, color='red', linestyle='--', linewidth=2.5, label='Y=0 axis', alpha=0.8, zorder=5)
    if display_x_min <= 0 <= display_x_max:
        ax.axvline(x=0, color='blue', linestyle='--', linewidth=2.5, label='X=0 axis', alpha=0.8, zorder=5)
    
    # 标注原点 (只在显示范围内)
    if display_x_min <= 0 <= display_x_max and display_y_min <= 0 <= display_y_max:
        ax.plot(0, 0, 'g*', markersize=35, label='Origin (0,0) = Start Point', 
                zorder=10, markeredgecolor='darkgreen', markeredgewidth=2)
        ax.text(0.3, 0.3, 'Origin & Start\n(0, 0)', fontsize=15, color='green', weight='bold',
                bbox=dict(boxstyle='round', facecolor='white', edgecolor='green', linewidth=2.5, alpha=0.95),
                zorder=11)
    
    # 绘制坐标轴箭头 (只在原点在显示范围内时)
    if display_x_min <= 0 <= display_x_max and display_y_min <= 0 <= display_y_max:
        arrow_len = min(3.0, (display_x_max - display_x_min) * 0.15, (display_y_max - display_y_min) * 0.15)
        
        # X轴箭头
        if 0 + arrow_len <= display_x_max:
            ax.arrow(0, 0, arrow_len, 0, head_width=0.4, head_length=0.3, 
                     fc='blue', ec='blue', linewidth=3.5, zorder=9)
            ax.text(arrow_len+0.5, 0, 'X+ (East)', fontsize=17, color='blue', weight='bold',
                    bbox=dict(boxstyle='round', facecolor='white', edgecolor='blue', linewidth=2, alpha=0.9))
        
        # Y轴箭头
        if 0 + arrow_len <= display_y_max:
            ax.arrow(0, 0, 0, arrow_len, head_width=0.4, head_length=0.3, 
                     fc='red', ec='red', linewidth=3.5, zorder=9)
            ax.text(0, arrow_len+0.5, 'Y+ (North)', fontsize=17, color='red', weight='bold',
                    bbox=dict(boxstyle='round', facecolor='white', edgecolor='red', linewidth=2, alpha=0.9))
    
    # X轴刻度标注 (每1米)
    for x in x_range:
        if display_y_min <= 0 <= display_y_max and abs(x) > 0.1:  # 只在0轴存在且不是原点时
            ax.plot(x, 0, 'bo', markersize=6, zorder=6)
            text_y = max(display_y_min + 0.3, -0.4)
            ax.text(x, text_y, f'{x:.0f}m', fontsize=11, color='blue', 
                   ha='center', weight='bold',
                   bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))
    
    # Y轴刻度标注 (每1米)
    for y in y_range:
        if display_x_min <= 0 <= display_x_max and abs(y) > 0.1:  # 只在0轴存在且不是原点时
            ax.plot(0, y, 'ro', markersize=6, zorder=6)
            text_x = max(display_x_min + 0.3, -0.4)
            ax.text(text_x, y, f'{y:.0f}m', fontsize=11, color='red', 
                   ha='center', weight='bold',
                   bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))
    
    # 标注地图四角 (显示完整地图边界)
    margin = 0.3
    # 只标注在显示范围内的角
    corners = []
    if abs(display_x_min - origin_x) < 0.1 and abs(display_y_min - origin_y) < 0.1:
        corners.append((origin_x + margin, origin_y + margin, f'({origin_x:.1f}, {origin_y:.1f})', 'left', 'bottom'))
    if abs(display_x_max - max_x) < 0.1 and abs(display_y_min - origin_y) < 0.1:
        corners.append((max_x - margin, origin_y + margin, f'({max_x:.1f}, {origin_y:.1f})', 'right', 'bottom'))
    if abs(display_x_min - origin_x) < 0.1 and abs(display_y_max - max_y) < 0.1:
        corners.append((origin_x + margin, max_y - margin, f'({origin_x:.1f}, {max_y:.1f})', 'left', 'top'))
    if abs(display_x_max - max_x) < 0.1 and abs(display_y_max - max_y) < 0.1:
        corners.append((max_x - margin, max_y - margin, f'({max_x:.1f}, {max_y:.1f})', 'right', 'top'))
    
    for x, y, label, ha, va in corners:
        ax.text(x, y, label, fontsize=10, ha=ha, va=va,
                bbox=dict(boxstyle='round', facecolor='yellow', edgecolor='black', 
                         linewidth=1.5, alpha=0.9), zorder=8)
    
    # 设置刻度
    ax.set_xticks(x_range)
    ax.set_yticks(y_range)
    
    # 次刻度: 每0.5米
    x_minor = np.arange(int(np.ceil(display_x_min)), int(np.floor(display_x_max)) + 1, 0.5)
    y_minor = np.arange(int(np.ceil(display_y_min)), int(np.floor(display_y_max)) + 1, 0.5)
    ax.set_xticks(x_minor, minor=True)
    ax.set_yticks(y_minor, minor=True)
    
    # 网格
    ax.grid(True, which='major', alpha=0.6, linestyle='-', linewidth=1.2)
    ax.grid(True, which='minor', alpha=0.3, linestyle=':', linewidth=0.6)
    
    # 设置图例和标题
    ax.legend(loc='upper right', fontsize=13, framealpha=0.95, 
             edgecolor='black', fancybox=True, shadow=True)
    ax.set_xlabel('X Coordinate (meters)', fontsize=16, weight='bold')
    ax.set_ylabel('Y Coordinate (meters)', fontsize=16, weight='bold')
    
    map_name = os.path.basename(yaml_file).replace('.yaml', '')
    if display_range:
        ax.set_title(f'Map Coordinate System: {map_name} (Local View)\n' + 
                     f'Display: X[{display_x_min:.1f}, {display_x_max:.1f}] Y[{display_y_min:.1f}, {display_y_max:.1f}] | Grid: 1m',
                     fontsize=18, weight='bold', pad=25)
    else:
        ax.set_title(f'Map Coordinate System: {map_name}\n' + 
                     'Origin (0,0) = Mapping Start Point | Grid: 1m',
                     fontsize=18, weight='bold', pad=25)
    ax.set_aspect('equal')
    
    # 添加配置信息文本框
    info_text = "Map Configuration:\n"
    info_text += f"Origin: [{origin_x:.2f}, {origin_y:.2f}, {origin_theta:.2f}]\n"
    info_text += f"Resolution: {resolution} m/pixel\n"
    info_text += f"Image Size: {width} x {height} px\n"
    info_text += f"Full Coverage: {width*resolution:.1f}m x {height*resolution:.1f}m\n"
    if display_range:
        info_text += f"\nDisplay Range:\n"
        info_text += f"X: [{display_x_min:.1f}, {display_x_max:.1f}] m\n"
        info_text += f"Y: [{display_y_min:.1f}, {display_y_max:.1f}] m"
    else:
        info_text += f"X range: [{origin_x:.1f}, {max_x:.1f}] m\n"
        info_text += f"Y range: [{origin_y:.1f}, {max_y:.1f}] m"
    
    ax.text(0.02, 0.98, info_text, transform=ax.transAxes,
            fontsize=11, verticalalignment='top', family='monospace',
            bbox=dict(boxstyle='round', facecolor='lightblue', 
                     edgecolor='navy', linewidth=2, alpha=0.9))
    
    # 保存图片
    if display_range:
        output_file = yaml_file.replace('.yaml', '_local_view.png')
    else:
        output_file = yaml_file.replace('.yaml', '_coordinate_visualization.png')
    
    # 确保输出文件在脚本所在目录
    output_file = os.path.basename(output_file)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(script_dir, output_file)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=200, bbox_inches='tight')
    
    print("=" * 70)
    print("Map Coordinate Visualization Complete!")
    print("=" * 70)
    print(f"Map file:   {yaml_file}")
    print(f"Output:     {output_file}")
    print(f"\nFull Map Info:")
    print(f"  Origin:          (0, 0) = Mapping start point")
    print(f"  X range:         {origin_x:.1f}m to {max_x:.1f}m")
    print(f"  Y range:         {origin_y:.1f}m to {max_y:.1f}m")
    print(f"  Resolution:      {resolution} m/pixel ({resolution*100} cm/pixel)")
    print(f"  Coverage:        {width*resolution:.1f}m x {height*resolution:.1f}m")
    if display_range:
        print(f"\nDisplay Range:")
        print(f"  X: {display_x_min:.1f}m to {display_x_max:.1f}m ({display_x_max - display_x_min:.1f}m)")
        print(f"  Y: {display_y_min:.1f}m to {display_y_max:.1f}m ({display_y_max - display_y_min:.1f}m)")
    print(f"\nGrid Info:")

    print(f"  Major grid:      1 meter")
    print(f"  Minor grid:      0.5 meter")
    print(f"  Blue numbers:    X-axis ticks (meters)")
    print(f"  Red numbers:     Y-axis ticks (meters)")
    print("=" * 70)
    
    # 关闭图形（不显示）
    plt.close()

if __name__ == '__main__':
    # 检查是否使用命令行参数
    if len(sys.argv) > 1 and sys.argv[1] not in ['-h', '--help']:
        # 使用命令行参数模式
        parser = argparse.ArgumentParser(
            description='Visualize map coordinate system with optional local view',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog='''
Examples:
  # 显示完整地图
  python3 visualize_map_coordinates.py 419_map_line.yaml
  
  # 显示局部区域
  python3 visualize_map_coordinates.py 419_map_line.yaml --range -2 6 -2 5
            '''
        )
        
        parser.add_argument('yaml_file', nargs='?', default=MAP_YAML_FILE,
                           help='Map YAML file (default: 419_map_line.yaml)')
        parser.add_argument('--range', nargs=4, type=float, metavar=('X_MIN', 'X_MAX', 'Y_MIN', 'Y_MAX'),
                           help='Display range in meters: X_MIN X_MAX Y_MIN Y_MAX')
        
        args = parser.parse_args()
        visualize_map_coordinates(args.yaml_file, args.range)
    else:
        # 使用配置文件模式
        print("\n" + "="*70)
        print("使用配置模式运行")
        print("="*70)
        print(f"地图文件: {MAP_YAML_FILE}")
        print(f"显示模式: {DISPLAY_MODE}")
        
        # 根据模式选择显示范围
        if DISPLAY_MODE == 'full':
            display_range = None
            print("范围: 完整地图")
        elif DISPLAY_MODE == 'local':
            display_range = [LOCAL_RANGE['x_min'], LOCAL_RANGE['x_max'], 
                           LOCAL_RANGE['y_min'], LOCAL_RANGE['y_max']]
            print(f"范围: X[{LOCAL_RANGE['x_min']}, {LOCAL_RANGE['x_max']}] "
                  f"Y[{LOCAL_RANGE['y_min']}, {LOCAL_RANGE['y_max']}]")
        elif DISPLAY_MODE == 'experiment':
            display_range = [EXPERIMENT_RANGE['x_min'], EXPERIMENT_RANGE['x_max'], 
                           EXPERIMENT_RANGE['y_min'], EXPERIMENT_RANGE['y_max']]
            print(f"范围: X[{EXPERIMENT_RANGE['x_min']}, {EXPERIMENT_RANGE['x_max']}] "
                  f"Y[{EXPERIMENT_RANGE['y_min']}, {EXPERIMENT_RANGE['y_max']}]")
        else:
            print(f"错误: 未知的显示模式 '{DISPLAY_MODE}'")
            print("可选模式: 'full', 'local', 'experiment'")
            sys.exit(1)
        
        print("="*70 + "\n")
        
        # 生成可视化
        visualize_map_coordinates(MAP_YAML_FILE, display_range)


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
里程计数据解析脚本

功能：
1. 读取PKL数据文件
2. 解析机器人0和4的里程计位姿数据
3. 显示详细的位置、速度和时间信息

使用方法：
python3 parse_robot_odometry.py
"""

import pickle
import numpy as np
import os

# ==================== 配置区域 ====================
# 修改这里指定要读取的PKL文件路径
# PKL_FILE_PATH = "./8字形一致性编队及避障实验数据（实物：直线+S形）/line/consensus_data_2026-02-07-15-09-15.pkl"
PKL_FILE_PATH = "./8字形一致性编队及避障实验数据（实物：直线+S形）/S/consensus_data_2026-04-15-17-03-25.pkl"
# ==================================================


def load_pkl_data(pkl_file_path):
    """加载PKL数据文件"""
    # 获取脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 展开路径中的~符号
    pkl_file_path = os.path.expanduser(pkl_file_path)
    
    # 如果是相对路径，则基于脚本目录解析
    if not os.path.isabs(pkl_file_path):
        pkl_file = os.path.abspath(os.path.join(script_dir, pkl_file_path))
    else:
        pkl_file = os.path.abspath(pkl_file_path)
    
    print(f"正在读取文件: {pkl_file}")
    
    if not os.path.exists(pkl_file):
        print(f"❌ 错误：文件不存在 - {pkl_file}")
        return None
    
    try:
        with open(pkl_file, 'rb') as f:
            data = pickle.load(f)
        print(f"✓ 文件读取成功")
        return data
    except Exception as e:
        print(f"❌ 读取文件时出错: {e}")
        return None


def print_data_structure(data):
    """打印数据结构"""
    print("\n" + "="*80)
    print("数据结构概览")
    print("="*80)
    
    if isinstance(data, dict):
        print(f"数据类型: 字典 (dict)")
        print(f"顶层键: {list(data.keys())}")
        print()
        
        # 检查是否有robots键
        if 'robots' in data:
            print("机器人数据 (robots):")
            robots = data['robots']
            if isinstance(robots, dict):
                print(f"  机器人ID列表: {list(robots.keys())}")
                print()
                
                # 显示第一个机器人的数据结构
                for robot_id in robots:
                    if robots[robot_id] is not None:
                        print(f"  机器人{robot_id}的数据字段:")
                        for key in robots[robot_id].keys():
                            value = robots[robot_id][key]
                            if isinstance(value, list):
                                print(f"    - {key}: 列表，长度={len(value)}")
                            else:
                                print(f"    - {key}: {type(value).__name__}")
                        break
        
        # 检查是否有leader键
        if 'leader' in data:
            print("\n领导者数据 (leader):")
            leader = data['leader']
            if isinstance(leader, dict):
                print(f"  领导者数据字段:")
                for key in leader.keys():
                    value = leader[key]
                    if isinstance(value, list):
                        print(f"    - {key}: 列表，长度={len(value)}")
                        if len(value) > 0:
                            print(f"      首个值: {value[0]}")
                    else:
                        print(f"    - {key}: {type(value).__name__} = {value}")
            else:
                print(f"  领导者数据类型: {type(leader).__name__}")
                print(f"  领导者数据值: {leader}")
        else:
            print("\n⚠️ 数据中没有leader键")
    else:
        print(f"数据类型: {type(data)}")


def parse_robot_odometry(data, robot_ids=[0, 1, 2, 3, 4]):
    """解析指定机器人的里程计数据"""
    
    if data is None or 'robots' not in data:
        print("❌ 数据无效或不包含机器人信息")
        return
    
    robots = data['robots']
    
    print("\n" + "="*80)
    print("机器人里程计位姿数据")
    print("="*80)
    
    for robot_id in robot_ids:
        if robot_id not in robots:
            print(f"\n❌ 机器人{robot_id}不存在于数据中")
            continue
        
        robot_data = robots[robot_id]
        
        if robot_data is None:
            print(f"\n❌ 机器人{robot_id}的数据为空")
            continue
        
        print(f"\n{'='*80}")
        print(f"机器人 {robot_id} 的里程计数据")
        print(f"{'='*80}")
        
        # 提取关键信息
        print(f"\n基本信息:")
        if 'robot_id' in robot_data:
            print(f"  机器人ID: {robot_data['robot_id']}")
        
        # 时间信息
        if 't' in robot_data and robot_data['t']:
            t = np.array(robot_data['t'])
            print(f"\n时间序列:")
            print(f"  数据点数: {len(t)}")
            print(f"  起始时间: {t[0]:.3f} s")
            print(f"  结束时间: {t[-1]:.3f} s")
            print(f"  总时长: {t[-1] - t[0]:.3f} s")
            print(f"  平均采样间隔: {np.mean(np.diff(t)):.3f} s")
        
        # 位置信息 (xc, yc) - 实际里程计位置
        x_key = 'xc' if 'xc' in robot_data else 'x'
        y_key = 'yc' if 'yc' in robot_data else 'y'
        theta_key = 'thetac' if 'thetac' in robot_data else 'theta'
        
        if x_key in robot_data and robot_data[x_key] and y_key in robot_data and robot_data[y_key]:
            x = np.array(robot_data[x_key])
            y = np.array(robot_data[y_key])
            
            print(f"\n位置信息 ({x_key}, {y_key}) - 实际里程计位姿:")
            print(f"  数据点数: {len(x)}")
            print(f"  起始位置: ({x[0]:.4f}, {y[0]:.4f}) m")
            print(f"  结束位置: ({x[-1]:.4f}, {y[-1]:.4f}) m")
            print(f"  位移: ({x[-1]-x[0]:.4f}, {y[-1]-y[0]:.4f}) m")
            print(f"  X范围: [{np.min(x):.4f}, {np.max(x):.4f}] m")
            print(f"  Y范围: [{np.min(y):.4f}, {np.max(y):.4f}] m")
            
            # 计算轨迹长度
            distances = np.sqrt(np.diff(x)**2 + np.diff(y)**2)
            total_distance = np.sum(distances)
            print(f"  轨迹总长度: {total_distance:.4f} m")
        
        # 航向角信息
        if theta_key in robot_data and robot_data[theta_key]:
            theta = np.array(robot_data[theta_key])
            print(f"\n航向角信息 ({theta_key}) - 实际里程计航向:")
            print(f"  数据点数: {len(theta)}")
            print(f"  起始角度: {np.degrees(theta[0]):.2f}° ({theta[0]:.4f} rad)")
            print(f"  结束角度: {np.degrees(theta[-1]):.2f}° ({theta[-1]:.4f} rad)")
            print(f"  角度范围: [{np.degrees(np.min(theta)):.2f}°, {np.degrees(np.max(theta)):.2f}°]")
        
        # 线速度信息
        if 'vc' in robot_data and robot_data['vc']:
            vc = np.array(robot_data['vc'])
            print(f"\n线速度信息 (vc):")
            print(f"  数据点数: {len(vc)}")
            print(f"  平均速度: {np.mean(vc):.4f} m/s")
            print(f"  最大速度: {np.max(vc):.4f} m/s")
            print(f"  最小速度: {np.min(vc):.4f} m/s")
            print(f"  速度标准差: {np.std(vc):.4f} m/s")
        
        # 角速度信息
        if 'wc' in robot_data and robot_data['wc']:
            wc = np.array(robot_data['wc'])
            print(f"\n角速度信息 (wc):")
            print(f"  数据点数: {len(wc)}")
            print(f"  平均角速度: {np.degrees(np.mean(wc)):.2f}°/s ({np.mean(wc):.4f} rad/s)")
            print(f"  最大角速度: {np.degrees(np.max(wc)):.2f}°/s ({np.max(wc):.4f} rad/s)")
            print(f"  最小角速度: {np.degrees(np.min(wc)):.2f}°/s ({np.min(wc):.4f} rad/s)")
        
        # 期望位置信息 (如果有)
        if 'xr' in robot_data and robot_data['xr'] and 'yr' in robot_data and robot_data['yr']:
            xr = np.array(robot_data['xr'])
            yr = np.array(robot_data['yr'])
            x = np.array(robot_data[x_key])
            y = np.array(robot_data[y_key])
            
            print(f"\n期望位置信息 (xr, yr):")
            print(f"  数据点数: {len(xr)}")
            print(f"  起始期望位置: ({xr[0]:.4f}, {yr[0]:.4f}) m")
            print(f"  结束期望位置: ({xr[-1]:.4f}, {yr[-1]:.4f}) m")
            
            # 计算跟踪误差
            if len(x) == len(xr) and len(y) == len(yr):
                ex = x - xr
                ey = y - yr
                tracking_error = np.sqrt(ex**2 + ey**2)
                print(f"  平均跟踪误差: {np.mean(tracking_error):.4f} m")
                print(f"  最大跟踪误差: {np.max(tracking_error):.4f} m")
                print(f"  最终跟踪误差: {tracking_error[-1]:.4f} m")
        
        # 显示前5个和后5个数据点
        print(f"\n前5个位姿数据点:")
        print(f"  {'时间(s)':<10} {'X(m)':<12} {'Y(m)':<12} {'Theta(deg)':<12}")
        print(f"  {'-'*50}")
        if 't' in robot_data and x_key in robot_data and y_key in robot_data and theta_key in robot_data:
            t = robot_data['t']
            x = robot_data[x_key]
            y = robot_data[y_key]
            theta = robot_data[theta_key]
            for i in range(min(5, len(t))):
                print(f"  {t[i]:<10.3f} {x[i]:<12.6f} {y[i]:<12.6f} {np.degrees(theta[i]):<12.2f}")
        
        print(f"\n后5个位姿数据点:")
        print(f"  {'时间(s)':<10} {'X(m)':<12} {'Y(m)':<12} {'Theta(deg)':<12}")
        print(f"  {'-'*50}")
        if 't' in robot_data and x_key in robot_data and y_key in robot_data and theta_key in robot_data:
            t = robot_data['t']
            x = robot_data[x_key]
            y = robot_data[y_key]
            theta = robot_data[theta_key]
            for i in range(max(0, len(t)-5), len(t)):
                print(f"  {t[i]:<10.3f} {x[i]:<12.6f} {y[i]:<12.6f} {np.degrees(theta[i]):<12.2f}")


def parse_leader_data(data):
    """解析虚拟领导者的数据"""
    
    if data is None or 'leader' not in data:
        print("\n❌ 数据无效或不包含领导者信息")
        return
    
    leader_data = data['leader']
    
    if leader_data is None:
        print("\n❌ 领导者数据为空")
        return
    
    print(f"\n{'='*80}")
    print(f"虚拟领导者数据")
    print(f"{'='*80}")
    
    # 时间信息
    if 't' in leader_data and leader_data['t']:
        t = np.array(leader_data['t'])
        print(f"\n时间序列:")
        print(f"  数据点数: {len(t)}")
        print(f"  起始时间: {t[0]:.3f} s")
        print(f"  结束时间: {t[-1]:.3f} s")
        print(f"  总时长: {t[-1] - t[0]:.3f} s")
        print(f"  平均采样间隔: {np.mean(np.diff(t)):.3f} s")
    
    # 位置信息
    if 'x0' in leader_data and leader_data['x0'] and 'y0' in leader_data and leader_data['y0']:
        x = np.array(leader_data['x0'])
        y = np.array(leader_data['y0'])
        
        print(f"\n位置信息 (x0, y0):")
        print(f"  数据点数: {len(x)}")
        print(f"  起始位置: ({x[0]:.4f}, {y[0]:.4f}) m")
        print(f"  结束位置: ({x[-1]:.4f}, {y[-1]:.4f}) m")
        print(f"  位移: ({x[-1]-x[0]:.4f}, {y[-1]-y[0]:.4f}) m")
        print(f"  X范围: [{np.min(x):.4f}, {np.max(x):.4f}] m")
        print(f"  Y范围: [{np.min(y):.4f}, {np.max(y):.4f}] m")
        
        # 计算轨迹长度
        distances = np.sqrt(np.diff(x)**2 + np.diff(y)**2)
        total_distance = np.sum(distances)
        print(f"  轨迹总长度: {total_distance:.4f} m")
    
    # 航向角信息
    if 'theta0' in leader_data and leader_data['theta0']:
        theta = np.array(leader_data['theta0'])
        print(f"\n航向角信息 (theta0):")
        print(f"  数据点数: {len(theta)}")
        print(f"  起始角度: {np.degrees(theta[0]):.2f}° ({theta[0]:.4f} rad)")
        print(f"  结束角度: {np.degrees(theta[-1]):.2f}° ({theta[-1]:.4f} rad)")
        print(f"  角度范围: [{np.degrees(np.min(theta)):.2f}°, {np.degrees(np.max(theta)):.2f}°]")
    
    # 线速度信息
    if 'v0' in leader_data and leader_data['v0']:
        v = np.array(leader_data['v0'])
        print(f"\n线速度信息 (v0):")
        print(f"  数据点数: {len(v)}")
        print(f"  平均速度: {np.mean(v):.4f} m/s")
        print(f"  最大速度: {np.max(v):.4f} m/s")
        print(f"  最小速度: {np.min(v):.4f} m/s")
        print(f"  速度标准差: {np.std(v):.4f} m/s")
    
    # 角速度信息
    if 'w0' in leader_data and leader_data['w0']:
        w = np.array(leader_data['w0'])
        print(f"\n角速度信息 (w0):")
        print(f"  数据点数: {len(w)}")
        print(f"  平均角速度: {np.degrees(np.mean(w)):.2f}°/s ({np.mean(w):.4f} rad/s)")
        print(f"  最大角速度: {np.degrees(np.max(w)):.2f}°/s ({np.max(w):.4f} rad/s)")
        print(f"  最小角速度: {np.degrees(np.min(w)):.2f}°/s ({np.min(w):.4f} rad/s)")
    
    # 显示前5个和后5个数据点
    print(f"\n前5个位姿数据点:")
    print(f"  {'时间(s)':<10} {'X(m)':<12} {'Y(m)':<12} {'Theta(deg)':<12}")
    print(f"  {'-'*50}")
    if 't' in leader_data and 'x0' in leader_data and 'y0' in leader_data and 'theta0' in leader_data:
        t = leader_data['t']
        x = leader_data['x0']
        y = leader_data['y0']
        theta = leader_data['theta0']
        for i in range(min(5, len(t))):
            print(f"  {t[i]:<10.3f} {x[i]:<12.6f} {y[i]:<12.6f} {np.degrees(theta[i]):<12.2f}")
    
    print(f"\n后5个位姿数据点:")
    print(f"  {'时间(s)':<10} {'X(m)':<12} {'Y(m)':<12} {'Theta(deg)':<12}")
    print(f"  {'-'*50}")
    if 't' in leader_data and 'x0' in leader_data and 'y0' in leader_data and 'theta0' in leader_data:
        t = leader_data['t']
        x = leader_data['x0']
        y = leader_data['y0']
        theta = leader_data['theta0']
        for i in range(max(0, len(t)-5), len(t)):
            print(f"  {t[i]:<10.3f} {x[i]:<12.6f} {y[i]:<12.6f} {np.degrees(theta[i]):<12.2f}")


def save_odometry_to_csv(data, robot_ids=[0, 1, 2, 3, 4], output_dir="./output_odometry"):
    """将里程计数据保存为CSV文件"""
    
    if data is None or 'robots' not in data:
        print("❌ 数据无效或不包含机器人信息")
        return
    
    # 创建输出目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, output_dir)
    os.makedirs(output_dir, exist_ok=True)
    
    robots = data['robots']
    
    print("\n" + "="*80)
    print("保存CSV文件")
    print("="*80)
    
    for robot_id in robot_ids:
        if robot_id not in robots or robots[robot_id] is None:
            continue
        
        robot_data = robots[robot_id]
        
        # 检查必要字段
        x_key = 'xc' if 'xc' in robot_data else 'x'
        y_key = 'yc' if 'yc' in robot_data else 'y'
        theta_key = 'thetac' if 'thetac' in robot_data else 'theta'
        
        if 't' not in robot_data or x_key not in robot_data or y_key not in robot_data:
            print(f"❌ 机器人{robot_id}缺少必要数据字段")
            continue
        
        # 构建CSV文件路径
        csv_file = os.path.join(output_dir, f"robot_{robot_id}_odometry.csv")
        
        try:
            with open(csv_file, 'w') as f:
                # 写入表头
                header = "time(s),x(m),y(m),theta(rad),theta(deg),vc(m/s),wc(rad/s)"
                if 'xr' in robot_data:
                    header += ",xr(m),yr(m),thetar(rad)"
                if 'xe' in robot_data:
                    header += ",xe(m),ye(m),thetae(rad)"
                f.write(header + "\n")
                
                # 写入数据
                t = robot_data['t']
                x = robot_data[x_key]
                y = robot_data[y_key]
                theta = robot_data.get(theta_key, [0]*len(t))
                vc = robot_data.get('vc', [0]*len(t))
                wc = robot_data.get('wc', [0]*len(t))
                
                for i in range(len(t)):
                    line = f"{t[i]:.6f},{x[i]:.6f},{y[i]:.6f},{theta[i]:.6f},{np.degrees(theta[i]):.2f},{vc[i]:.6f},{wc[i]:.6f}"
                    
                    if 'xr' in robot_data:
                        xr = robot_data['xr']
                        yr = robot_data['yr']
                        thetar = robot_data.get('thetar', [0]*len(t))
                        line += f",{xr[i]:.6f},{yr[i]:.6f},{thetar[i]:.6f}"
                    
                    if 'xe' in robot_data:
                        xe = robot_data['xe']
                        ye = robot_data['ye']
                        thetae = robot_data.get('thetae', [0]*len(t))
                        line += f",{xe[i]:.6f},{ye[i]:.6f},{thetae[i]:.6f}"
                    
                    f.write(line + "\n")
            
            print(f"✓ 机器人{robot_id}的数据已保存到: {csv_file}")
        
        except Exception as e:
            print(f"❌ 保存机器人{robot_id}数据时出错: {e}")


def save_leader_to_csv(data, output_dir="./output_odometry"):
    """将领导者数据保存为CSV文件"""
    
    if data is None or 'leader' not in data:
        print("❌ 数据无效或不包含领导者信息")
        return
    
    leader_data = data['leader']
    
    if leader_data is None:
        print("❌ 领导者数据为空")
        return
    
    # 创建输出目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, output_dir)
    os.makedirs(output_dir, exist_ok=True)
    
    # 检查必要字段
    if 't' not in leader_data or 'x0' not in leader_data or 'y0' not in leader_data:
        print("❌ 领导者缺少必要数据字段")
        return
    
    # 构建CSV文件路径
    csv_file = os.path.join(output_dir, "leader_data.csv")
    
    try:
        with open(csv_file, 'w') as f:
            # 写入表头
            header = "time(s),x(m),y(m),theta(rad),theta(deg),v(m/s),w(rad/s)"
            if 'u0x' in leader_data:
                header += ",u0x,u0y"
            f.write(header + "\n")
            
            # 写入数据
            t = leader_data['t']
            x = leader_data['x0']
            y = leader_data['y0']
            theta = leader_data.get('theta0', [0]*len(t))
            v = leader_data.get('v0', [0]*len(t))
            w = leader_data.get('w0', [0]*len(t))
            
            for i in range(len(t)):
                line = f"{t[i]:.6f},{x[i]:.6f},{y[i]:.6f},{theta[i]:.6f},{np.degrees(theta[i]):.2f},{v[i]:.6f},{w[i]:.6f}"
                
                if 'u0x' in leader_data:
                    u0x = leader_data['u0x']
                    u0y = leader_data['u0y']
                    line += f",{u0x[i]:.6f},{u0y[i]:.6f}"
                
                f.write(line + "\n")
        
        print(f"✓ 领导者数据已保存到: {csv_file}")
    
    except Exception as e:
        print(f"❌ 保存领导者数据时出错: {e}")


def main():
    """主函数"""
    print("\n" + "="*80)
    print("机器人里程计数据解析工具")
    print("="*80)
    
    # 加载数据
    data = load_pkl_data(PKL_FILE_PATH)
    
    if data is None:
        return
    
    # 打印数据结构
    print_data_structure(data)
    
    # 解析虚拟领导者数据
    parse_leader_data(data)
    
    # 解析所有机器人的里程计数据
    parse_robot_odometry(data, robot_ids=[0, 1, 2, 3, 4])
    
    # 保存为CSV文件
    save_leader_to_csv(data)
    save_odometry_to_csv(data, robot_ids=[0, 1, 2, 3, 4])
    
    print("\n" + "="*80)
    print("解析完成！")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()

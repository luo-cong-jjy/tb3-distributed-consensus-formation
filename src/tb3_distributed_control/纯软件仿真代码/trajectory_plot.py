#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import block_diag
import math

# 时间设置
t1 = 0.1  # 采样时间
T = 140  # 总时间
i = np.arange(1, T/t1 + 1)  # 时间序列
Rnum = 5  # 机器人数量

# 参考轨迹
aa = 0
bb = 1

# 初始化虚拟领导者控制输入
u0x = np.zeros((1, len(i)+1))
u0x[0, 0] = 0

u0y = np.zeros((1, len(i)+1))
u0y[0, 0] = 0

u0 = np.zeros((2, len(i)+1))
u0[:, 0] = np.array([u0x[0, 0], u0y[0, 0]])

# 初始化位置矩阵
x_hat = np.zeros((Rnum, len(i)+1))
y_hat = np.zeros((Rnum, len(i)+1))
x_hat[:, 0] = np.array([0.5, 0.5, 0, 0, 0])
y_hat[:, 0] = np.array([0, 1, 0.5, -0.5, -1])

# 初始化参考轨迹x和y方向坐标矩阵
xr = np.zeros((Rnum, len(i)+1))
xr[:, 0] = x_hat[:, 0]
yr = np.zeros((Rnum, len(i)+1))
yr[:, 0] = y_hat[:, 0]


# 初始化虚拟领导者角速度和线速度
w0 = np.zeros((1, len(i)+1))
w0[:, 0] = 0
v0 = np.zeros((1, len(i)+1))
v0[:, 0] = 0

# 初始化虚拟领导者位置
x0 = np.zeros((1, len(i)+1))
x0[0, 0] = 2
y0 = np.zeros((1, len(i)+1))
y0[0, 0] = 2.5
theta0 = np.zeros((1, len(i)+1))
theta0[0, 0] = 1.57

# 初始化位置偏移
px = np.zeros((Rnum,  len(i)+1))
py = np.zeros((Rnum,  len(i)+1))


# 时间序列
t = np.arange(0, T + t1, t1)

# 初始化时间变量
t2 = 0

# 主控制循环
for k in range(len(i)):

    for j in range(Rnum):
        px[j, k+1] = bb * 0.5 * np.cos(aa * t2 + ((j) * 2 * np.pi / Rnum))
        py[j, k+1] = bb * 0.5 * np.sin(aa * t2 + ((j) * 2 * np.pi / Rnum))

    # 更新参考轨迹
    x0[0, k] = x0[0, 0] + 2.5 * np.sin(t2/25)
    y0[0, k] = y0[0, 0] + 2.5 * np.sin(t2/12.5)
    
    x0[0, k+1] = x0[0, 0] + 2.5 * np.sin((t2+t1)/25)
    y0[0, k+1] = y0[0, 0] + 2.5 * np.sin((t2+t1)/12.5)
    
    # 计算参考速度
    u0x[0, k+1] = (x0[0, k+1] - x0[0, k])/t1
    u0y[0, k+1] = (y0[0, k+1] - y0[0, k])/t1
               
    # 更新控制输入
    u0[:, k+1] = np.array([u0x[0, k+1], u0y[0, k+1]])
    theta0[0, k+1] = np.arctan2(u0y[0, k+1], u0x[0, k+1])
    # print(f"Leader: k={k+1}, x0={x0[0, k+1]:.2f}, y0={y0[0, k+1]:.2f}, u0x={u0x[0, k+1]:.2f}, u0y={u0y[0, k+1]:.2f}")
    # 角度处理
    theta0_sub = 0
    flagplne0 = 0
        
    if theta0[0, k] >= np.pi/2 and theta0[0, k] <= np.pi and \
    theta0[0, k+1] <= -np.pi/2 and theta0[0, k+1] >= -np.pi:
        flagplne0 = -1
    elif theta0[0, k] <= -np.pi/2 and theta0[0, k] >= -np.pi and \
        theta0[0, k+1] >= np.pi/2 and theta0[0, k+1] <= np.pi:
        flagplne0 = 1
    
    theta0_sub = theta0[0, k] + 2 * np.pi * flagplne0
        
    # 计算角速度和线速度
    w0[0, k+1] = (theta0[0, k+1] - theta0_sub)/t1
    v0[0, k+1] = np.sqrt((x0[0, k+1] - x0[0, k])**2 + 
                        (y0[0, k+1] - y0[0, k])**2)/t1

    # 更新参考轨迹位置
    x_hat[:, k+1] = x0[:, k+1] + px[:, k]
    y_hat[:, k+1] = y0[:, k+1] + py[:, k]


    t2 = t2 + t1


# 可视化
tclc = np.array([1, int(k/2), k+1])

# 图1：机器人轨迹
plt.figure(1)
for i in range(5):
    plt.plot(xr[i, :], yr[i, :], linewidth=2)
plt.plot(x0[0, :], y0[0, :], '--', linewidth=2)

plt.axis('equal')
plt.xlabel('X coordinate(m)')
plt.ylabel('Y coordinate(m)')
plt.legend(['Robot_1', 'Robot_2', 'Robot_3', 'Robot_4', 'Robot_5', 
           'Robot_L', 'Actual centroid'])
plt.grid(True)

# 图2-3：速度图（合并显示）
plt.figure(2, figsize=(12, 5))

# 子图1：线速度
plt.subplot(1, 2, 1)
plt.plot(t, v0[0, :], '--', linewidth=2)
plt.axis([0, k*0.1, -0.51, 0.51])
plt.grid(True)
plt.xlabel('Time(s)')
plt.ylabel('Linear velocities')
plt.legend(['v_L'])

# 子图2：角速度
plt.subplot(1, 2, 2)
plt.plot(t, w0[0, :], '--', linewidth=2)
plt.axis([0, k*0.1, -2.6, 2.6])
plt.grid(True)
plt.xlabel('Time(s)')
plt.ylabel('Angular velocities')
plt.legend(['ω_L'])


# 显示所有图表
plt.show()














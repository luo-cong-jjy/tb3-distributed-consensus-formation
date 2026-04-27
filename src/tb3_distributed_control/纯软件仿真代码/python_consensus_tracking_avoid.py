#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import block_diag
import math

# 设置matplotlib允许更多图窗，避免警告
plt.rcParams['figure.max_open_warning'] = 30

def gfunction2(u):
    """
    将输入向量u的每个元素限制在ym和yp的对应范围内
    Args:
        u: 输入向量
    Returns:
        gf: 约束后的向量
    """
    global yp, ym
    gf = np.zeros_like(u)
    for i in range(len(u)):
        if u[i] > yp[i]:
            gf[i] = yp[i]
        elif u[i] < ym[i]:
            gf[i] = ym[i]
        else:
            gf[i] = u[i]
    return gf

def gfunction2z(u):
    """
    将输入向量u的每个元素限制在ymz和ypz的对应范围内
    Args:
        u: 输入向量
    Returns:
        gf: 约束后的向量
    """
    global ypz, ymz
    gf = np.zeros_like(u)
    
    for i in range(len(u)):
        if u[i] > ypz[i]:
            gf[i] = ypz[i]
        elif u[i] < ymz[i]:
            gf[i] = ymz[i]
        else:
            gf[i] = u[i]
    return gf

# 基本参数设置
N = 3  # 预测时域
Nu = 2  # 控制时域
gamma = 0.1  # 全局变量gamma，PDNN求解器参数

# 创建权重矩阵
Q = 1000000 * np.eye(10*N)  # 状态权重矩阵Q
R = 1 * np.eye(10*Nu)  # 控制权重矩阵R

# 时间设置
t1 = 0.1  # 采样时间
T = 180  # 总时间
i = np.arange(1, T/t1 + 1)  # 时间序列
Rnum = 5  # 机器人数量

# 设置邻接矩阵
A = np.array([[0, 0, 1, 0, 0],
                [1, 0, 1, 0, 0],
                [0, 0, 0, 1, 0],
                [1, 0, 0, 0, 0],
                [0, 1, 0, 0, 0]])

D = np.diag(np.sum(A, axis=1))
L = D - A
B = np.diag([1, 0, 0, 0, 0])
F = L + B
Fx = np.kron(F, np.eye(2))

# 参考轨迹
aa = 0
bb = 1

# 更新权重矩阵
em = 100
Qx = 100 * em
Qy = 1000 * em
Qtheta = 10 * em
I0 = np.eye(5*N)
Qxyt = np.array([[Qx, 0, 0],
                [0, Qy, 0],
                [0, 0, Qtheta]])
Qz = np.kron(I0, Qxyt)
Rz = 10 * np.eye(10*Nu)

# 初始化控制输入矩阵
ux = np.zeros((Rnum, len(i)+1))
uy = np.zeros((Rnum, len(i)+1))

# 初始化虚拟领导者控制输入
u0x = np.zeros((1, len(i)+1))
u0x[0, 0] = 0

u0y = np.zeros((1, len(i)+1))
u0y[0, 0] = 0

u0 = np.zeros((2, len(i)+1))
u0[:, 0] = np.array([u0x[0, 0], u0y[0, 0]])

u = np.zeros((2*Rnum, len(i)+1))

# 初始化中间变量
abaru = np.zeros((2*Rnum*Nu, len(i)+1))
detabarU = np.zeros((2*Rnum*Nu, len(i)+1))
abaruz = np.zeros((2*Rnum*Nu, len(i)+1))
detabarUz = np.zeros((2*Rnum*Nu, len(i)+1))

# 初始化GPNN状态变量
y0x = np.zeros((2*Rnum*Nu, len(i)+1))
y0z = np.zeros((2*Rnum*Nu, len(i)+1))

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

# 初始化当前位置
xc = np.zeros((Rnum, len(i)+1))
xc[:, 0] = xr[:, 0]
yc = np.zeros((Rnum, len(i)+1))
yc[:, 0] = yr[:, 0]

# 初始化误差矩阵
xe = np.zeros((Rnum, len(i)))
ye = np.zeros((Rnum, len(i)))

# 初始化角度矩阵
thetar = np.zeros((Rnum, len(i)+1))
thetac = np.zeros((Rnum, len(i)+1))
thetae = np.zeros((Rnum, len(i)+1))
thetae[:, 0] = thetar[:, 0] - thetac[:, 0]
thetae_hat = np.zeros((Rnum, len(i)+1))

# 初始化虚拟领导者角速度和线速度
w0 = np.zeros((1, len(i)+1))
w0[:, 0] = 0
v0 = np.zeros((1, len(i)+1))
v0[:, 0] = 0

# 初始化速度矩阵
vr = np.zeros((Rnum, len(i)+1))
vc = np.zeros((Rnum, len(i)+1))

wr = np.zeros((Rnum, len(i)+1))
wc = np.zeros((Rnum, len(i)+1))


# 初始化控制输入
uz = np.zeros((2*Rnum, len(i)+1))

# 初始化质心位置，即编队几何中心
xccc = np.zeros((1, len(i)+1))
xccc[0, 0] = np.sum(xc[:, 0])/Rnum
yccc = np.zeros((1, len(i)+1))
yccc[0, 0] = np.sum(yc[:, 0])/Rnum

# 初始化虚拟领导者位置
x0 = np.zeros((1, len(i)+1))
x0[0, 0] = 0.3
y0 = np.zeros((1, len(i)+1))
y0[0, 0] = 0.0
theta0 = np.zeros((1, len(i)+1))
theta0[0, 0] = 0

# 初始化误差矩阵
ex1 = np.zeros((2*Rnum, len(i)))
fx  = np.zeros((2*Rnum, len(i)))
z0 = np.zeros((2, len(i)+1))
zx = np.zeros((2*Rnum, len(i)+1))

# 初始化中间变量
L1 = np.zeros((5, 1))
L2 = np.zeros((5, 1))
L3 = np.zeros((5, 1))
M0 = np.zeros((5, 1))

# 时间序列
t = np.arange(0, T + t1, t1)

# 控制输入约束
abarUmin1 = -5 * np.ones((2*Rnum*Nu, 1))
abarUmax1 = 5 * np.ones((2*Rnum*Nu, 1))
detabarUmin = -5 * np.ones((2*Rnum*Nu, 1))
detabarUmax = 5 * np.ones((2*Rnum*Nu, 1))
abarUminz = -0.5 * np.ones((2*Rnum*Nu, 1))
abarUmaxz = 0.5 * np.ones((2*Rnum*Nu, 1))
detabarUminz = -0.5 * np.ones((2*Rnum*Nu, 1))
detabarUmaxz = 0.5 * np.ones((2*Rnum*Nu, 1))

# 位置约束
xmin = -5
xmax = 5
abarxmin = xmin * np.ones((2*Rnum*N, 1))
abarxmax = xmax * np.ones((2*Rnum*N, 1))
abarxminz = xmin * np.ones((3*Rnum*N, 1))
abarxmaxz = xmax * np.ones((3*Rnum*N, 1))

# 初始化位置偏移
px = np.zeros((Rnum,  len(i)+1))
py = np.zeros((Rnum,  len(i)+1))

# 初始化预测模型状态矩阵 fxz
fxz = np.zeros((3 * Rnum, len(i)))  # 3*Rnum=15，len(i)=1200

gzzz0 = np.eye(2)
gz0 = block_diag(gzzz0, gzzz0, gzzz0, gzzz0, gzzz0)
gx = t1 * Fx @ gz0

# 初始化时间变量
t2 = 0

# 注释掉障碍物设置部分 - 只保留轨迹跟踪
# #需大改
# # 障碍物设置
# xobs_org = np.zeros((1, 800))
# yobs_org = np.zeros((1, 800))

# # 设置圆形障碍物1
# r_of_obs1 = 0.3
# p_obs1 = np.array([1.7, 0.0]).reshape(2, 1)

# for ko in range(200):
#     theta = ko * 2 * np.pi / 200
#     xobs_org[0, ko] = p_obs1[0, 0] + r_of_obs1 * np.cos(theta)
#     yobs_org[0, ko] = p_obs1[1, 0] + r_of_obs1 * np.sin(theta)

# xyobs_org = np.zeros((2, 800))
# xyobs_org[:, :200] = np.vstack((xobs_org[:, :200], yobs_org[:, :200]))

# # 设置椭圆障碍物2
# r_of_obs2_a = 0.6
# r_of_obs2_b = 0.45
# p_obs2 = np.array([-3.0, 2.0]).reshape(2, 1)
# rot_1 = np.pi / 4

# for ko in range(200, 400):
#     theta = (ko - 1) * 2 * np.pi / 200
#     idx = ko
#     xobs_org[0, idx] = r_of_obs2_a * np.cos(theta)
#     yobs_org[0, idx] = r_of_obs2_b * np.sin(theta)

# # 旋转并平移
# pts2 = np.vstack((xobs_org[:, 200:400], yobs_org[:, 200:400]))  # shape (2,200) → stack to (4,200)?
# # 注意：MATLAB 原来是 [x; y] 变成 2×200，再右乘 2×2 旋转矩阵，这里：
# pts2_2d = pts2.reshape(2, 200)    # 重新组合成 (2,200)
# R1 = np.array([[ np.cos(rot_1),  np.sin(rot_1)],
#                [-np.sin(rot_1),  np.cos(rot_1)]])
# xyobs_rot2 = R1 @ pts2_2d + p_obs2 @ np.ones((1, 200))
# xyobs_org[:, 200:400] = xyobs_rot2

# # —— 第3段：长短边矩形 obs3 ——  
# la, lb = 1.0, 0.8
# p_obs3 = np.array([1.2, -1.5]).reshape(2, 1)
# rot_3 = -np.pi / 8

# # 先在 xobs_org/yobs_org 中填 400~600 列
# for ko in range(1, 51):
#     idx1 = 400 + ko
#     idx2 = 400 + ko + 100
#     xobs_org[0, idx1] = -la/2 + (ko-1) * la/50
#     yobs_org[0, idx1] = -lb/2
#     xobs_org[0, idx2] = la/2 - (ko-1) * la/50
#     yobs_org[0, idx2] = lb/2

# for ko in range(51, 101):
#     idx1 = 400 + ko
#     idx2 = 400 + ko + 100
#     xobs_org[0, idx1] = la/2
#     yobs_org[0, idx1] = -lb/2 + (ko-51) * lb/50
#     xobs_org[0, idx2] = -la/2
#     yobs_org[0, idx2] = -lb/2 + (ko-51) * lb/50

# # 旋转并平移
# pts3 = np.vstack((xobs_org[:, 400:600], yobs_org[:, 400:600]))
# pts3_2d = pts3.reshape(2, 200)
# R3 = np.array([[ np.cos(rot_3),  np.sin(rot_3)],
#                [-np.sin(rot_3),  np.cos(rot_3)]])
# xyobs_rot3 = R3 @ pts3_2d + p_obs3 @ np.ones((1, 200))
# xyobs_org[:, 400:600] = xyobs_rot3

# # —— 第4段：小圆 obs4 ——  
# r_of_obs4 = 0.15
# p_obs4 = np.array([0.5, 2.5]).reshape(2, 1)

# for ko in range(600, 800):
#     theta = (ko - 1) * 2 * np.pi / 200
#     xobs_org[0, ko] = p_obs4[0, 0] + r_of_obs4 * np.cos(theta)
#     yobs_org[0, ko] = p_obs4[1, 0] + r_of_obs4 * np.sin(theta)

# xyobs_org[:, 600:800] = np.vstack((xobs_org[:, 600:800], yobs_org[:, 600:800]))

# xyobs_rot = xyobs_org.copy()
# col_o, n_o = xyobs_org.shape
# xobs = xyobs_rot[0, 0:n_o]
# yobs = xyobs_rot[1, 0:n_o]

# # 初始化障碍物距离矩阵
# dobsmin = np.zeros((Rnum, len(i)))

# ord_avoid = 0.35 #用于计算避障时的距离参数
# ord_safe = 0.3 #判断是否为危险障碍物的距离阈值
# # 机器人间避碰
# dij_avoid = 0.35

# 获取矩阵gx的行数和列数
n_gx_x, m_gx_u = gx.shape
z = np.zeros((n_gx_x, m_gx_u))

# 定义步长和迭代次数
h = t1/10
n = 10

# 注释掉避障相关变量
# min_obs_num = np.zeros((Rnum,), dtype=int)
# pxy_avoid = np.zeros((2*Rnum, 1))
# d_R2R    = np.zeros((Rnum, Rnum))

# 主控制循环
for k in range(len(i)):
    # 注释掉避障相关代码
    # pxy_avoid = np.zeros((2*Rnum, 1))  # 每个ii循环前重置为零，避免累积误差

    for j in range(Rnum):
        px[j, k+1] = bb * 0.5 * np.cos(aa * t2 + ((j) * 2 * np.pi / Rnum))
        py[j, k+1] = bb * 0.5 * np.sin(aa * t2 + ((j) * 2 * np.pi / Rnum))
    
    # 注释掉障碍物距离计算和避障控制
    # # 计算障碍物距离
    # dobs = np.zeros((Rnum, n_o+1))
    
    # for ii in range(Rnum):
    #     dobsmin[ii, k] = 10000
    #     min_obs_num[ii] = 0
        
    #     for jj in range(n_o):
    #         dobs[ii, jj] = np.sqrt((xobs[jj] - xr[ii, k])**2 + 
    #                               (yobs[jj] - yr[ii, k])**2)
            
    #         if dobs[ii, jj] <= dobsmin[ii, k]:
    #             min_obs_num[ii] = jj
    #             dobsmin[ii, k] = dobs[ii, jj]
        
    #     # 避障控制
    #     if dobsmin[ii, k] <= ord_safe:
    #         jj_min = min_obs_num[ii]
    #         angle_o2r = np.arctan2(
    #             yobs[jj_min] - yr[ii, k],
    #             xobs[jj_min] - xr[ii, k]
    #         )
    #         force = (ord_avoid / dobs[ii, jj_min]) * (ord_avoid - dobs[ii, jj_min])
    #         pxy_avoid[2*ii:2*ii+2, 0] = force * np.array([np.cos(angle_o2r),
    #                                                     np.sin(angle_o2r)])
    #     else:
    #         pxy_avoid[2*ii:2*ii+2, 0] = 0
        
    #     # 机器人间避碰
    #     for jj in range(Rnum):
    #         if jj != ii:
    #             d_R2R[ii, jj] = np.sqrt((xr[jj, k] - xr[ii, k])**2 + 
    #                            (yr[jj, k] - yr[ii, k])**2)
                
    #             if d_R2R[ii, jj] <= 0.3:
    #                 angle_r2i = np.arctan2(yr[jj, k] - yr[ii, k],
    #                                      xr[jj, k] - xr[ii, k])
    #                 force_rr = (dij_avoid / d_R2R[ii, jj]) * (dij_avoid - d_R2R[ii, jj])
    #                 pxy_avoid[2*ii:2*ii+2, 0] += force_rr * np.array([np.cos(angle_r2i),
    #                                                           np.sin(angle_r2i)])
        
    #     px[ii, k+1] -= pxy_avoid[2*ii].item() 
    #     py[ii, k+1] -= pxy_avoid[2*ii+1].item() 

    # 更新参考轨迹
    x0[0, k] = x0[0, 0] + 2.5 * np.sin(t2/12.5)
    y0[0, k] = y0[0, 0] + 2.5 * np.sin(t2/25)
    
    x0[0, k+1] = x0[0, 0] + 2.5 * np.sin((t2+t1)/12.5)
    y0[0, k+1] = y0[0, 0] + 2.5 * np.sin((t2+t1)/25)
    
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
        
    # 更新状态
    for ii in range(Rnum):
        zx[ii*2:ii*2+2, k] = np.array([x_hat[ii, k] - px[ii, k+1],
                                    y_hat[ii, k] - py[ii, k+1]])
    
    z0[:, k+1] = np.array([x0[0, k+1], y0[0, k+1]])

    # 计算动态系统状态
    ex1[:, k] = Fx @ (zx[:, k] - np.kron(np.ones((Rnum)), z0[:, k+1])) 
    fx[:, k] = (ex1[:, k].reshape(-1, 1) - t1 * Fx @ np.kron(np.ones((Rnum, 1)), u0[:, k+1].reshape(-1, 1))).ravel()
    if k ==0:

        print(zx[:, k])
        print(ex1[:, k])
        print(fx[:, k])
    if k ==1:
        print(zx[:, k])
        print(ex1[:, k])
        print(fx[:, k])


    # 定义矩阵G、tildrg、tildrf和tildrI
    G = np.vstack((np.hstack((gx, z)),
                np.hstack((gx, gx)),
                np.hstack((gx, gx))))



    tildrg = np.vstack((gx @ u[:, k].reshape(-1, 1),
                        gx @ u[:, k].reshape(-1, 1),
                        gx @ u[:, k].reshape(-1, 1)))
    
    tildrf = np.vstack((fx[:, k].reshape(-1, 1),
                        fx[:, k].reshape(-1, 1),
                        fx[:, k].reshape(-1, 1)))
   
    tildrI = np.eye(Nu * m_gx_u) + np.vstack((np.zeros((10, Nu * m_gx_u)),
                                            np.hstack((np.eye(m_gx_u), np.zeros((m_gx_u, m_gx_u))))))
    
    Irnn = np.eye(Nu * n_gx_x, Nu * m_gx_u)

    # 计算二次规划问题的矩阵W、C1和E
    W = 2 * (G.T @ Q @ G + R)
    C1 = 2 * G.T @ Q @ (tildrg + tildrf)
    E = np.vstack((-tildrI, tildrI, -G, G, Irnn))
    
    # 定义约束向量b1
    b1 = np.vstack((-abarUmin1 + abaru[:, k].reshape(-1, 1),
                    abarUmax1 - abaru[:, k].reshape(-1, 1),
                    -abarxmin + tildrg + tildrf,
                    abarxmax - tildrg - tildrf))
    
    # 定义一些常量
    m = 20 * Nu + 20 * N
    myInf = 1e10

    Pinfty = myInf * np.ones((m, 1))
    Minfty = -Pinfty

    # 定义GPNN参数
    global M, p, yp, ym, ImH, IpHt, RIpHt
    p = -E @ np.linalg.inv(W) @ C1
    M = -np.linalg.inv(W) @ C1
    yp = np.vstack((b1, detabarUmax))
    ym = np.vstack((Minfty, detabarUmin))
    ImH = E @ np.linalg.inv(W) @ E.T
    IpHt = np.linalg.inv(W) @ E.T
    RIpHt = (np.linalg.inv(IpHt @ IpHt.T) @ IpHt).T

    # 初始化变量ycv
    ycv = np.zeros((2*Rnum*Nu, n+1, 1))
    for i in range(2*Rnum*Nu):
        ycv[i, 0, 0] = y0x[i, k]

        
    # 使用龙格库塔方法进行数值求解
    for ii in range(n):
        k11 = (-IpHt @ (gfunction2(ImH @ RIpHt @ (ycv[:, ii] - M) + p - RIpHt @ (ycv[:, ii] - M)) - 
                    ImH @ RIpHt @ (ycv[:, ii] - M) - p))/gamma
        k21 = (-IpHt @ (ImH @ RIpHt @ ((ycv[:, ii] + h*k11/2) - M) - 
                        gfunction2(ImH @ RIpHt @ ((ycv[:, ii] + h*k11/2) - M) - 
                                RIpHt @ ((ycv[:, ii] + h*k11/2) - M) + p) + p))/gamma
        k31 = (-IpHt @ (ImH @ RIpHt @ ((ycv[:, ii] + h*k21/2) - M) - 
                        gfunction2(ImH @ RIpHt @ ((ycv[:, ii] + h*k21/2) - M) - 
                                RIpHt @ ((ycv[:, ii] + h*k21/2) - M) + p) + p))/gamma
        k41 = (-IpHt @ (ImH @ RIpHt @ ((ycv[:, ii] + h*k31) - M) - 
                        gfunction2(ImH @ RIpHt @ ((ycv[:, ii] + h*k31) - M) - 
                                RIpHt @ ((ycv[:, ii] + h*k31) - M) + p) + p))/gamma
        ycv[:, ii+1] = ycv[:, ii] + h*(k11 + 2*k21 + 2*k31 + k41)/6

    dot_y1 = ycv[:, n]
    y0x[:, k+1] = dot_y1.ravel()
    a = y0x[:, k+1]

    detabarU[:, k+1] = a[0:10*Nu]
    dd = detabarU[:, k+1]
    abaru[:, k+1] = dd
    u[:, k+1] = dd[0:10]

    gxxz = np.zeros((15, 10))

    # 控制输入限制和轨迹更新
    for i in range(5):
        # 限制x方向输入
        if u[2*i, k+1] >= 0.22:
            u[2*i, k+1] = 0.22
        elif u[2*i, k+1] < -0.22:
            u[2*i, k+1] = -0.22

        # 限制y方向输入
        if u[2*i+1, k+1] >= 0.22:
            u[2*i+1, k+1] = 0.22
        elif u[2*i+1, k+1] < -0.22:
            u[2*i+1, k+1] = -0.22
            
        # 提取控制输入
        ux[i, k+1] = u[2*i, k+1]
        uy[i, k+1] = u[2*i+1, k+1]

        # 计算期望航向角
        thetar[i, k+1] = np.arctan2(uy[i, k+1], ux[i, k+1])
        
        # 航向角跨象限处理
        thetar_sub = 0
        flagplne = 0
        if thetar[i, k] >= np.pi/2 and thetar[i, k] <= np.pi and \
        thetar[i, k+1] <= -np.pi/2 and thetar[i, k+1] >= -np.pi:
            flagplne = -1
        elif thetar[i, k] <= -np.pi/2 and thetar[i, k] >= -np.pi and \
            thetar[i, k+1] >= np.pi/2 and thetar[i, k+1] <= np.pi:
            flagplne = 1
            
        thetar_sub = thetar[i, k] + 2 * np.pi * flagplne
        wr[i, k+1] = (thetar[i, k+1] - thetar_sub) / t1
        vr[i, k+1] = np.sqrt(ux[i, k+1]**2 + uy[i, k+1]**2)

    # 更新参考轨迹位置
    x_hat[:, k+1] = x_hat[:, k] + ux[:, k+1] * t1
    y_hat[:, k+1] = y_hat[:, k] + uy[:, k+1] * t1
    xr[:, k+1] = x_hat[:, k+1]
    yr[:, k+1] = y_hat[:, k+1]

    if k ==0:
        print("u[:, k+1]=", u[:, k+1])
    if k ==1:
        print("u[:, k+1]=", u[:, k+1])
    # 计算跟踪误差
    for i in range(5):
        xe[i, k] = np.cos(thetac[i, k]) * (xr[i, k+1] - xc[i, k]) + \
                np.sin(thetac[i, k]) * (yr[i, k+1] - yc[i, k])
        ye[i, k] = np.cos(thetac[i, k]) * (yr[i, k+1] - yc[i, k]) - \
                np.sin(thetac[i, k]) * (xr[i, k+1] - xc[i, k])
        
        # 航向角误差处理
        thetar_subc = 0
        flagplnec = 0
        if thetac[i, k] >= np.pi/2 and thetac[i, k] <= np.pi and \
        thetar[i, k+1] <= -np.pi/2 and thetar[i, k+1] >= -np.pi:
            flagplnec = -1
        elif thetac[i, k] <= -np.pi/2 and thetac[i, k] >= -np.pi and \
            thetar[i, k+1] >= np.pi/2 and thetar[i, k+1] <= np.pi:
            flagplnec = 1
        
        thetar_subc = thetac[i, k] + 2 * np.pi * flagplnec
        thetae[i, k] = thetar[i, k+1] - (thetac[i, k] + flagplnec * 2 * np.pi)
        
        # 计算中间变量
        k0 = 2 * np.sign(vr[i, k+1])
        L1[i] = np.sqrt(1 + xe[i, k]**2 + ye[i, k]**2)
        thetae_hat[i, k] = thetae[i, k] + np.arctan2(k0 * ye[i, k], L1[i].item())
        L2[i] = np.sqrt(1 + xe[i, k]**2 + (1 + k0**2) * ye[i, k]**2)
        L3[i] = np.sqrt(1 + thetae_hat[i, k]**2)
        
        # 计算非线性项
        if thetae_hat[i, k] == 0:
            alp = np.cos(thetae[i, k])
        else:
            alp = (1/thetae_hat[i, k]) * (np.sin(thetae[i, k]) + 
                np.sin(np.arctan2(k0 * ye[i, k], L1[i])))
        
        M0[i] = (k0 * vr[i, k+1] * np.sin(thetae[i, k]) * (1 + xe[i, k]**2) - 
                k0 * xe[i, k] * ye[i, k] * vr[i, k+1] * np.cos(thetae[i, k])) / \
                (L1[i] * (L2[i]**2))
                        
        # 构建预测模型矩阵
        fxz[i*3:i*3+3, k] = np.array([
            xe[i, k],
            ye[i, k],
            thetae_hat[i, k]
        ]) + t1 * np.array([
            vr[i, k+1] * np.cos(thetae[i, k]),
            vr[i, k+1] * np.sin(thetae[i, k]),
            wr[i, k+1] + M0[i].item()
        ])
        
        # 输入矩阵
        gxxz[i*3:i*3+3, i*2:i*2+2] = t1 * np.array([
            [-1, ye[i, k]],
            [0, -xe[i, k]],
            [(k0 * xe[i, k] * ye[i, k])/(L1[i] * L2[i]**2).item(), -(1 + (k0 * L1[i] * xe[i, k])/(L2[i]**2)).item()]           
                                                                                                            ])

    # 构建扩展预测模型矩阵
    zz = np.zeros((15, 10))
    Gz = np.vstack((
        np.hstack((gxxz, zz)),
        np.hstack((gxxz, gxxz)),
        np.hstack((gxxz, gxxz))
    ))

    tildrgz = np.vstack((
        gxxz @ uz[:, k].reshape(-1, 1),
        gxxz @ uz[:, k].reshape(-1, 1),
        gxxz @ uz[:, k].reshape(-1, 1)
    ))

    tildrfz = np.vstack((
        fxz[:, k].reshape(-1, 1),
        fxz[:, k].reshape(-1, 1),
        fxz[:, k].reshape(-1, 1)
    ))

    tildrIz = np.eye(20, 20) + np.vstack((
        np.zeros((10, 20)),
        np.hstack((np.eye(10, 10), np.zeros((10, 10))))
    ))

    Irnnz = np.eye(20, 20)

    # 构建QP问题
    Wz = 2 * (Gz.T @ Qz @ Gz + Rz)
    Cz = 2 * Gz.T @ Qz @ (tildrgz + tildrfz)
    Ez = np.vstack((
        -tildrIz,
        tildrIz,
        -Gz,
        Gz,
        Irnnz
    ))
    
    bz = np.vstack((
        -abarUminz + abaruz[:, k].reshape(-1, 1),
        abarUmaxz - abaruz[:, k].reshape(-1, 1),
        -abarxminz + tildrfz + tildrgz,
        abarxmaxz - tildrfz - tildrgz,
        -detabarUminz,
        detabarUmaxz
    ))

    # 定义神经网络优化参数
    mz = 20 * Nu + 30 * N
    myInfz = 1e100
    Pinftyz = myInfz * np.ones((mz, 1))
    Minftyz = -Pinftyz

    # 构建PDNN矩阵
    global Mz, pz, ypz, ymz, ImHz, IpHtz, RIpHtz
    pz = -Ez @ np.linalg.inv(Wz) @ Cz
    Mz = -np.linalg.inv(Wz) @ Cz
    ypz = np.vstack((bz, detabarUmaxz))
    ymz = np.vstack((Minftyz, detabarUminz))
    ImHz = Ez @ np.linalg.inv(Wz) @ Ez.T
    IpHtz = np.linalg.inv(Wz) @ Ez.T
    RIpHtz = (np.linalg.inv(IpHtz @ IpHtz.T) @ IpHtz).T

    # 使用龙格-库塔方法求解神经网络动态方程
    h = t1/10
    n = 10
    ycvz = np.zeros((20, n+1, 1))
    ycvz[:, 0] = y0z[:, k].reshape(-1, 1)

    for ii in range(n):
        k11 = (-IpHtz @ (ImHz @ RIpHtz @ (ycvz[:, ii] - Mz) - 
                        gfunction2z(ImHz @ RIpHtz @ (ycvz[:, ii] - Mz) - 
                                RIpHtz @ (ycvz[:, ii] - Mz) + pz) + pz))/gamma
        k21 = (-IpHtz @ (ImHz @ RIpHtz @ ((ycvz[:, ii] + h*k11/2) - Mz) - 
                        gfunction2z(ImHz @ RIpHtz @ ((ycvz[:, ii] + h*k11/2) - Mz) - 
                                RIpHtz @ ((ycvz[:, ii] + h*k11/2) - Mz) + pz) + pz))/gamma
        k31 = (-IpHtz @ (ImHz @ RIpHtz @ ((ycvz[:, ii] + h*k21/2) - Mz) - 
                        gfunction2z(ImHz @ RIpHtz @ ((ycvz[:, ii] + h*k21/2) - Mz) - 
                                RIpHtz @ ((ycvz[:, ii] + h*k21/2) - Mz) + pz) + pz))/gamma
        k41 = (-IpHtz @ (ImHz @ RIpHtz @ ((ycvz[:, ii] + h*k31) - Mz) - 
                        gfunction2z(ImHz @ RIpHtz @ ((ycvz[:, ii] + h*k31) - Mz) - 
                                RIpHtz @ ((ycvz[:, ii] + h*k31) - Mz) + pz) + pz))/gamma
        ycvz[:, ii+1] = ycvz[:, ii] + h*(k11 + 2*k21 + 2*k31 + k41)/6

    dot_y1z = ycvz[:, n]
    y0z[:, k+1] = dot_y1z.reshape(-1)
    az = y0z[:, k+1]

    detabarUz[:, k+1] = az[0:10*Nu]
    ddz = detabarUz[:, k+1]
    abaruz[:, k+1] = ddz
    uz[:, k+1] = abaruz[0:10, k+1]

    # 实际控制输入限制和更新
    for i in range(5):
        # 限制线速度
        if uz[2*i, k+1] >= 0.22:
            uz[2*i, k+1] = 0.22
        elif uz[2*i, k+1] < -0.22:
            uz[2*i, k+1] = -0.22
        
        # 限制角速度
        if uz[2*i+1, k+1] >= 2.84:
            uz[2*i+1, k+1] = 2.84
        elif uz[2*i+1, k+1] < -2.84:
            uz[2*i+1, k+1] = -2.84

        vc[i, k+1] = uz[2*i, k+1]
        wc[i, k+1] = uz[2*i+1, k+1]
        
        rrr = 0  # 模拟扰动
        # 更新机器人位姿
        thetac[i, k+1] = thetac[i, k] + t1 * wc[i, k+1]
        
        # 位姿跨象限调整
        if thetac[i, k+1] >= np.pi:
            thetac[i, k+1] = thetac[i, k+1] - 2 * np.pi
        elif thetac[i, k+1] <= -np.pi:
            thetac[i, k+1] = thetac[i, k+1] + 2 * np.pi
        
        # 更新机器人位置
        
        xc[i, k+1] = xc[i, k] + vc[i, k+1] * t1 * np.cos(thetac[i, k+1]) + \
                    (np.random.random() - 0.5) * rrr
        yc[i, k+1] = yc[i, k] + vc[i, k+1] * t1 * np.sin(thetac[i, k+1]) + \
                    (np.random.random() - 0.5) * rrr

    # 更新质心位置
    xccc[0, k+1] = np.sum(xc[:, k+1])/Rnum
    yccc[0, k+1] = np.sum(yc[:, k+1])/Rnum

    # 存储位置误差
    for ii in range(Rnum):
        zx[ii*2:ii*2+2, k+1] = np.array([
            x_hat[ii, k+1] - px[ii, k+1],
            y_hat[ii, k+1] - py[ii, k+1]
        ])

    z0[:, k+1] = np.array([x0[0, k+1], y0[0, k+1]])
    t2 = t2 + t1


# 可视化
tclc = np.array([1, int(k/2), k+1])

# 图1：机器人轨迹
plt.figure(1)
# for i in range(5):
#     plt.plot(xc[i, :], yc[i, :], linewidth=2)
plt.plot(x0[0, :], y0[0, :], '--', linewidth=2)
# plt.plot(xccc[0, :], yccc[0, :], linewidth=2)
# 注释掉障碍物绘制 - 只保留轨迹跟踪
# plt.plot(xobs, yobs, 'k.', linewidth=3)

# for j in range(3):
#     for i in range(5):
#         plt.plot([xc[i, tclc[j]], xc[(i+1)%5, tclc[j]]],
#                 [yc[i, tclc[j]], yc[(i+1)%5, tclc[j]]],
#                 color=[0.4, 0.5, 0.6], linewidth=2)

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
for i in range(5):
    plt.plot(t, vc[i, :], linewidth=2)
plt.plot(t, v0[0, :], '--', linewidth=2)
plt.axis([0, k*0.1, -0.51, 0.51])
plt.grid(True)
plt.xlabel('Time(s)')
plt.ylabel('Linear velocities')
plt.legend(['v_1', 'v_2', 'v_3', 'v_4', 'v_5', 'v_L'])

# 子图2：角速度
plt.subplot(1, 2, 2)
for i in range(5):
    plt.plot(t, wc[i, :], linewidth=2)
plt.plot(t, w0[0, :], '--', linewidth=2)
plt.axis([0, k*0.1, -2.6, 2.6])
plt.grid(True)
plt.xlabel('Time(s)')
plt.ylabel('Angular velocities')
plt.legend(['ω_1', 'ω_2', 'ω_3', 'ω_4', 'ω_5', 'ω_L'])

plt.tight_layout()

# 图4-5：位置误差图（合并显示）
plt.figure(3, figsize=(12, 5))

# 子图1：X方向误差
plt.subplot(1, 2, 1)
for i in range(5):
    plt.plot(t, xc[i, :] - z0[0, :] - px[i, :], linewidth=2)
plt.grid(True)
plt.xlabel('Time(s)')
plt.ylabel('Errors of x_i')
plt.legend(['x_1-x_L-p_1x', 'x_2-x_L-p_2x', 'x_3-x_L-p_3x', 
           'x_4-x_L-p_4x', 'x_5-x_L-p_5x'])

# 子图2：Y方向误差
plt.subplot(1, 2, 2)
for i in range(5):
    plt.plot(t, yc[i, :] - z0[1, :] - py[i, :], linewidth=2)
plt.grid(True)
plt.xlabel('Time(s)')
plt.ylabel('Errors of y_i')
plt.legend(['y_1-y_L-p_1y', 'y_2-y_L-p_2y', 'y_3-y_L-p_3y', 
           'y_4-y_L-p_4y', 'y_5-y_L-p_5y'])

plt.tight_layout()

# 图4：航向角误差
plt.figure(4)
for i in range(5):
    plt.plot(t, thetac[i, :] - theta0[0, :], linewidth=2)
plt.grid(True)
plt.xlabel('Time(s)')
plt.ylabel('Errors of θ_i')
plt.legend(['θ_1-θ_L', 'θ_2-θ_L', 'θ_3-θ_L', 'θ_4-θ_L', 'θ_5-θ_L'])

# # 图5-6：朝向角图（合并显示）
# plt.figure(5, figsize=(12, 5))

# # 子图1：实际朝向角
# plt.subplot(1, 2, 1)
# for i in range(5):
#     plt.plot(t, thetac[i, :] , linewidth=2)
# plt.grid(True)
# plt.xlabel('Time(s)')
# plt.ylabel('Actual θ_i')
# plt.legend(['θ_1', 'θ_2', 'θ_3', 'θ_4', 'θ_5'])

# # 子图2：领导者朝向角
# plt.subplot(1, 2, 2)
# plt.plot(t, theta0[0, :] , linewidth=2)
# plt.grid(True)
# plt.xlabel('Time(s)')
# plt.ylabel('Leader θ_L')
# plt.legend(['θ_L'])

# plt.tight_layout()

# # 图6-7：X方向位置图（合并显示）
# plt.figure(6, figsize=(12, 5))

# # 子图1：X方向实际位置
# plt.subplot(1, 2, 1)
# for i in range(5):
#     plt.plot(t, xc[i, :], linewidth=2)
# plt.grid(True)
# plt.xlabel('Time(s)')
# plt.ylabel('Actual x_i')
# plt.legend(['x_1', 'x_2', 'x_3', 'x_4', 'x_5'])

# # 子图2：领导者X方向位置
# plt.subplot(1, 2, 2)
# plt.plot(t, z0[0, :], linewidth=2)
# plt.grid(True)
# plt.xlabel('Time(s)')
# plt.ylabel('Leader x_L')
# plt.legend(['x_L'])

# plt.tight_layout()


# # 图7：X方向偏移
# plt.figure(7)
# for i in range(5):
#     plt.plot(t, px[i, :], linewidth=2)
# plt.grid(True)
# plt.xlabel('Time(s)')
# plt.ylabel(' px_i')
# plt.legend(['p_1x', 'p_2x', 'p_3x', 'p_4x', 'p_5x'])

# # 图8-9：Y方向位置图（合并显示）
# plt.figure(8, figsize=(12, 5))

# # 子图1：Y方向实际位置
# plt.subplot(1, 2, 1)
# for i in range(5):
#     plt.plot(t, yc[i, :] , linewidth=2)
# plt.grid(True)
# plt.xlabel('Time(s)')
# plt.ylabel('y_i')
# plt.legend(['y_1', 'y_2', 'y_3', 'y_4', 'y_5'])

# # 子图2：领导者Y方向位置
# plt.subplot(1, 2, 2)
# plt.plot(t, z0[1, :], linewidth=2)
# plt.grid(True)
# plt.xlabel('Time(s)')
# plt.ylabel('Leader y_L')
# plt.legend(['y_L'])

# plt.tight_layout()



# # 图9-10：Y方向偏移和速度图（合并显示）
# plt.figure(9, figsize=(12, 5))

# # 子图1：Y方向偏移
# plt.subplot(1, 2, 1)
# for i in range(5):
#     plt.plot(t, py[i, :], linewidth=2)
# plt.grid(True)
# plt.xlabel('Time(s)')
# plt.ylabel('py_i')
# plt.legend(['py_1', 'py_2', 'py_3', 'py_4', 'py_5'])

# # 子图2：实际线速度
# plt.subplot(1, 2, 2)
# for i in range(5):
#     plt.plot(t, vc[i, :], linewidth=2)
# plt.grid(True)
# plt.xlabel('Time(s)')
# plt.ylabel(' v_i')
# plt.legend(['v_1', 'v_2', 'v_3', 'v_4', 'v_5'])

# plt.tight_layout()

# # 图10-11：角速度和轨迹规划ux（合并显示）
# plt.figure(10, figsize=(12, 5))

# # 子图1：实际角速度
# plt.subplot(1, 2, 1)
# for i in range(5):
#     plt.plot(t, wc[i, :], linewidth=2)
# plt.grid(True)
# plt.xlabel('Time(s)')
# plt.ylabel(' ω_i')
# plt.legend(['ω_1', 'ω_2', 'ω_3', 'ω_4', 'ω_5'])

# # 子图2：轨迹规划ux
# plt.subplot(1, 2, 2)
# for i in range(5):
#     plt.plot(t, ux[i, :], linewidth=2)
# plt.grid(True)
# plt.xlabel('Time(s)')
# plt.ylabel(' u_x')
# plt.legend(['u_x1', 'u_x2', 'u_x3', 'u_x4', 'u_x5'])

# plt.tight_layout()

# # 图11-12：轨迹规划和期望位置（合并显示）
# plt.figure(11, figsize=(12, 5))

# # 子图1：轨迹规划uy
# plt.subplot(1, 2, 1)
# for i in range(5):
#     plt.plot(t, uy[i, :], linewidth=2)
# plt.grid(True)
# plt.xlabel('Time(s)')
# plt.ylabel(' u_y')
# plt.legend(['u_y1', 'u_y2', 'u_y3', 'u_y4', 'u_y5'])

# # 子图2：期望x位置
# plt.subplot(1, 2, 2)
# for i in range(5):
#     plt.plot(t, x_hat[i, :], linewidth=2)
# plt.grid(True)
# plt.xlabel('Time(s)')
# plt.ylabel(' x_hat')
# plt.legend(['x_hat1', 'x_hat2', 'x_hat3', 'x_hat4', 'x_hat5'])

# plt.tight_layout()

# # 图12-13：期望位置和状态变量（合并显示）
# plt.figure(12, figsize=(12, 5))

# # 子图1：期望y位置
# plt.subplot(1, 2, 1)
# for i in range(5):
#     plt.plot(t, y_hat[i, :], linewidth=2)
# plt.grid(True)
# plt.xlabel('Time(s)')
# plt.ylabel(' y_hat')
# plt.legend(['y_hat1', 'y_hat2', 'y_hat3', 'y_hat4', 'y_hat5'])

# # 子图2：ex1状态变量（选择前5个显示）
# plt.subplot(1, 2, 2)
# for i in range(5):
#     plt.plot(t[:-1], ex1[i, :], linewidth=2)
# plt.grid(True)
# plt.xlabel('Time(s)')
# plt.ylabel(' ex1')
# plt.legend(['ex1_1', 'ex1_2', 'ex1_3', 'ex1_4', 'ex1_5'])

# plt.tight_layout()

# # 图13：fx状态变量
# plt.figure(13)
# for i in range(10):
#     plt.plot(t[:-1], fx[i, :], linewidth=2)
# plt.grid(True)
# plt.xlabel('Time(s)')
# plt.ylabel(' fx')
# plt.legend(['fx_1', 'fx_2', 'fx_3', 'fx_4', 'fx_5', 'fx_6', 'fx_7', 'fx_8', 'fx_9', 'fx_10'])

# 显示所有图表
plt.show()

























# 注释掉障碍物距离图 - 只保留轨迹跟踪
# # 图7：障碍物最小距离
# plt.figure(7)
# for i in range(5):
#     plt.plot(t[0:k+1], dobsmin[i, :], linewidth=2)
# plt.xlabel('Time(s)')
# plt.ylabel('Min distance of obstacle')
# plt.legend(['dobsmin_1', 'dobsmin_2', 'dobsmin_3', 'dobsmin_4', 'dobsmin_5'])

# plt.show()
#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import block_diag
import math

def gfunction2_1(u):
    """
    将输入向量u的每个元素限制在ym和yp的对应范围内
    Args:
        u: 输入向量
    Returns:
        gf: 约束后的向量
    """
    global yp_1, ym_1
    gf = np.zeros_like(u)
    for i in range(len(u)):
        if u[i] > yp_1[i]:
            gf[i] = yp_1[i]
        elif u[i] < ym_1[i]:
            gf[i] = ym_1[i]
        else:
            gf[i] = u[i]
    return gf

def gfunction2z_1(u):
    """
    将输入向量u的每个元素限制在ymz和ypz的对应范围内
    Args:
        u: 输入向量
    Returns:
        gf: 约束后的向量
    """
    global ypz_1, ymz_1
    gf = np.zeros_like(u)
    
    for i in range(len(u)):
        if u[i] > ypz_1[i]:
            gf[i] = ypz_1[i]
        elif u[i] < ymz_1[i]:
            gf[i] = ymz_1[i]
        else:
            gf[i] = u[i]
    return gf

def gfunction2_2(u):
    """
    将输入向量u的每个元素限制在ym和yp的对应范围内
    Args:
        u: 输入向量
    Returns:
        gf: 约束后的向量
    """
    global yp_2, ym_2
    gf = np.zeros_like(u)
    for i in range(len(u)):
        if u[i] > yp_2[i]:
            gf[i] = yp_2[i]
        elif u[i] < ym_2[i]:
            gf[i] = ym_2[i]
        else:
            gf[i] = u[i]
    return gf

def gfunction2z_2(u):
    """
    将输入向量u的每个元素限制在ymz和ypz的对应范围内
    Args:
        u: 输入向量
    Returns:
        gf: 约束后的向量
    """
    global ypz_2, ymz_2
    gf = np.zeros_like(u)
    
    for i in range(len(u)):
        if u[i] > ypz_2[i]:
            gf[i] = ypz_2[i]
        elif u[i] < ymz_2[i]:
            gf[i] = ymz_2[i]
        else:
            gf[i] = u[i]
    return gf

def gfunction2_3(u):
    """
    将输入向量u的每个元素限制在ym和yp的对应范围内
    Args:
        u: 输入向量
    Returns:
        gf: 约束后的向量
    """
    global yp_3, ym_3
    gf = np.zeros_like(u)
    for i in range(len(u)):
        if u[i] > yp_3[i]:
            gf[i] = yp_3[i]
        elif u[i] < ym_3[i]:
            gf[i] = ym_3[i]
        else:
            gf[i] = u[i]
    return gf

def gfunction2z_3(u):
    """
    将输入向量u的每个元素限制在ymz和ypz的对应范围内
    Args:
        u: 输入向量
    Returns:
        gf: 约束后的向量
    """
    global ypz_3, ymz_3
    gf = np.zeros_like(u)
    
    for i in range(len(u)):
        if u[i] > ypz_3[i]:
            gf[i] = ypz_3[i]
        elif u[i] < ymz_3[i]:
            gf[i] = ymz_3[i]
        else:
            gf[i] = u[i]
    return gf

def gfunction2_4(u):
    """
    将输入向量u的每个元素限制在ym和yp的对应范围内
    Args:
        u: 输入向量
    Returns:
        gf: 约束后的向量
    """
    global yp_4, ym_4
    gf = np.zeros_like(u)
    for i in range(len(u)):
        if u[i] > yp_4[i]:
            gf[i] = yp_4[i]
        elif u[i] < ym_4[i]:
            gf[i] = ym_4[i]
        else:
            gf[i] = u[i]
    return gf

def gfunction2z_4(u):
    """
    将输入向量u的每个元素限制在ymz和ypz的对应范围内
    Args:
        u: 输入向量
    Returns:
        gf: 约束后的向量
    """
    global ypz_4, ymz_4
    gf = np.zeros_like(u)
    
    for i in range(len(u)):
        if u[i] > ypz_4[i]:
            gf[i] = ypz_4[i]
        elif u[i] < ymz_4[i]:
            gf[i] = ymz_4[i]
        else:
            gf[i] = u[i]
    return gf

def gfunction2_5(u):
    """
    将输入向量u的每个元素限制在ym和yp的对应范围内
    Args:
        u: 输入向量
    Returns:
        gf: 约束后的向量
    """
    global yp_5, ym_5
    gf = np.zeros_like(u)
    for i in range(len(u)):
        if u[i] > yp_5[i]:
            gf[i] = yp_5[i]
        elif u[i] < ym_5[i]:
            gf[i] = ym_5[i]
        else:
            gf[i] = u[i]
    return gf

def gfunction2z_5(u):
    """
    将输入向量u的每个元素限制在ymz和ypz的对应范围内
    Args:
        u: 输入向量
    Returns:
        gf: 约束后的向量
    """
    global ypz_5, ymz_5
    gf = np.zeros_like(u)
    
    for i in range(len(u)):
        if u[i] > ypz_5[i]:
            gf[i] = ypz_5[i]
        elif u[i] < ymz_5[i]:
            gf[i] = ymz_5[i]
        else:
            gf[i] = u[i]
    return gf



# 基本参数设置
N = 3  # 预测时域
Nu = 2  # 控制时域
gamma = 0.1  # 全局变量gamma，PDNN求解器参数

# 创建权重矩阵
Q_1 = 1000000000 * np.eye(2*N)  # 状态权重矩阵Q
R_1 = 10000 * np.eye(2*Nu)  # 控制权重矩阵R

Q_2 = 1000000000 * np.eye(2*N)  # 状态权重矩阵Q
R_2 = 10000 * np.eye(2*Nu)  # 控制权重矩阵R

Q_3 = 1000000000 * np.eye(2*N)  # 状态权重矩阵Q
R_3 = 10000 * np.eye(2*Nu)  # 控制权重矩阵R

Q_4 = 1000000000 * np.eye(2*N)  # 状态权重矩阵Q
R_4 = 10000 * np.eye(2*Nu)  # 控制权重矩阵R

Q_5 = 1000000000 * np.eye(2*N)  # 状态权重矩阵Q
R_5 = 10000 * np.eye(2*Nu)  # 控制权重矩阵R


# 时间设置
t1 = 0.1  # 采样时间
T = 180  # 总时间
i = np.arange(1, T/t1 + 1)  # 时间序列
Rnum = 5  # 机器人数量

# 设置邻接矩阵

# A = np.array([[0, 0, 1, 0, 0],
#               [1, 0, 1, 0, 0],
#               [0, 0, 0, 1, 0],
#               [1, 0, 0, 0, 0],
#               [0, 1, 0, 0, 0]])

# 现在观测器部分已经支持动态邻接矩阵，可以直接修改A矩阵来切换拓扑
# 例如：
A = np.array([[0, 0, 0, 0, 0],
              [1, 0, 0, 0, 0],
              [0, 1, 0, 0, 0],
              [0, 0, 1, 0, 0],
              [0, 0, 0, 1, 0]])

D = np.diag(np.sum(A, axis=1))
L = D - A
B = np.diag([1, 0, 0, 0, 0])
F = L + B
Fx = np.kron(F, np.eye(2))


Fx_1 = F[0,0]*np.eye(2)

Fx_2 = F[1,1]*np.eye(2)

Fx_3 = F[2,2]*np.eye(2)

Fx_4 = F[3,3]*np.eye(2)

Fx_5 = F[4,4]*np.eye(2)


# 参考轨迹
aa = 0
bb = 1

# 更新权重矩阵
em = 100
Qx = 1000 * em
Qy = 1000 * em
Qtheta = 10 * em
I0 = np.eye(1*N)
Qxyt = np.array([[Qx, 0, 0],
                [0, Qy, 0],
                [0, 0, Qtheta]])
Qz = np.kron(I0, Qxyt)
Rz = 10 * np.eye(2*Nu)

# 初始化控制输入矩阵
ux1 = np.zeros((1, len(i)+1))
uy1 = np.zeros((1, len(i)+1))

ux2 = np.zeros((1, len(i)+1))
uy2 = np.zeros((1, len(i)+1))

ux3 = np.zeros((1, len(i)+1))
uy3 = np.zeros((1, len(i)+1))

ux4 = np.zeros((1, len(i)+1))
uy4 = np.zeros((1, len(i)+1))

ux5 = np.zeros((1, len(i)+1))
uy5 = np.zeros((1, len(i)+1))

# 初始化虚拟领导者控制输入
u0x = np.zeros((1, len(i)+1))
u0x[0, 0] = 0

u0y = np.zeros((1, len(i)+1))
u0y[0, 0] = 0

u0 = np.zeros((2, len(i)+1))
u0[:, 0] = np.array([u0x[0, 0], u0y[0, 0]])

u1 = np.zeros((2, len(i)+1))

u2 = np.zeros((2, len(i)+1))

u3 = np.zeros((2, len(i)+1))

u4 = np.zeros((2, len(i)+1))

u5 = np.zeros((2, len(i)+1))

# 初始化中间变量
abaru1 = np.zeros((2*Nu, len(i)+1))
detabarU1 = np.zeros((2*Nu, len(i)+1))
abaruz1 = np.zeros((2*Nu, len(i)+1))
detabarUz1 = np.zeros((2*Nu, len(i)+1))

# 初始化GPNN状态变量
y0x1 = np.zeros((2*Nu, len(i)+1))
y0z1 = np.zeros((2*Nu, len(i)+1))

abaru2 = np.zeros((2*Nu, len(i)+1))
detabarU2 = np.zeros((2*Nu, len(i)+1))
abaruz2 = np.zeros((2*Nu, len(i)+1))
detabarUz2 = np.zeros((2*Nu, len(i)+1))

# 初始化GPNN状态变量
y0x2 = np.zeros((2*Nu, len(i)+1))
y0z2 = np.zeros((2*Nu, len(i)+1))

abaru3 = np.zeros((2*Nu, len(i)+1))
detabarU3 = np.zeros((2*Nu, len(i)+1))
abaruz3 = np.zeros((2*Nu, len(i)+1))
detabarUz3 = np.zeros((2*Nu, len(i)+1))

# 初始化GPNN状态变量
y0x3 = np.zeros((2*Nu, len(i)+1))
y0z3 = np.zeros((2*Nu, len(i)+1))

abaru4 = np.zeros((2*Nu, len(i)+1))
detabarU4 = np.zeros((2*Nu, len(i)+1))
abaruz4 = np.zeros((2*Nu, len(i)+1))
detabarUz4 = np.zeros((2*Nu, len(i)+1))

# 初始化GPNN状态变量
y0x4 = np.zeros((2*Nu, len(i)+1))
y0z4 = np.zeros((2*Nu, len(i)+1))

abaru5 = np.zeros((2*Nu, len(i)+1))
detabarU5 = np.zeros((2*Nu, len(i)+1))
abaruz5 = np.zeros((2*Nu, len(i)+1))
detabarUz5 = np.zeros((2*Nu, len(i)+1))

# 初始化GPNN状态变量
y0x5 = np.zeros((2*Nu, len(i)+1))
y0z5 = np.zeros((2*Nu, len(i)+1))


# 初始化位置矩阵
x_hat1 = np.zeros((1, len(i)+1))
y_hat1 = np.zeros((1, len(i)+1))
x_hat1[:, 0] = 0.5
y_hat1[:, 0] = 0

x_hat2 = np.zeros((1, len(i)+1))
y_hat2 = np.zeros((1, len(i)+1))
x_hat2[:, 0] = 0.5
y_hat2[:, 0] = 1

x_hat3 = np.zeros((1, len(i)+1))
y_hat3 = np.zeros((1, len(i)+1))
x_hat3[:, 0] = 0
y_hat3[:, 0] = 0.5

x_hat4 = np.zeros((1, len(i)+1))
y_hat4 = np.zeros((1, len(i)+1))
x_hat4[:, 0] = 0
y_hat4[:, 0] = -0.5

x_hat5 = np.zeros((1, len(i)+1))
y_hat5 = np.zeros((1, len(i)+1))
x_hat5[:, 0] = 0
y_hat5[:, 0] = -1


# 初始化参考轨迹x和y方向坐标矩阵
xr1 = np.zeros((1, len(i)+1))
xr1[:, 0] = x_hat1[:, 0]
yr1 = np.zeros((1, len(i)+1))
yr1[:, 0] = y_hat1[:, 0]

xr2 = np.zeros((1, len(i)+1))
xr2[:, 0] = x_hat2[:, 0]
yr2 = np.zeros((1, len(i)+1))
yr2[:, 0] = y_hat2[:, 0]

xr3 = np.zeros((1, len(i)+1))
xr3[:, 0] = x_hat3[:, 0]
yr3 = np.zeros((1, len(i)+1))
yr3[:, 0] = y_hat3[:, 0]

xr4 = np.zeros((1, len(i)+1))
xr4[:, 0] = x_hat4[:, 0]
yr4 = np.zeros((1, len(i)+1))
yr4[:, 0] = y_hat4[:, 0]

xr5 = np.zeros((1, len(i)+1))
xr5[:, 0] = x_hat5[:, 0]
yr5 = np.zeros((1, len(i)+1))
yr5[:, 0] = y_hat5[:, 0]

# 初始化当前位置
xc1 = np.zeros((1, len(i)+1))
xc1[:, 0] = xr1[:, 0]
yc1 = np.zeros((1, len(i)+1))
yc1[:, 0] = yr1[:, 0]

xc2 = np.zeros((1, len(i)+1))
xc2[:, 0] = xr2[:, 0]
yc2 = np.zeros((1, len(i)+1))
yc2[:, 0] = yr2[:, 0]

xc3 = np.zeros((1, len(i)+1))
xc3[:, 0] = xr3[:, 0]
yc3 = np.zeros((1, len(i)+1))
yc3[:, 0] = yr3[:, 0]

xc4 = np.zeros((1, len(i)+1))
xc4[:, 0] = xr4[:, 0]
yc4 = np.zeros((1, len(i)+1))
yc4[:, 0] = yr4[:, 0]

xc5 = np.zeros((1, len(i)+1))
xc5[:, 0] = xr5[:, 0]
yc5 = np.zeros((1, len(i)+1))
yc5[:, 0] = yr5[:, 0]

# 初始化误差矩阵
xe1 = np.zeros((1, len(i)))
ye1 = np.zeros((1, len(i)))

xe2 = np.zeros((1, len(i)))
ye2 = np.zeros((1, len(i)))

xe3 = np.zeros((1, len(i)))
ye3 = np.zeros((1, len(i)))

xe4 = np.zeros((1, len(i)))
ye4 = np.zeros((1, len(i)))

xe5 = np.zeros((1, len(i)))
ye5 = np.zeros((1, len(i)))

# 初始化角度矩阵
thetar1 = np.zeros((1, len(i)+1))
thetac1 = np.zeros((1, len(i)+1))
thetae1 = np.zeros((1, len(i)+1))
thetae1[:, 0] = thetar1[:, 0] - thetac1[:, 0]
thetae_hat1 = np.zeros((1, len(i)+1))

thetar2 = np.zeros((1, len(i)+1))
thetac2 = np.zeros((1, len(i)+1))
thetae2 = np.zeros((1, len(i)+1))
thetae2[:, 0] = thetar2[:, 0] - thetac2[:, 0]
thetae_hat2 = np.zeros((1, len(i)+1))

thetar3 = np.zeros((1, len(i)+1))
thetac3 = np.zeros((1, len(i)+1))
thetae3 = np.zeros((1, len(i)+1))
thetae3[:, 0] = thetar3[:, 0] - thetac3[:, 0]
thetae_hat3 = np.zeros((1, len(i)+1))

thetar4 = np.zeros((1, len(i)+1))
thetac4 = np.zeros((1, len(i)+1))
thetae4 = np.zeros((1, len(i)+1))
thetae4[:, 0] = thetar4[:, 0] - thetac4[:, 0]
thetae_hat4 = np.zeros((1, len(i)+1))

thetar5 = np.zeros((1, len(i)+1))
thetac5 = np.zeros((1, len(i)+1))
thetae5 = np.zeros((1, len(i)+1))
thetae5[:, 0] = thetar5[:, 0] - thetac5[:, 0]
thetae_hat5 = np.zeros((1, len(i)+1))


# 初始化虚拟领导者角速度和线速度
w0 = np.zeros((1, len(i)+1))
w0[:, 0] = 0
v0 = np.zeros((1, len(i)+1))
v0[:, 0] = 0

# 初始化速度矩阵
vr1 = np.zeros((1, len(i)+1))
vc1 = np.zeros((1, len(i)+1))
ve1 = np.zeros((1, len(i)+1))
wr1 = np.zeros((1, len(i)+1))
wc1 = np.zeros((1, len(i)+1))
we1 = np.zeros((1, len(i)+1))

vr2 = np.zeros((1, len(i)+1))
vc2 = np.zeros((1, len(i)+1))
ve2 = np.zeros((1, len(i)+1))
wr2 = np.zeros((1, len(i)+1))
wc2 = np.zeros((1, len(i)+1))
we2 = np.zeros((1, len(i)+1))

vr3 = np.zeros((1, len(i)+1))
vc3 = np.zeros((1, len(i)+1))
ve3 = np.zeros((1, len(i)+1))
wr3 = np.zeros((1, len(i)+1))
wc3 = np.zeros((1, len(i)+1))
we3 = np.zeros((1, len(i)+1))

vr4 = np.zeros((1, len(i)+1))
vc4 = np.zeros((1, len(i)+1))
ve4 = np.zeros((1, len(i)+1))
wr4 = np.zeros((1, len(i)+1))
wc4 = np.zeros((1, len(i)+1))
we4 = np.zeros((1, len(i)+1))

vr5 = np.zeros((1, len(i)+1))
vc5 = np.zeros((1, len(i)+1))
ve5 = np.zeros((1, len(i)+1))
wr5 = np.zeros((1, len(i)+1))
wc5 = np.zeros((1, len(i)+1))
we5 = np.zeros((1, len(i)+1))


# 初始化控制输入
uz1 = np.zeros((2, len(i)+1))

uz2 = np.zeros((2, len(i)+1))

uz3 = np.zeros((2, len(i)+1))

uz4 = np.zeros((2, len(i)+1))

uz5 = np.zeros((2, len(i)+1))


# 初始化质心位置，即编队几何中心
xccc = np.zeros((1, len(i)+1))
xccc[0, 0] = np.sum(xc1[:, 0]+xc2[:, 0]+xc3[:, 0]+xc4[:, 0]+xc5[:, 0])/Rnum
yccc = np.zeros((1, len(i)+1))
yccc[0, 0] = np.sum(yc1[:, 0]+yc2[:, 0]+yc3[:, 0]+yc4[:, 0]+yc5[:, 0])/Rnum

# 初始化虚拟领导者位置
x0 = np.zeros((1, len(i)+1))
x0[0, 0] = 0.3
y0 = np.zeros((1, len(i)+1))
y0[0, 0] = 0.0
theta0 = np.zeros((1, len(i)+1))
theta0[0, 0] = 0

z0 = np.zeros((2, len(i)+1))

# 初始化误差矩阵
ex1 = np.zeros((2, len(i)))
fx1  = np.zeros((2, len(i)))
zx1 = np.zeros((2, len(i)+1))

ex2 = np.zeros((2, len(i)))
fx2  = np.zeros((2, len(i)))
zx2 = np.zeros((2, len(i)+1))

ex3 = np.zeros((2, len(i)))
fx3  = np.zeros((2, len(i)))
zx3 = np.zeros((2, len(i)+1))

ex4 = np.zeros((2, len(i)))
fx4  = np.zeros((2, len(i)))
zx4 = np.zeros((2, len(i)+1))

ex5 = np.zeros((2, len(i)))
fx5  = np.zeros((2, len(i)))
zx5 = np.zeros((2, len(i)+1))

# 初始化中间变量
L1_1=0
L2_1=0
L3_1=0
M0_1=0


L1_2=0
L2_2=0
L3_2=0
M0_2=0


L1_3=0
L2_3=0
L3_3=0
M0_3=0


L1_4=0
L2_4=0
L3_4=0
M0_4=0


L1_5=0
L2_5=0
L3_5=0
M0_5=0

# 时间序列
t = np.arange(0, T + t1, t1)

# 控制输入约束
abarUmin11 = -5 * np.ones((2*Nu, 1))
abarUmax11 = 5 * np.ones((2*Nu, 1))
detabarUmin1 = -5 * np.ones((2*Nu, 1))
detabarUmax1 = 5 * np.ones((2*Nu, 1))
abarUminz1 = -0.5 * np.ones((2*Nu, 1))
abarUmaxz1 = 0.5 * np.ones((2*Nu, 1))
detabarUminz1 = -0.5 * np.ones((2*Nu, 1))
detabarUmaxz1 = 0.5 * np.ones((2*Nu, 1))

abarUmin12 = -5 * np.ones((2*Nu, 1))
abarUmax12 = 5 * np.ones((2*Nu, 1))
detabarUmin2 = -5 * np.ones((2*Nu, 1))
detabarUmax2 = 5 * np.ones((2*Nu, 1))
abarUminz2 = -0.5 * np.ones((2*Nu, 1))
abarUmaxz2 = 0.5 * np.ones((2*Nu, 1))
detabarUminz2 = -0.5 * np.ones((2*Nu, 1))
detabarUmaxz2 = 0.5 * np.ones((2*Nu, 1))

abarUmin13 = -5 * np.ones((2*Nu, 1))
abarUmax13 = 5 * np.ones((2*Nu, 1))
detabarUmin3 = -5 * np.ones((2*Nu, 1))
detabarUmax3 = 5 * np.ones((2*Nu, 1))
abarUminz3 = -0.5 * np.ones((2*Nu, 1))
abarUmaxz3 = 0.5 * np.ones((2*Nu, 1))
detabarUminz3 = -0.5 * np.ones((2*Nu, 1))
detabarUmaxz3 = 0.5 * np.ones((2*Nu, 1))

abarUmin14 = -5 * np.ones((2*Nu, 1))
abarUmax14 = 5 * np.ones((2*Nu, 1))
detabarUmin4 = -5 * np.ones((2*Nu, 1))
detabarUmax4 = 5 * np.ones((2*Nu, 1))
abarUminz4 = -0.5 * np.ones((2*Nu, 1))
abarUmaxz4 = 0.5 * np.ones((2*Nu, 1))
detabarUminz4 = -0.5 * np.ones((2*Nu, 1))
detabarUmaxz4 = 0.5 * np.ones((2*Nu, 1))

abarUmin15 = -5 * np.ones((2*Nu, 1))
abarUmax15 = 5 * np.ones((2*Nu, 1))
detabarUmin5 = -5 * np.ones((2*Nu, 1))
detabarUmax5 = 5 * np.ones((2*Nu, 1))
abarUminz5 = -0.5 * np.ones((2*Nu, 1))
abarUmaxz5 = 0.5 * np.ones((2*Nu, 1))
detabarUminz5 = -0.5 * np.ones((2*Nu, 1))
detabarUmaxz5 = 0.5 * np.ones((2*Nu, 1))


# 位置约束
xmin = -5
xmax = 5

abarxmin1 = xmin * np.ones((2*N, 1))
abarxmax1 = xmax * np.ones((2*N, 1))
abarxminz1 = xmin * np.ones((3*N, 1))
abarxmaxz1 = xmax * np.ones((3*N, 1))

abarxmin2 = xmin * np.ones((2*N, 1))
abarxmax2 = xmax * np.ones((2*N, 1))
abarxminz2 = xmin * np.ones((3*N, 1))
abarxmaxz2 = xmax * np.ones((3*N, 1))

abarxmin3 = xmin * np.ones((2*N, 1))
abarxmax3 = xmax * np.ones((2*N, 1))
abarxminz3 = xmin * np.ones((3*N, 1))
abarxmaxz3 = xmax * np.ones((3*N, 1))

abarxmin4 = xmin * np.ones((2*N, 1))
abarxmax4 = xmax * np.ones((2*N, 1))
abarxminz4 = xmin * np.ones((3*N, 1))
abarxmaxz4 = xmax * np.ones((3*N, 1))

abarxmin5 = xmin * np.ones((2*N, 1))
abarxmax5 = xmax * np.ones((2*N, 1))
abarxminz5 = xmin * np.ones((3*N, 1))
abarxmaxz5 = xmax * np.ones((3*N, 1))

# 初始化位置偏移
px1 = np.zeros((1,  len(i)+1))
py1 = np.zeros((1,  len(i)+1))

px2 = np.zeros((1,  len(i)+1))
py2 = np.zeros((1,  len(i)+1))

px3 = np.zeros((1,  len(i)+1))
py3 = np.zeros((1,  len(i)+1))

px4 = np.zeros((1,  len(i)+1))
py4 = np.zeros((1,  len(i)+1))

px5 = np.zeros((1,  len(i)+1))
py5 = np.zeros((1,  len(i)+1))

# 初始化预测模型状态矩阵 fxz
fxz_1 = np.zeros((3, len(i)))  # 3*Rnum=15，len(i)=1200

fxz_2 = np.zeros((3, len(i)))

fxz_3 = np.zeros((3, len(i)))

fxz_4 = np.zeros((3, len(i)))

fxz_5 = np.zeros((3, len(i)))

gz0 = np.eye(2)

gx_1 = t1 * Fx_1 @ gz0

gx_2 = t1 * Fx_2 @ gz0

gx_3 = t1 * Fx_3 @ gz0

gx_4 = t1 * Fx_4 @ gz0

gx_5 = t1 * Fx_5 @ gz0

# 初始化时间变量
t2 = 0


# 获取矩阵gx的行数和列数
n_gx_x, m_gx_u = gx_1.shape

z_1 = np.zeros((n_gx_x, m_gx_u))

z_2 = np.zeros((n_gx_x, m_gx_u))

z_3 = np.zeros((n_gx_x, m_gx_u))

z_4 = np.zeros((n_gx_x, m_gx_u))

z_5 = np.zeros((n_gx_x, m_gx_u))

# 定义步长和迭代次数
h = t1/10
n = 10

# 领导者分布式观测器相关初始化
# 定义领导者的观测器估计，这里的zxeo_i代表第i个机器人（agent）对leader在时间k时刻的状态估计,dzxeo_i是这些状态估计的离散时间导数
# 观测器估计变量（每个机器人一组）
zxeo_1 = np.zeros((2, len(i)+1))
dzxeo_1 = np.zeros((2, len(i)+1))

zxeo_2 = np.zeros((2, len(i)+1))
dzxeo_2 = np.zeros((2, len(i)+1))

zxeo_3 = np.zeros((2, len(i)+1))
dzxeo_3 = np.zeros((2, len(i)+1))

zxeo_4 = np.zeros((2, len(i)+1))
dzxeo_4 = np.zeros((2, len(i)+1))

zxeo_5 = np.zeros((2, len(i)+1))
dzxeo_5 = np.zeros((2, len(i)+1))

# 分布式观测器参数
ob_eta = 0.6
ob_alp = 0.8


# 🚀 Python语法改造：将单独变量组织成列表，便于避障时机器人之间距离计算索引访问
xr = [xr1, xr2, xr3, xr4, xr5]  # 索引0-4对应xr1-xr5
yr = [yr1, yr2, yr3, yr4, yr5]  # 索引0-4对应yr1-yr5

#障碍物设置 - 根据Gazebo世界场景配置
# 基于consensus_obstacle_2.world中的28个障碍物设置
# 每个障碍物用20个点来描绘边界

# 初始化障碍物存储矩阵 (28个障碍物 × 20个点/障碍物 = 560个点)
n_obstacles = 28
points_per_obstacle = 20
total_points = n_obstacles * points_per_obstacle

xobs_org = np.zeros((1, total_points))
yobs_org = np.zeros((1, total_points))
xyobs_org = np.zeros((2, total_points))

# 定义所有障碍物的配置信息
obstacles_config = [
    # 圆柱形障碍物 (14个)
    {'name': 'obs_cylinder1', 'type': 'cylinder', 'x': -2.50, 'y': 1.80, 'radius': 0.150},
    {'name': 'obs_cylinder2', 'type': 'cylinder', 'x': 0.80, 'y': 3.10, 'radius': 0.120},
    {'name': 'obs_cylinder3', 'type': 'cylinder', 'x': 2.10, 'y': 2.30, 'radius': 0.180},
    {'name': 'obs_cylinder4', 'type': 'cylinder', 'x': 1.50, 'y': -0.80, 'radius': 0.140},
    {'name': 'obs_cylinder5', 'type': 'cylinder', 'x': 3.00, 'y': 0.90, 'radius': 0.160},
    {'name': 'obs_cylinder6', 'type': 'cylinder', 'x': -2.80, 'y': -1.10, 'radius': 0.110},
    {'name': 'obs_cylinder7', 'type': 'cylinder', 'x': -3.20, 'y': 3.00, 'radius': 0.130},
    {'name': 'obs_cylinder8', 'type': 'cylinder', 'x': 3.50, 'y': 2.10, 'radius': 0.170},
    {'name': 'obs_cylinder9', 'type': 'cylinder', 'x': -1.80, 'y': -3.50, 'radius': 0.190},
    {'name': 'obs_cylinder10', 'type': 'cylinder', 'x': 0.30, 'y': -1.20, 'radius': 0.100},
    {'name': 'obs_cylinder11', 'type': 'cylinder', 'x': -3.80, 'y': -2.20, 'radius': 0.140},
    {'name': 'obs_cylinder12', 'type': 'cylinder', 'x': 2.80, 'y': 3.60, 'radius': 0.120},
    {'name': 'obs_cylinder13', 'type': 'cylinder', 'x': -1.50, 'y': 0.80, 'radius': 0.160},
    {'name': 'obs_cylinder14', 'type': 'cylinder', 'x': 0.70, 'y': 1.80, 'radius': 0.110},
    
    # 方形障碍物 (14个) - 包括长方形和正方形
    {'name': 'obs_box1', 'type': 'box', 'x': 3.20, 'y': -1.50, 'width': 0.250, 'height': 0.350},
    {'name': 'obs_box2', 'type': 'box', 'x': -1.20, 'y': -2.80, 'width': 0.180, 'height': 0.320},
    {'name': 'obs_box3', 'type': 'box', 'x': -3.50, 'y': 0.20, 'width': 0.300, 'height': 0.150},
    {'name': 'obs_box4', 'type': 'box', 'x': -0.50, 'y': 1.20, 'width': 0.220, 'height': 0.280},
    {'name': 'obs_box5', 'type': 'box', 'x': 0.20, 'y': -3.20, 'width': 0.350, 'height': 0.200},
    {'name': 'obs_box6', 'type': 'box', 'x': 2.70, 'y': -2.90, 'width': 0.120, 'height': 0.380},
    {'name': 'obs_square7', 'type': 'box', 'x': -2.00, 'y': 2.80, 'width': 0.250, 'height': 0.250},
    {'name': 'obs_square8', 'type': 'box', 'x': 3.80, 'y': -0.50, 'width': 0.180, 'height': 0.180},
    {'name': 'obs_square9', 'type': 'box', 'x': -0.80, 'y': 3.70, 'width': 0.320, 'height': 0.320},
    {'name': 'obs_square10', 'type': 'box', 'x': 1.30, 'y': -3.00, 'width': 0.150, 'height': 0.150},
    {'name': 'obs_square11', 'type': 'box', 'x': -2.70, 'y': -0.30, 'width': 0.280, 'height': 0.280},
    {'name': 'obs_square12', 'type': 'box', 'x': 3.20, 'y': 1.20, 'width': 0.200, 'height': 0.200},
    {'name': 'obs_square13', 'type': 'box', 'x': -0.20, 'y': -2.10, 'width': 0.350, 'height': 0.350},
    {'name': 'obs_square14', 'type': 'box', 'x': 1.80, 'y': 0.30, 'width': 0.220, 'height': 0.220},
]

# 生成所有障碍物的边界点
for obs_idx, obs in enumerate(obstacles_config):
    start_idx = obs_idx * points_per_obstacle
    end_idx = (obs_idx + 1) * points_per_obstacle
    
    if obs['type'] == 'cylinder':
        # 圆形障碍物：生成圆周上的点
        center_x, center_y = obs['x'], obs['y']
        radius = obs['radius']
        
        for j in range(points_per_obstacle):
            angle = j * 2 * np.pi / points_per_obstacle
            xobs_org[0, start_idx + j] = center_x + radius * np.cos(angle)
            yobs_org[0, start_idx + j] = center_y + radius * np.sin(angle)
            
    elif obs['type'] == 'box':
        # 矩形障碍物：生成矩形边界上的点
        center_x, center_y = obs['x'], obs['y']
        width, height = obs['width'], obs['height']
        
        # 4条边，每条边5个点
        points_per_side = points_per_obstacle // 4
        
        for j in range(points_per_side):  # 底边
            x = center_x - width/2 + j * width / (points_per_side - 1)
            y = center_y - height/2
            xobs_org[0, start_idx + j] = x
            yobs_org[0, start_idx + j] = y
            
        for j in range(points_per_side):  # 右边
            x = center_x + width/2
            y = center_y - height/2 + j * height / (points_per_side - 1)
            xobs_org[0, start_idx + points_per_side + j] = x
            yobs_org[0, start_idx + points_per_side + j] = y
            
        for j in range(points_per_side):  # 顶边
            x = center_x + width/2 - j * width / (points_per_side - 1)
            y = center_y + height/2
            xobs_org[0, start_idx + 2*points_per_side + j] = x
            yobs_org[0, start_idx + 2*points_per_side + j] = y
            
        for j in range(points_per_side):  # 左边
            x = center_x - width/2
            y = center_y + height/2 - j * height / (points_per_side - 1)
            xobs_org[0, start_idx + 3*points_per_side + j] = x
            yobs_org[0, start_idx + 3*points_per_side + j] = y

# 填充xyobs_org矩阵
xyobs_org[0, :] = xobs_org[0, :]
xyobs_org[1, :] = yobs_org[0, :]

xyobs_rot = xyobs_org.copy()

n_o = xyobs_org.shape[1]  # 障碍物总点数560

xobs = xyobs_rot[0, 0:n_o]#所有障碍物的x坐标
yobs = xyobs_rot[1, 0:n_o]#所有障碍物的y坐标

# 初始化机器人与障碍物距离矩阵
dobsmin_1 = np.zeros((1, len(i)))

dobsmin_2 = np.zeros((1, len(i)))

dobsmin_3 = np.zeros((1, len(i)))

dobsmin_4 = np.zeros((1, len(i)))

dobsmin_5 = np.zeros((1, len(i)))

ord_avoid = 0.35 #用于计算避障时的距离参数
ord_safe = 0.3 #判断是否为危险障碍物的距离阈值

dobs_1 = np.zeros((1, n_o+1)) # 机器人参考轨迹与障碍物距离

dobs_2 = np.zeros((1, n_o+1)) # 机器人参考轨迹与障碍物距离

dobs_3 = np.zeros((1, n_o+1)) # 机器人参考轨迹与障碍物距离

dobs_4 = np.zeros((1, n_o+1)) # 机器人参考轨迹与障碍物距离

dobs_5 = np.zeros((1, n_o+1)) # 机器人参考轨迹与障碍物距离

dij_avoid = 0.35 #用于计算机器人间避障时的距离参数

min_obs_num_1 = np.zeros((1,), dtype=int) #每个参考位置机器人最近的障碍物编号

min_obs_num_2 = np.zeros((1,), dtype=int) #每个参考位置机器人最近的障碍物编号

min_obs_num_3 = np.zeros((1,), dtype=int) #每个参考位置机器人最近的障碍物编号

min_obs_num_4 = np.zeros((1,), dtype=int) #每个参考位置机器人最近的障碍物编号

min_obs_num_5 = np.zeros((1,), dtype=int) #每个参考位置机器人最近的障碍物编号


pxy_avoid_1 = np.zeros((2, 1)) #避障参考轨迹轨迹偏移向量

pxy_avoid_2 = np.zeros((2, 1)) #避障参考轨迹轨迹偏移向量

pxy_avoid_3 = np.zeros((2, 1)) #避障参考轨迹轨迹偏移向量

pxy_avoid_4 = np.zeros((2, 1)) #避障参考轨迹轨迹偏移向量

pxy_avoid_5 = np.zeros((2, 1)) #避障参考轨迹轨迹偏移向量


d_R2R_1    = np.zeros((1, Rnum)) #机器人与所有机器人的距离矩阵

d_R2R_2    = np.zeros((1, Rnum)) #机器人与所有机器人的距离矩阵

d_R2R_3    = np.zeros((1, Rnum)) #机器人与所有机器人的距离矩阵

d_R2R_4    = np.zeros((1, Rnum)) #机器人与所有机器人的距离矩阵

d_R2R_5    = np.zeros((1, Rnum)) #机器人与所有机器人的距离矩阵


# 主控制循环
for k in range(len(i)):

    px1[:, k+1] = bb * 0.5 * np.cos(aa * t2 + (0 * 2 * np.pi / Rnum))
    py1[:, k+1] = bb * 0.5 * np.sin(aa * t2 + (0 * 2 * np.pi / Rnum)) 

    px2[:, k+1] = bb * 0.5 * np.cos(aa * t2 + (1 * 2 * np.pi / Rnum))
    py2[:, k+1] = bb * 0.5 * np.sin(aa * t2 + (1 * 2 * np.pi / Rnum)) 

    px3[:, k+1] = bb * 0.5 * np.cos(aa * t2 + (2 * 2 * np.pi / Rnum))
    py3[:, k+1] = bb * 0.5 * np.sin(aa * t2 + (2 * 2 * np.pi / Rnum)) 

    px4[:, k+1] = bb * 0.5 * np.cos(aa * t2 + (3 * 2 * np.pi / Rnum))
    py4[:, k+1] = bb * 0.5 * np.sin(aa * t2 + (3 * 2 * np.pi / Rnum)) 

    px5[:, k+1] = bb * 0.5 * np.cos(aa * t2 + (4 * 2 * np.pi / Rnum))
    py5[:, k+1] = bb * 0.5 * np.sin(aa * t2 + (4 * 2 * np.pi / Rnum)) 
    

    #机器人1避障
    dobsmin_1[0, k] = 10000
    min_obs_num_1 = 0
    
    for jj in range(n_o):
        dobs_1[0, jj] = np.sqrt((xobs[jj] - xr1[0, k])**2 + 
                                (yobs[jj] - yr1[0, k])**2)

        if dobs_1[0, jj] <= dobsmin_1[0, k]:
            min_obs_num_1 = jj
            dobsmin_1[0, k] = dobs_1[0, jj]
    # 找出最近的障碍物


    # 避障控制
    if dobsmin_1[0, k] <= ord_safe:
        jj_min = min_obs_num_1
        angle_o2r = np.arctan2(
            yobs[jj_min] - yr1[0, k],
            xobs[jj_min] - xr1[0, k]
        )
        force = (ord_avoid / dobs_1[0, jj_min]) * (ord_avoid - dobs_1[0, jj_min])
        pxy_avoid_1[:, 0] = force * np.array([np.cos(angle_o2r),
                                                    np.sin(angle_o2r)])
    else:
        pxy_avoid_1[:, 0] = 0

    # 🚀 定义当前机器人编号（这里是机器人1，索引为0）
    ii = 0  # 机器人1对应索引0
    
    for jj in range(Rnum):
        if jj != ii:
            # 🚀 Python语法改造：使用列表索引访问对应的xr和yr变量
            # xr[0]=xr1, xr[1]=xr2, xr[2]=xr3, xr[3]=xr4, xr[4]=xr5
            # yr[0]=yr1, yr[1]=yr2, yr[2]=yr3, yr[3]=yr4, yr[4]=yr5
            d_R2R_1[0, jj] = np.sqrt((xr[jj][0, k] - xr[ii][0, k])**2 + 
                            (yr[jj][0, k] - yr[ii][0, k])**2)

            if d_R2R_1[0, jj] <= 0.3:
                angle_r2i = np.arctan2(yr[jj][0, k] - yr[ii][0, k],
                                        xr[jj][0, k] - xr[ii][0, k])
                force_rr = (dij_avoid / d_R2R_1[0, jj]) * (dij_avoid - d_R2R_1[0, jj])
                pxy_avoid_1[:, 0] += force_rr * np.array([np.cos(angle_r2i),
                                                            np.sin(angle_r2i)])
    px1[:, k+1] -= pxy_avoid_1[0, 0]
    py1[:, k+1] -= pxy_avoid_1[1, 0]


    #机器人2避障
    dobsmin_2[0, k] = 10000
    min_obs_num_2 = 0

    for jj in range(n_o):
        dobs_2[0, jj] = np.sqrt((xobs[jj] - xr2[0, k])**2 + 
                                (yobs[jj] - yr2[0, k])**2)

        if dobs_2[0, jj] <= dobsmin_2[0, k]:
            min_obs_num_2 = jj
            dobsmin_2[0, k] = dobs_2[0, jj]

    # 避障控制
    if dobsmin_2[0, k] <= ord_safe:
        jj_min = min_obs_num_2
        angle_o2r = np.arctan2(
            yobs[jj_min] - yr2[0, k],
            xobs[jj_min] - xr2[0, k]
        )
        force = (ord_avoid / dobs_2[0, jj_min]) * (ord_avoid - dobs_2[0, jj_min])
        pxy_avoid_2[:, 0] = force * np.array([np.cos(angle_o2r),
                                                    np.sin(angle_o2r)])
    else:
        pxy_avoid_2[:, 0] = 0

    # 🚀 定义当前机器人编号（这里是机器人2，索引为1）
    ii = 1  # 机器人2对应索引1
    for jj in range(Rnum):
        if jj != ii:
            # 🚀 Python语法改造：使用列表索引访问对应的xr和yr变量
            # xr[0]=xr1, xr[1]=xr2, xr[2]=xr3, xr[3]=xr4, xr[4]=xr5
            # yr[0]=yr1, yr[1]=yr2, yr[2]=yr3, yr[3]=yr4, yr[4]=yr5
            d_R2R_2[0, jj] = np.sqrt((xr[jj][0, k] - xr[ii][0, k])**2 + 
                            (yr[jj][0, k] - yr[ii][0, k])**2)

            if d_R2R_2[0, jj] <= 0.3:
                angle_r2i = np.arctan2(yr[jj][0, k] - yr[ii][0, k],
                                        xr[jj][0, k] - xr[ii][0, k])
                force_rr = (dij_avoid / d_R2R_2[0, jj]) * (dij_avoid - d_R2R_2[0, jj])
                pxy_avoid_2[:, 0] += force_rr * np.array([np.cos(angle_r2i),
                                                            np.sin(angle_r2i)])
    px2[:, k+1] -= pxy_avoid_2[0, 0]
    py2[:, k+1] -= pxy_avoid_2[1, 0]

    
    #机器人3避障
    dobsmin_3[0, k] = 10000
    min_obs_num_3 = 0

    for jj in range(n_o):
        dobs_3[0, jj] = np.sqrt((xobs[jj] - xr3[0, k])**2 + 
                                (yobs[jj] - yr3[0, k])**2)

        if dobs_3[0, jj] <= dobsmin_3[0, k]:
            min_obs_num_3 = jj
            dobsmin_3[0, k] = dobs_3[0, jj]

    # 避障控制
    if dobsmin_3[0, k] <= ord_safe:
        jj_min = min_obs_num_3
        angle_o2r = np.arctan2(
            yobs[jj_min] - yr3[0, k],
            xobs[jj_min] - xr3[0, k]
        )
        force = (ord_avoid / dobs_3[0, jj_min]) * (ord_avoid - dobs_3[0, jj_min])
        pxy_avoid_3[:, 0] = force * np.array([np.cos(angle_o2r),
                                                    np.sin(angle_o2r)])
    else:
        pxy_avoid_3[:, 0] = 0

    # 🚀 定义当前机器人编号（这里是机器人3，索引为2）
    ii = 2  # 机器人3对应索引2
    for jj in range(Rnum):
        if jj != ii:
            # 🚀 Python语法改造：使用列表索引访问对应的xr和yr变量
            # xr[0]=xr1, xr[1]=xr2, xr[2]=xr3, xr[3]=xr4, xr[4]=xr5
            # yr[0]=yr1, yr[1]=yr2, yr[2]=yr3, yr[3]=yr4, yr[4]=yr5
            d_R2R_3[0, jj] = np.sqrt((xr[jj][0, k] - xr[ii][0, k])**2 + 
                            (yr[jj][0, k] - yr[ii][0, k])**2)

            if d_R2R_3[0, jj] <= 0.3:
                angle_r2i = np.arctan2(yr[jj][0, k] - yr[ii][0, k],
                                        xr[jj][0, k] - xr[ii][0, k])
                force_rr = (dij_avoid / d_R2R_3[0, jj]) * (dij_avoid - d_R2R_3[0, jj])
                pxy_avoid_3[:, 0] += force_rr * np.array([np.cos(angle_r2i),
                                                            np.sin(angle_r2i)])
    px3[:, k+1] -= pxy_avoid_3[0, 0]
    py3[:, k+1] -= pxy_avoid_3[1, 0]


    #机器人4避障
    dobsmin_4[0, k] = 10000
    min_obs_num_4 = 0

    for jj in range(n_o):
        dobs_4[0, jj] = np.sqrt((xobs[jj] - xr4[0, k])**2 + 
                                (yobs[jj] - yr4[0, k])**2)

        if dobs_4[0, jj] <= dobsmin_4[0, k]:
            min_obs_num_4 = jj
            dobsmin_4[0, k] = dobs_4[0, jj]

    # 避障控制
    if dobsmin_4[0, k] <= ord_safe:
        jj_min = min_obs_num_4
        angle_o2r = np.arctan2(
            yobs[jj_min] - yr4[0, k],
            xobs[jj_min] - xr4[0, k]
        )
        force = (ord_avoid / dobs_4[0, jj_min]) * (ord_avoid - dobs_4[0, jj_min])
        pxy_avoid_4[:, 0] = force * np.array([np.cos(angle_o2r),
                                                    np.sin(angle_o2r)])
    else:
        pxy_avoid_4[:, 0] = 0

    # 🚀 定义当前机器人编号（这里是机器人4，索引为3）
    ii = 3  # 机器人4对应索引3
    for jj in range(Rnum):
        if jj != ii:
            # 🚀 Python语法改造：使用列表索引访问对应的xr和yr变量
            # xr[0]=xr1, xr[1]=xr2, xr[2]=xr3, xr[3]=xr4, xr[4]=xr5
            # yr[0]=yr1, yr[1]=yr2, yr[2]=yr3, yr[3]=yr4, yr[4]=yr5
            d_R2R_4[0, jj] = np.sqrt((xr[jj][0, k] - xr[ii][0, k])**2 + 
                            (yr[jj][0, k] - yr[ii][0, k])**2)

            if d_R2R_4[0, jj] <= 0.3:
                angle_r2i = np.arctan2(yr[jj][0, k] - yr[ii][0, k],
                                        xr[jj][0, k] - xr[ii][0, k])
                force_rr = (dij_avoid / d_R2R_4[0, jj]) * (dij_avoid - d_R2R_4[0, jj])
                pxy_avoid_4[:, 0] += force_rr * np.array([np.cos(angle_r2i),
                                                            np.sin(angle_r2i)])
    px4[:, k+1] -= pxy_avoid_4[0, 0]
    py4[:, k+1] -= pxy_avoid_4[1, 0]


    #机器人5避障
    dobsmin_5[0, k] = 10000
    min_obs_num_5 = 0

    for jj in range(n_o):
        dobs_5[0, jj] = np.sqrt((xobs[jj] - xr5[0, k])**2 + 
                                (yobs[jj] - yr5[0, k])**2)

        if dobs_5[0, jj] <= dobsmin_5[0, k]:
            min_obs_num_5 = jj
            dobsmin_5[0, k] = dobs_5[0, jj]

    # 避障控制
    if dobsmin_5[0, k] <= ord_safe:
        jj_min = min_obs_num_5
        angle_o2r = np.arctan2(
            yobs[jj_min] - yr5[0, k],
            xobs[jj_min] - xr5[0, k]
        )
        force = (ord_avoid / dobs_5[0, jj_min]) * (ord_avoid - dobs_5[0, jj_min])
        pxy_avoid_5[:, 0] = force * np.array([np.cos(angle_o2r),
                                                np.sin(angle_o2r)])
    else:
        pxy_avoid_5[:, 0] = 0

    # 🚀 定义当前机器人编号（这里是机器人5，索引为4）
    ii = 4  # 机器人5对应索引4
    for jj in range(Rnum):
        if jj != ii:
            # 🚀 Python语法改造：使用列表索引访问对应的xr和yr变量
            # xr[0]=xr1, xr[1]=xr2, xr[2]=xr3, xr[3]=xr4, xr[4]=xr5
            # yr[0]=yr1, yr[1]=yr2, yr[2]=yr3, yr[3]=yr4, yr[4]=yr5
            d_R2R_5[0, jj] = np.sqrt((xr[jj][0, k] - xr[ii][0, k])**2 + 
                            (yr[jj][0, k] - yr[ii][0, k])**2)

            if d_R2R_5[0, jj] <= 0.3:
                angle_r2i = np.arctan2(yr[jj][0, k] - yr[ii][0, k],
                                        xr[jj][0, k] - xr[ii][0, k])
                force_rr = (dij_avoid / d_R2R_5[0, jj]) * (dij_avoid - d_R2R_5[0, jj])
                pxy_avoid_5[:, 0] += force_rr * np.array([np.cos(angle_r2i),
                                                            np.sin(angle_r2i)])
    px5[:, k+1] -= pxy_avoid_5[0, 0]
    py5[:, k+1] -= pxy_avoid_5[1, 0]


    if k==0:
        print(dobsmin_1[0, k])
        print(d_R2R_1[0, :])
        print(dobsmin_2[0, k])
        print(d_R2R_2[0, :])
        print(dobsmin_3[0, k])
        print(d_R2R_3[0, :])
        print(dobsmin_4[0, k])
        print(d_R2R_4[0, :])
        print(dobsmin_5[0, k])
        print(d_R2R_5[0, :])

    # 更新参考轨迹
    x0[0, k] = x0[0, 0] + 2.5 * np.sin(t2/15)
    y0[0, k] = y0[0, 0] + 2.5 * np.sin(t2/30)
    
    x0[0, k+1] = x0[0, 0] + 2.5 * np.sin((t2+t1)/15)
    y0[0, k+1] = y0[0, 0] + 2.5 * np.sin((t2+t1)/30)

    # 计算参考速度
    u0x[0, k+1] = (x0[0, k+1] - x0[0, k])/t1
    u0y[0, k+1] = (y0[0, k+1] - y0[0, k])/t1
    # print(x0[0, k+1], y0[0, k+1], u0x[0, k+1], u0y[0, k+1])           
    # 更新控制输入
    u0[:, k+1] = np.array([u0x[0, k+1], u0y[0, k+1]])
    theta0[0, k+1] = np.arctan2(u0y[0, k+1], u0x[0, k+1])
    
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
        
    # 更新机器人编队误差状态
    zx1[:, k] = np.array([x_hat1[0, k] - px1[0, k+1], y_hat1[0, k] - py1[0, k+1]])
    
    zx2[:, k] = np.array([x_hat2[0, k] - px2[0, k+1], y_hat2[0, k] - py2[0, k+1]])
    
    zx3[:, k] = np.array([x_hat3[0, k] - px3[0, k+1], y_hat3[0, k] - py3[0, k+1]])
    
    zx4[:, k] = np.array([x_hat4[0, k] - px4[0, k+1], y_hat4[0, k] - py4[0, k+1]])
    
    zx5[:, k] = np.array([x_hat5[0, k] - px5[0, k+1], y_hat5[0, k] - py5[0, k+1]])


    z0[:, k+1] = np.array([x0[0, k+1], y0[0, k+1]])

    # print(f"时间步={k+1}, 领导者位置=({x0[0, k+1]:.2f}, {y0[0, k+1]:.2f}), 速度=({u0x[0, k+1]:.2f}, {u0y[0, k+1]:.2f})")
          
    # 观测器状态存储列表，便于动态访问
    zxeo_all = [zxeo_1, zxeo_2, zxeo_3, zxeo_4, zxeo_5]
    dzxeo_all = [dzxeo_1, dzxeo_2, dzxeo_3, dzxeo_4, dzxeo_5]
    
    # 动态计算每个机器人的观测器状态更新
    for robot_id in range(Rnum):
        sum_dzxeo_j = np.zeros((2, 1))
        sum_consensus_error_zxeo = np.zeros((2, 1))
        
        # 根据邻接矩阵动态获取邻居
        for neighbor_id in range(Rnum):
            if A[robot_id, neighbor_id] != 0:  # 如果存在连接
                weight = A[robot_id, neighbor_id]
                sum_dzxeo_j += weight * dzxeo_all[neighbor_id][:, k].reshape(2, 1)
                sum_consensus_error_zxeo += weight * (zxeo_all[robot_id][:, k].reshape(2, 1) - zxeo_all[neighbor_id][:, k].reshape(2, 1))
                
                # # 🔍 打印前3个时间步的邻居观测器数据
                # if robot_id == 0:
                #     if k < 3:
                #         print(f"[时间步{k}] Robot {robot_id} 接收到邻居 {neighbor_id} 的观测器数据: "
                #             f"zxeo=[{zxeo_all[neighbor_id][0, k]:.10f}, {zxeo_all[neighbor_id][1, k]:.10f}], "
                #             f"dzxeo=[{dzxeo_all[neighbor_id][0, k]:.10f}, {dzxeo_all[neighbor_id][1, k]:.10f}]")
        
        # 计算SS项
        SS = sum_consensus_error_zxeo + B[robot_id, robot_id] * (zxeo_all[robot_id][:, k].reshape(2, 1) - z0[:, k+1].reshape(2, 1))
        
        # 观测器状态增量
        dzxeo_all[robot_id][:, k+1] = (
            (1.0 / (D[robot_id, robot_id] + B[robot_id, robot_id])) * (sum_dzxeo_j + B[robot_id, robot_id] * u0[:, k+1].reshape(2, 1))
            - ob_eta * (1.0 / (D[robot_id, robot_id] + B[robot_id, robot_id]))
            * np.sign(SS) * np.power(np.abs(SS), ob_alp)
        ).flatten()

        # 观测器状态
        zxeo_all[robot_id][:, k+1] = dzxeo_all[robot_id][:, k+1] * t1 + zxeo_all[robot_id][:, k]

        # if robot_id == 2:
        #     if k<3:
        #         print(f"[时间步{k}] Robot {robot_id} 计算结果: sum_dzxeo_j=[{sum_dzxeo_j[0,0]:.10f}, {sum_dzxeo_j[1,0]:.10f}], "
        #             f"SS=[{SS[0,0]:.10f}, {SS[1,0]:.10f}], "
        #             f"dzxeo=[{dzxeo_all[robot_id][0, k+1]:.10f}, {dzxeo_all[robot_id][1, k+1]:.10f}],"
        #             f"zxeo=[{zxeo_all[robot_id][0, k+1]:.10f}, {zxeo_all[robot_id][1, k+1]:.10f}]")
        
    # 计算误差和动态反馈项
    zx_all = [zx1, zx2, zx3, zx4, zx5]
    ex_all = [ex1, ex2, ex3, ex4, ex5]
    fx_all = [fx1, fx2, fx3, fx4, fx5]



    for robot_id in range(Rnum):
        ex_all[robot_id][:, k] = zx_all[robot_id][:, k] - zxeo_all[robot_id][:, k]
        fx_all[robot_id][:, k] = ex_all[robot_id][:, k] - t1 * dzxeo_all[robot_id][:, k+1]

    if k<3:
        print(f"[时间步{k}] Robot {0} zx=[{zx_all[0][0, k]:.10f}, {zx_all[0][1, k]:.10f}], "
                f"ex_all=[{ex_all[0][0, k]:.10f}, {ex_all[0][1, k]:.10f}], "
                f"fx_all=[{fx_all[0][0, k]:.10f}, {fx_all[0][1, k]:.10f}]")

    # # 计算动态系统状态
    # ex1[:, k] = Fx_1 @ zx1[:, k] - zx3[:, k]-z0[:, k+1]
    # fx1[:, k] = ex1[:, k] - t1*u0[:, k+1]

    # ex2[:, k] = Fx_2 @ zx2[:, k] - zx1[:, k] - zx3[:, k]
    # fx2[:, k] = ex2[:, k] 

    # ex3[:, k] = Fx_3 @ zx3[:, k] - zx4[:, k]
    # fx3[:, k] = ex3[:, k] 

    # ex4[:, k] = Fx_4 @ zx4[:, k] - zx1[:, k]
    # fx4[:, k] = ex4[:, k] 

    # ex5[:, k] = Fx_5 @ zx5[:, k] - zx2[:, k]
    # fx5[:, k] = ex5[:, k] 
    


   
    # print(ex1[:, 1], ex2[:, 1], ex3[:, 1], ex4[:, 1], ex5[:, 1])
    # print(fx1[:, 1], fx2[:, 1], fx3[:, 1], fx4[:, 1], fx5[:, 1])





    # 定义矩阵G、tildrg、tildrf和tildrI
    G_1 = np.vstack((np.hstack((gx_1, z_1)),
                np.hstack((gx_1, gx_1)),
                np.hstack((gx_1, gx_1))))
    
    G_2 = np.vstack((np.hstack((gx_2, z_2)),
                np.hstack((gx_2, gx_2)),
                np.hstack((gx_2, gx_2))))
    
    G_3 = np.vstack((np.hstack((gx_3, z_3)),
                np.hstack((gx_3, gx_3)),
                np.hstack((gx_3, gx_3))))
    # if k<3:
    #     print("G_1:", G_1)
    #     print("Q_1:", Q_1)

    G_4 = np.vstack((np.hstack((gx_4, z_4)),
                np.hstack((gx_4, gx_4)),
                np.hstack((gx_4, gx_4))))
    
    G_5 = np.vstack((np.hstack((gx_5, z_5)),
                np.hstack((gx_5, gx_5)),
                np.hstack((gx_5, gx_5))))

    tildrg_1 = np.vstack((gx_1 @ u1[:, k].reshape(-1, 1),
                        gx_1 @ u1[:, k].reshape(-1, 1),
                        gx_1 @ u1[:, k].reshape(-1, 1)))
    
    tildrg_2 = np.vstack((gx_2 @ u2[:, k].reshape(-1, 1),
                        gx_2 @ u2[:, k].reshape(-1, 1),
                        gx_2 @ u2[:, k].reshape(-1, 1)))

    tildrg_3 = np.vstack((gx_3 @ u3[:, k].reshape(-1, 1),
                        gx_3 @ u3[:, k].reshape(-1, 1),
                        gx_3 @ u3[:, k].reshape(-1, 1)))
    # if k<3:
    #     print("tildrg_1:", tildrg_1)

    tildrg_4 = np.vstack((gx_4 @ u4[:, k].reshape(-1, 1),
                        gx_4 @ u4[:, k].reshape(-1, 1),
                        gx_4 @ u4[:, k].reshape(-1, 1)))

    tildrg_5 = np.vstack((gx_5 @ u5[:, k].reshape(-1, 1),
                        gx_5 @ u5[:, k].reshape(-1, 1),
                        gx_5 @ u5[:, k].reshape(-1, 1)))
        

    tildrf_1 = np.vstack((fx1[:, k].reshape(-1, 1),
                        fx1[:, k].reshape(-1, 1),
                        fx1[:, k].reshape(-1, 1)))

    tildrf_2 = np.vstack((fx2[:, k].reshape(-1, 1),
                        fx2[:, k].reshape(-1, 1),
                        fx2[:, k].reshape(-1, 1)))

    tildrf_3 = np.vstack((fx3[:, k].reshape(-1, 1),
                        fx3[:, k].reshape(-1, 1),
                        fx3[:, k].reshape(-1, 1)))
    # if k<3:
    #     print("tildrf_1:", tildrf_1)

    tildrf_4 = np.vstack((fx4[:, k].reshape(-1, 1),
                        fx4[:, k].reshape(-1, 1),
                        fx4[:, k].reshape(-1, 1)))
    
    tildrf_5 = np.vstack((fx5[:, k].reshape(-1, 1),
                        fx5[:, k].reshape(-1, 1),
                        fx5[:, k].reshape(-1, 1)))    



    
    tildrI_1 = np.eye(Nu * m_gx_u) + np.vstack((np.zeros((2, Nu * m_gx_u)),
                                            np.hstack((np.eye(m_gx_u), np.zeros((m_gx_u, m_gx_u))))))
    
    tildrI_2 = np.eye(Nu * m_gx_u) + np.vstack((np.zeros((2, Nu * m_gx_u)),
                                            np.hstack((np.eye(m_gx_u), np.zeros((m_gx_u, m_gx_u))))))
    
    tildrI_3 = np.eye(Nu * m_gx_u) + np.vstack((np.zeros((2, Nu * m_gx_u)),
                                            np.hstack((np.eye(m_gx_u), np.zeros((m_gx_u, m_gx_u))))))
    
    tildrI_4 = np.eye(Nu * m_gx_u) + np.vstack((np.zeros((2, Nu * m_gx_u)),
                                            np.hstack((np.eye(m_gx_u), np.zeros((m_gx_u, m_gx_u))))))
    
    tildrI_5 = np.eye(Nu * m_gx_u) + np.vstack((np.zeros((2, Nu * m_gx_u)),
                                            np.hstack((np.eye(m_gx_u), np.zeros((m_gx_u, m_gx_u))))))
    # if k<3:
    #     print("tildrI_1:", tildrI_1)
    
    Irnn_1 = np.eye(Nu * n_gx_x, Nu * m_gx_u)

    Irnn_2 = np.eye(Nu * n_gx_x, Nu * m_gx_u)

    Irnn_3 = np.eye(Nu * n_gx_x, Nu * m_gx_u)

    # if k<3:
    #     print("Irnn_1:", Irnn_1)

    Irnn_4 = np.eye(Nu * n_gx_x, Nu * m_gx_u)

    Irnn_5 = np.eye(Nu * n_gx_x, Nu * m_gx_u)


    # 计算二次规划问题的矩阵W、C1和E
    W_1 = 2 * (G_1.T @ Q_1 @ G_1 + R_1)
    C1_1 = 2 * G_1.T @ Q_1 @ (tildrg_1 + tildrf_1)
    E_1 = np.vstack((-tildrI_1, tildrI_1, -G_1, G_1, Irnn_1))

    W_2 = 2 * (G_2.T @ Q_2 @ G_2 + R_2)
    C1_2 = 2 * G_2.T @ Q_2 @ (tildrg_2 + tildrf_2)
    E_2 = np.vstack((-tildrI_2, tildrI_2, -G_2, G_2, Irnn_2))

    W_3 = 2 * (G_3.T @ Q_3 @ G_3 + R_3)
    C1_3 = 2 * G_3.T @ Q_3 @ (tildrg_3 + tildrf_3)
    E_3 = np.vstack((-tildrI_3, tildrI_3, -G_3, G_3, Irnn_3))

    W_4 = 2 * (G_4.T @ Q_4 @ G_4 + R_4)
    C1_4 = 2 * G_4.T @ Q_4 @ (tildrg_4 + tildrf_4)
    E_4 = np.vstack((-tildrI_4, tildrI_4, -G_4, G_4, Irnn_4))

    W_5 = 2 * (G_5.T @ Q_5 @ G_5 + R_5)
    C1_5 = 2 * G_5.T @ Q_5 @ (tildrg_5 + tildrf_5)
    E_5 = np.vstack((-tildrI_5, tildrI_5, -G_5, G_5, Irnn_5))    
    
    # if t2==0:
    #     print("W_1=", W_1)
    #     print("W_2=", W_2)
    #     print("W_3=", W_3)
    #     print("W_4=", W_4)
    #     print("W_5=", W_5)
    # 定义约束向量b1
    b1_1 = np.vstack((-abarUmin11 + abaru1[:, k].reshape(-1, 1),
                    abarUmax11 - abaru1[:, k].reshape(-1, 1),
                    -abarxmin1 + tildrg_1 + tildrf_1,
                    abarxmax1 - tildrg_1 - tildrf_1,
                    -detabarUmin1,
                    detabarUmax1))
    
    b1_2 = np.vstack((-abarUmin12 + abaru2[:, k].reshape(-1, 1),
                    abarUmax12 - abaru2[:, k].reshape(-1, 1),
                    -abarxmin2 + tildrg_2 + tildrf_2,
                    abarxmax2 - tildrg_2 - tildrf_2,
                    -detabarUmin2,
                    detabarUmax2))
                    
    # if k<3:
        # print(f"[时间步{k}] 机器人0 abarUmin1:\n{abarUmin11.flatten()}")
        # print(f"[时间步{k}] 机器人0 abaru:\n{abaru1[:, k].flatten()}")
    
    b1_3 = np.vstack((-abarUmin13 + abaru3[:, k].reshape(-1, 1),
                    abarUmax13 - abaru3[:, k].reshape(-1, 1),
                    -abarxmin3 + tildrg_3 + tildrf_3,
                    abarxmax3 - tildrg_3 - tildrf_3,
                    -detabarUmin3,
                    detabarUmax3))
                  
    
    b1_4 = np.vstack((-abarUmin14 + abaru4[:, k].reshape(-1, 1),
                    abarUmax14 - abaru4[:, k].reshape(-1, 1),
                    -abarxmin4 + tildrg_4 + tildrf_4,
                    abarxmax4 - tildrg_4 - tildrf_4,
                    -detabarUmin4,
                    detabarUmax4))
    
    b1_5 = np.vstack((-abarUmin15 + abaru5[:, k].reshape(-1, 1),
                    abarUmax15 - abaru5[:, k].reshape(-1, 1),
                    -abarxmin5 + tildrg_5 + tildrf_5,
                    abarxmax5 - tildrg_5 - tildrf_5,
                    -detabarUmin5,
                    detabarUmax5))
    
    # 定义一些常量
    m_1 = b1_1.shape[0]
    myInf_1 = 1e10

    Pinfty_1 = myInf_1 * np.ones((m_1, 1))
    Minfty_1 = -Pinfty_1

    m_2 = b1_2.shape[0]
    myInf_2 = 1e10

    Pinfty_2 = myInf_2 * np.ones((m_2, 1))
    Minfty_2 = -Pinfty_2


    m_3 = b1_3.shape[0]
    myInf_3 = 1e10

    Pinfty_3 = myInf_3 * np.ones((m_3, 1))
    Minfty_3 = -Pinfty_3


    m_4 = b1_4.shape[0]
    myInf_4 = 1e10

    Pinfty_4 = myInf_4 * np.ones((m_4, 1))
    Minfty_4 = -Pinfty_4


    m_5 = b1_5.shape[0]
    myInf_5 = 1e10

    Pinfty_5 = myInf_5 * np.ones((m_5, 1))
    Minfty_5 = -Pinfty_5

    # if k<3:
    #     print(f"[时间步{k}] 机器人0 W矩阵W_1:\n{W_1.flatten()}")
    #     print(f"[时间步{k}] 机器人0 C1向量C1_1:\n{C1_1.flatten()}")
    #     print(f"[时间步{k}] 机器人0 E矩阵E_1:\n{E_1.flatten()}")
    #     print(f"[时间步{k}] 机器人0 约束向量b1_1:\n{b1_1.flatten()}")
    #     print(f"[时间步{k}] 机器人0 Pinfty向量Pinfty_1:\n{Pinfty_1.flatten()}")

        
     

    # 定义GPNN参数
    global M_1, p_1, yp_1, ym_1, ImH_1, IpHt_1, RIpHt_1
    p_1 = -E_1 @ np.linalg.inv(W_1) @ C1_1
    M_1 = -np.linalg.inv(W_1) @ C1_1
    yp_1 = np.vstack((b1_1, detabarUmax1))
    ym_1 = np.vstack((Minfty_1, detabarUmin1))
    ImH_1 = E_1 @ np.linalg.inv(W_1) @ E_1.T
    IpHt_1 = np.linalg.inv(W_1) @ E_1.T
    RIpHt_1 = (np.linalg.inv(IpHt_1 @ IpHt_1.T) @ IpHt_1).T

    global M_2, p_2, yp_2, ym_2, ImH_2, IpHt_2, RIpHt_2
    p_2 = -E_2 @ np.linalg.inv(W_2) @ C1_2
    M_2 = -np.linalg.inv(W_2) @ C1_2
    yp_2 = np.vstack((b1_2, detabarUmax2))
    ym_2 = np.vstack((Minfty_2, detabarUmin2))
    ImH_2 = E_2 @ np.linalg.inv(W_2) @ E_2.T
    IpHt_2 = np.linalg.inv(W_2) @ E_2.T
    RIpHt_2 = (np.linalg.inv(IpHt_2 @ IpHt_2.T) @ IpHt_2).T

    global M_3, p_3, yp_3, ym_3, ImH_3, IpHt_3, RIpHt_3
    p_3 = -E_3 @ np.linalg.inv(W_3) @ C1_3
    M_3 = -np.linalg.inv(W_3) @ C1_3
    yp_3 = np.vstack((b1_3, detabarUmax3))
    ym_3 = np.vstack((Minfty_3, detabarUmin3))
    ImH_3 = E_3 @ np.linalg.inv(W_3) @ E_3.T
    IpHt_3 = np.linalg.inv(W_3) @ E_3.T
    RIpHt_3 = (np.linalg.inv(IpHt_3 @ IpHt_3.T) @ IpHt_3).T

    global M_4, p_4, yp_4, ym_4, ImH_4, IpHt_4, RIpHt_4
    p_4 = -E_4 @ np.linalg.inv(W_4) @ C1_4
    M_4 = -np.linalg.inv(W_4) @ C1_4
    yp_4 = np.vstack((b1_4, detabarUmax4))
    ym_4 = np.vstack((Minfty_4, detabarUmin4))
    ImH_4 = E_4 @ np.linalg.inv(W_4) @ E_4.T
    IpHt_4 = np.linalg.inv(W_4) @ E_4.T
    RIpHt_4 = (np.linalg.inv(IpHt_4 @ IpHt_4.T) @ IpHt_4).T

    global M_5, p_5, yp_5, ym_5, ImH_5, IpHt_5, RIpHt_5
    p_5 = -E_5 @ np.linalg.inv(W_5) @ C1_5
    M_5 = -np.linalg.inv(W_5) @ C1_5
    yp_5 = np.vstack((b1_5, detabarUmax5))
    ym_5 = np.vstack((Minfty_5, detabarUmin5))
    ImH_5 = E_5 @ np.linalg.inv(W_5) @ E_5.T
    IpHt_5 = np.linalg.inv(W_5) @ E_5.T
    RIpHt_5 = (np.linalg.inv(IpHt_5 @ IpHt_5.T) @ IpHt_5).T


    # 初始化变量ycv
    ycv_1 = np.zeros((2*Nu, n+1, 1))
    for i in range(2*Nu):
        ycv_1[i, 0, 0] = y0x1[i, k]

    ycv_2 = np.zeros((2*Nu, n+1, 1))
    for i in range(2*Nu):
        ycv_2[i, 0, 0] = y0x2[i, k]

    ycv_3 = np.zeros((2*Nu, n+1, 1))
    for i in range(2*Nu):
        ycv_3[i, 0, 0] = y0x3[i, k]

    ycv_4 = np.zeros((2*Nu, n+1, 1))
    for i in range(2*Nu):
        ycv_4[i, 0, 0] = y0x4[i, k]

    ycv_5 = np.zeros((2*Nu, n+1, 1))
    for i in range(2*Nu):
        ycv_5[i, 0, 0] = y0x5[i, k]
        
    

        
    # 使用龙格库塔方法进行数值求解
    for ii in range(n):
        k11_1 = (-IpHt_1 @ (gfunction2_1(ImH_1 @ RIpHt_1 @ (ycv_1[:, ii] - M_1) + p_1 - RIpHt_1 @ (ycv_1[:, ii] - M_1)) - 
                    ImH_1 @ RIpHt_1 @ (ycv_1[:, ii] - M_1) - p_1))/gamma
        k21_1 = (-IpHt_1 @ (ImH_1 @ RIpHt_1 @ ((ycv_1[:, ii] + h*k11_1/2) - M_1) - 
                        gfunction2_1(ImH_1 @ RIpHt_1 @ ((ycv_1[:, ii] + h*k11_1/2) - M_1) - 
                                RIpHt_1 @ ((ycv_1[:, ii] + h*k11_1/2) - M_1) + p_1) + p_1))/gamma
        k31_1 = (-IpHt_1 @ (ImH_1 @ RIpHt_1 @ ((ycv_1[:, ii] + h*k21_1/2) - M_1) - 
                        gfunction2_1(ImH_1 @ RIpHt_1 @ ((ycv_1[:, ii] + h*k21_1/2) - M_1) - 
                                RIpHt_1 @ ((ycv_1[:, ii] + h*k21_1/2) - M_1) + p_1) + p_1))/gamma
        k41_1 = (-IpHt_1 @ (ImH_1 @ RIpHt_1 @ ((ycv_1[:, ii] + h*k31_1) - M_1) - 
                        gfunction2_1(ImH_1 @ RIpHt_1 @ ((ycv_1[:, ii] + h*k31_1) - M_1) - 
                                RIpHt_1 @ ((ycv_1[:, ii] + h*k31_1) - M_1) + p_1) + p_1))/gamma
        ycv_1[:, ii+1] = ycv_1[:, ii] + h*(k11_1 + 2*k21_1 + 2*k31_1 + k41_1)/6

    dot_y1_1 = ycv_1[:, n]
    y0x1[:, k+1] = dot_y1_1.ravel()
    a_1 = y0x1[:, k+1]

    detabarU1[:, k+1] = a_1[0:2*Nu]
    dd_1 = detabarU1[:, k+1]
    abaru1[:, k+1] = dd_1
    u1[:, k+1] = dd_1[0:2]

    for ii in range(n):
        k11_2 = (-IpHt_2 @ (gfunction2_2(ImH_2 @ RIpHt_2 @ (ycv_2[:, ii] - M_2) + p_2 - RIpHt_2 @ (ycv_2[:, ii] - M_2)) - 
                    ImH_2 @ RIpHt_2 @ (ycv_2[:, ii] - M_2) - p_2))/gamma
        k21_2 = (-IpHt_2 @ (ImH_2 @ RIpHt_2 @ ((ycv_2[:, ii] + h*k11_2/2) - M_2) - 
                        gfunction2_2(ImH_2 @ RIpHt_2 @ ((ycv_2[:, ii] + h*k11_2/2) - M_2) - 
                                RIpHt_2 @ ((ycv_2[:, ii] + h*k11_2/2) - M_2) + p_2) + p_2))/gamma
        k31_2 = (-IpHt_2 @ (ImH_2 @ RIpHt_2 @ ((ycv_2[:, ii] + h*k21_2/2) - M_2) - 
                        gfunction2_2(ImH_2 @ RIpHt_2 @ ((ycv_2[:, ii] + h*k21_2/2) - M_2) - 
                                RIpHt_2 @ ((ycv_2[:, ii] + h*k21_2/2) - M_2) + p_2) + p_2))/gamma
        k41_2 = (-IpHt_2 @ (ImH_2 @ RIpHt_2 @ ((ycv_2[:, ii] + h*k31_2) - M_2) - 
                        gfunction2_2(ImH_2 @ RIpHt_2 @ ((ycv_2[:, ii] + h*k31_2) - M_2) - 
                                RIpHt_2 @ ((ycv_2[:, ii] + h*k31_2) - M_2) + p_2) + p_2))/gamma
        ycv_2[:, ii+1] = ycv_2[:, ii] + h*(k11_2 + 2*k21_2 + 2*k31_2 + k41_2)/6

    dot_y1_2 = ycv_2[:, n]
    y0x2[:, k+1] = dot_y1_2.ravel()
    a_2 = y0x2[:, k+1]

    detabarU2[:, k+1] = a_2[0:2*Nu]
    dd_2 = detabarU2[:, k+1]
    abaru2[:, k+1] = dd_2
    u2[:, k+1] = dd_2[0:2]

    for ii in range(n):
        k11_3 = (-IpHt_3 @ (gfunction2_3(ImH_3 @ RIpHt_3 @ (ycv_3[:, ii] - M_3) + p_3 - RIpHt_3 @ (ycv_3[:, ii] - M_3)) - 
                    ImH_3 @ RIpHt_3 @ (ycv_3[:, ii] - M_3) - p_3))/gamma
        k21_3 = (-IpHt_3 @ (ImH_3 @ RIpHt_3 @ ((ycv_3[:, ii] + h*k11_3/2) - M_3) - 
                        gfunction2_3(ImH_3 @ RIpHt_3 @ ((ycv_3[:, ii] + h*k11_3/2) - M_3) - 
                                RIpHt_3 @ ((ycv_3[:, ii] + h*k11_3/2) - M_3) + p_3) + p_3))/gamma
        k31_3 = (-IpHt_3 @ (ImH_3 @ RIpHt_3 @ ((ycv_3[:, ii] + h*k21_3/2) - M_3) - 
                        gfunction2_3(ImH_3 @ RIpHt_3 @ ((ycv_3[:, ii] + h*k21_3/2) - M_3) - 
                                RIpHt_3 @ ((ycv_3[:, ii] + h*k21_3/2) - M_3) + p_3) + p_3))/gamma
        k41_3 = (-IpHt_3 @ (ImH_3 @ RIpHt_3 @ ((ycv_3[:, ii] + h*k31_3) - M_3) - 
                        gfunction2_3(ImH_3 @ RIpHt_3 @ ((ycv_3[:, ii] + h*k31_3) - M_3) - 
                                RIpHt_3 @ ((ycv_3[:, ii] + h*k31_3) - M_3) + p_3) + p_3))/gamma
        ycv_3[:, ii+1] = ycv_3[:, ii] + h*(k11_3 + 2*k21_3 + 2*k31_3 + k41_3)/6

    dot_y1_3 = ycv_3[:, n]
    y0x3[:, k+1] = dot_y1_3.ravel()
    a_3 = y0x3[:, k+1]

    detabarU3[:, k+1] = a_3[0:2*Nu]
    dd_3 = detabarU3[:, k+1]
    abaru3[:, k+1] = dd_3
    u3[:, k+1] = dd_3[0:2]

    for ii in range(n):
        k11_4 = (-IpHt_4 @ (gfunction2_4(ImH_4 @ RIpHt_4 @ (ycv_4[:, ii] - M_4) + p_4 - RIpHt_4 @ (ycv_4[:, ii] - M_4)) - 
                    ImH_4 @ RIpHt_4 @ (ycv_4[:, ii] - M_4) - p_4))/gamma
        k21_4 = (-IpHt_4 @ (ImH_4 @ RIpHt_4 @ ((ycv_4[:, ii] + h*k11_4/2) - M_4) - 
                        gfunction2_4(ImH_4 @ RIpHt_4 @ ((ycv_4[:, ii] + h*k11_4/2) - M_4) - 
                                RIpHt_4 @ ((ycv_4[:, ii] + h*k11_4/2) - M_4) + p_4) + p_4))/gamma
        k31_4 = (-IpHt_4 @ (ImH_4 @ RIpHt_4 @ ((ycv_4[:, ii] + h*k21_4/2) - M_4) - 
                        gfunction2_4(ImH_4 @ RIpHt_4 @ ((ycv_4[:, ii] + h*k21_4/2) - M_4) - 
                                RIpHt_4 @ ((ycv_4[:, ii] + h*k21_4/2) - M_4) + p_4) + p_4))/gamma
        k41_4 = (-IpHt_4 @ (ImH_4 @ RIpHt_4 @ ((ycv_4[:, ii] + h*k31_4) - M_4) - 
                        gfunction2_4(ImH_4 @ RIpHt_4 @ ((ycv_4[:, ii] + h*k31_4) - M_4) - 
                                RIpHt_4 @ ((ycv_4[:, ii] + h*k31_4) - M_4) + p_4) + p_4))/gamma
        ycv_4[:, ii+1] = ycv_4[:, ii] + h*(k11_4 + 2*k21_4 + 2*k31_4 + k41_4)/6

    dot_y1_4 = ycv_4[:, n]
    y0x4[:, k+1] = dot_y1_4.ravel()
    a_4 = y0x4[:, k+1]

    detabarU4[:, k+1] = a_4[0:2*Nu]
    dd_4 = detabarU4[:, k+1]
    abaru4[:, k+1] = dd_4
    u4[:, k+1] = dd_4[0:2]

    for ii in range(n):
        k11_5 = (-IpHt_5 @ (gfunction2_5(ImH_5 @ RIpHt_5 @ (ycv_5[:, ii] - M_5) + p_5 - RIpHt_5 @ (ycv_5[:, ii] - M_5)) - 
                    ImH_5 @ RIpHt_5 @ (ycv_5[:, ii] - M_5) - p_5))/gamma
        k21_5 = (-IpHt_5 @ (ImH_5 @ RIpHt_5 @ ((ycv_5[:, ii] + h*k11_5/2) - M_5) - 
                        gfunction2_5(ImH_5 @ RIpHt_5 @ ((ycv_5[:, ii] + h*k11_5/2) - M_5) - 
                                RIpHt_5 @ ((ycv_5[:, ii] + h*k11_5/2) - M_5) + p_5) + p_5))/gamma
        k31_5 = (-IpHt_5 @ (ImH_5 @ RIpHt_5 @ ((ycv_5[:, ii] + h*k21_5/2) - M_5) - 
                        gfunction2_5(ImH_5 @ RIpHt_5 @ ((ycv_5[:, ii] + h*k21_5/2) - M_5) - 
                                RIpHt_5 @ ((ycv_5[:, ii] + h*k21_5/2) - M_5) + p_5) + p_5))/gamma
        k41_5 = (-IpHt_5 @ (ImH_5 @ RIpHt_5 @ ((ycv_5[:, ii] + h*k31_5) - M_5) - 
                        gfunction2_5(ImH_5 @ RIpHt_5 @ ((ycv_5[:, ii] + h*k31_5) - M_5) - 
                                RIpHt_5 @ ((ycv_5[:, ii] + h*k31_5) - M_5) + p_5) + p_5))/gamma
        ycv_5[:, ii+1] = ycv_5[:, ii] + h*(k11_5 + 2*k21_5 + 2*k31_5 + k41_5)/6

    dot_y1_5 = ycv_5[:, n]
    y0x5[:, k+1] = dot_y1_5.ravel()
    a_5 = y0x5[:, k+1]

    detabarU5[:, k+1] = a_5[0:2*Nu]
    dd_5 = detabarU5[:, k+1]
    abaru5[:, k+1] = dd_5
    u5[:, k+1] = dd_5[0:2]
    # if k < 3 :
    #     print("detabarU1:",detabarU1[:, k+1])
    #     print("abaru1:",abaru1[:, k+1])
    #     print("轨迹规划输入", u1[:, k+1], u2[:, k+1], u3[:, k+1], u4[:, k+1], u5[:, k+1])


    gxxz_1 = np.zeros((3, 2))
    gxxz_2 = np.zeros((3, 2))
    gxxz_3 = np.zeros((3, 2))
    gxxz_4 = np.zeros((3, 2))
    gxxz_5 = np.zeros((3, 2))

    # 控制输入限制和轨迹更新
    
    # 限制x方向输入
    if u1[0, k+1] >= 0.22:
        u1[0, k+1] = 0.22
    elif u1[0, k+1] < -0.22:
        u1[0, k+1] = -0.22
    
    # 限制y方向输入
    if u1[1, k+1] >= 0.22:
        u1[1, k+1] = 0.22
    elif u1[1, k+1] < -0.22:
        u1[1, k+1] = -0.22

    # 提取控制输入
    ux1[0, k+1] = u1[0, k+1]
    uy1[0, k+1] = u1[1, k+1]


    # 计算期望航向角
    thetar1[0, k+1] = np.arctan2(uy1[0, k+1], ux1[0, k+1])
    
    # 航向角跨象限处理
    thetar_sub = 0
    flagplne = 0
    if thetar1[0, k] >= np.pi/2 and thetar1[0, k] <= np.pi and \
    thetar1[0, k+1] <= -np.pi/2 and thetar1[0, k+1] >= -np.pi:
        flagplne = -1
    elif thetar1[0, k] <= -np.pi/2 and thetar1[0, k] >= -np.pi and \
        thetar1[0, k+1] >= np.pi/2 and thetar1[0, k+1] <= np.pi:
        flagplne = 1
        
    thetar1_sub = thetar1[0, k] + 2 * np.pi * flagplne
    wr1[0, k+1] = (thetar1[0, k+1] - thetar1_sub) / t1
    vr1[0, k+1] = np.sqrt(ux1[0, k+1]**2 + uy1[0, k+1]**2)


# 限制x方向输入
    if u2[0, k+1] >= 0.22:
        u2[0, k+1] = 0.22
    elif u2[0, k+1] < -0.22:
        u2[0, k+1] = -0.22

    # 限制y方向输入
    if u2[1, k+1] >= 0.22:
        u2[1, k+1] = 0.22
    elif u2[1, k+1] < -0.22:
        u2[1, k+1] = -0.22
        
    # 提取控制输入
    ux2[0, k+1] = u2[0, k+1]
    uy2[0, k+1] = u2[1, k+1]
    
    # 计算期望航向角
    thetar2[0, k+1] = np.arctan2(uy2[0, k+1], ux2[0, k+1])
    
    # 航向角跨象限处理
    thetar_sub = 0
    flagplne = 0
    if thetar2[0, k] >= np.pi/2 and thetar2[0, k] <= np.pi and \
    thetar2[0, k+1] <= -np.pi/2 and thetar2[0, k+1] >= -np.pi:
        flagplne = -1
    elif thetar2[0, k] <= -np.pi/2 and thetar2[0, k] >= -np.pi and \
        thetar2[0, k+1] >= np.pi/2 and thetar2[0, k+1] <= np.pi:
        flagplne = 1
        
    thetar2_sub = thetar2[0, k] + 2 * np.pi * flagplne
    wr2[0, k+1] = (thetar2[0, k+1] - thetar2_sub) / t1
    vr2[0, k+1] = np.sqrt(ux2[0, k+1]**2 + uy2[0, k+1]**2)


# 限制x方向输入
    if u3[0, k+1] >= 0.22:
        u3[0, k+1] = 0.22
    elif u3[0, k+1] < -0.22:
        u3[0, k+1] = -0.22
    
    # 限制y方向输入
    if u3[1, k+1] >= 0.22:
        u3[1, k+1] = 0.22
    elif u3[1, k+1] < -0.22:
        u3[1, k+1] = -0.22
        
    # 提取控制输入
    ux3[0, k+1] = u3[0, k+1]
    uy3[0, k+1] = u3[1, k+1]
    
    # 计算期望航向角
    thetar3[0, k+1] = np.arctan2(uy3[0, k+1], ux3[0, k+1])
    
    # 航向角跨象限处理
    thetar_sub = 0
    flagplne = 0
    if thetar3[0, k] >= np.pi/2 and thetar3[0, k] <= np.pi and \
    thetar3[0, k+1] <= -np.pi/2 and thetar3[0, k+1] >= -np.pi:
        flagplne = -1
    elif thetar3[0, k] <= -np.pi/2 and thetar3[0, k] >= -np.pi and \
        thetar3[0, k+1] >= np.pi/2 and thetar3[0, k+1] <= np.pi:
        flagplne = 1
        
    thetar3_sub = thetar3[0, k] + 2 * np.pi * flagplne
    wr3[0, k+1] = (thetar3[0, k+1] - thetar3_sub) / t1
    vr3[0, k+1] = np.sqrt(ux3[0, k+1]**2 + uy3[0, k+1]**2)


# 限制x方向输入
    if u4[0, k+1] >= 0.22:
        u4[0, k+1] = 0.22
    elif u4[0, k+1] < -0.22:
        u4[0, k+1] = -0.22
    
    # 限制y方向输入
    if u4[1, k+1] >= 0.22:
        u4[1, k+1] = 0.22
    elif u4[1, k+1] < -0.22:
        u4[1, k+1] = -0.22
        
    # 提取控制输入
    ux4[0, k+1] = u4[0, k+1]
    uy4[0, k+1] = u4[1, k+1]
    
    # 计算期望航向角
    thetar4[0, k+1] = np.arctan2(uy4[0, k+1], ux4[0, k+1])
    
    # 航向角跨象限处理
    thetar_sub = 0
    flagplne = 0
    if thetar4[0, k] >= np.pi/2 and thetar4[0, k] <= np.pi and \
    thetar4[0, k+1] <= -np.pi/2 and thetar4[0, k+1] >= -np.pi:
        flagplne = -1
    elif thetar4[0, k] <= -np.pi/2 and thetar4[0, k] >= -np.pi and \
        thetar4[0, k+1] >= np.pi/2 and thetar4[0, k+1] <= np.pi:
        flagplne = 1
        
    thetar4_sub = thetar4[0, k] + 2 * np.pi * flagplne
    wr4[0, k+1] = (thetar4[0, k+1] - thetar4_sub) / t1
    vr4[0, k+1] = np.sqrt(ux4[0, k+1]**2 + uy4[0, k+1]**2)


# 限制x方向输入
    if u5[0, k+1] >= 0.22:
        u5[0, k+1] = 0.22
    elif u5[0, k+1] < -0.22:
        u5[0, k+1] = -0.22
    
    # 限制y方向输入
    if u5[1, k+1] >= 0.22:
        u5[1, k+1] = 0.22
    elif u5[1, k+1] < -0.22:
        u5[1, k+1] = -0.22
        
    # 提取控制输入
    ux5[0, k+1] = u5[0, k+1]
    uy5[0, k+1] = u5[1, k+1]
    
    # 计算期望航向角
    thetar5[0, k+1] = np.arctan2(uy5[0, k+1], ux5[0, k+1])
    
    # 航向角跨象限处理
    thetar_sub = 0
    flagplne = 0
    if thetar5[0, k] >= np.pi/2 and thetar5[0, k] <= np.pi and \
    thetar5[0, k+1] <= -np.pi/2 and thetar5[0, k+1] >= -np.pi:
        flagplne = -1
    elif thetar5[0, k] <= -np.pi/2 and thetar5[0, k] >= -np.pi and \
        thetar5[0, k+1] >= np.pi/2 and thetar5[0, k+1] <= np.pi:
        flagplne = 1
        
    thetar5_sub = thetar5[0, k] + 2 * np.pi * flagplne
    wr5[0, k+1] = (thetar5[0, k+1] - thetar5_sub) / t1
    vr5[0, k+1] = np.sqrt(ux5[0, k+1]**2 + uy5[0, k+1]**2)
    
    # 更新参考轨迹位置

    x_hat1[:, k+1] = x_hat1[:, k] + ux1[:, k+1] * t1
    y_hat1[:, k+1] = y_hat1[:, k] + uy1[:, k+1] * t1
    xr1[:, k+1] = x_hat1[:, k+1]
    yr1[:, k+1] = y_hat1[:, k+1]

    x_hat2[:, k+1] = x_hat2[:, k] + ux2[:, k+1] * t1
    y_hat2[:, k+1] = y_hat2[:, k] + uy2[:, k+1] * t1
    xr2[:, k+1] = x_hat2[:, k+1]
    yr2[:, k+1] = y_hat2[:, k+1]

    x_hat3[:, k+1] = x_hat3[:, k] + ux3[:, k+1] * t1
    y_hat3[:, k+1] = y_hat3[:, k] + uy3[:, k+1] * t1
    xr3[:, k+1] = x_hat3[:, k+1]
    yr3[:, k+1] = y_hat3[:, k+1]

    x_hat4[:, k+1] = x_hat4[:, k] + ux4[:, k+1] * t1
    y_hat4[:, k+1] = y_hat4[:, k] + uy4[:, k+1] * t1
    xr4[:, k+1] = x_hat4[:, k+1]
    yr4[:, k+1] = y_hat4[:, k+1]

    x_hat5[:, k+1] = x_hat5[:, k] + ux5[:, k+1] * t1
    y_hat5[:, k+1] = y_hat5[:, k] + uy5[:, k+1] * t1
    xr5[:, k+1] = x_hat5[:, k+1]
    yr5[:, k+1] = y_hat5[:, k+1]


    # 计算跟踪误差
    
    xe1[0, k] = np.cos(thetac1[0, k]) * (xr1[0, k+1] - xc1[0, k]) + \
            np.sin(thetac1[0, k]) * (yr1[0, k+1] - yc1[0, k])
    ye1[0, k] = np.cos(thetac1[0, k]) * (yr1[0, k+1] - yc1[0, k]) - \
            np.sin(thetac1[0, k]) * (xr1[0, k+1] - xc1[0, k])
    
    # 航向角误差处理
    thetar_subc = 0
    flagplnec = 0
    if thetac1[0, k] >= np.pi/2 and thetac1[0, k] <= np.pi and \
    thetar1[0, k+1] <= -np.pi/2 and thetar1[0, k+1] >= -np.pi:
        flagplnec = -1
    elif thetac1[0, k] <= -np.pi/2 and thetac1[0, k] >= -np.pi and \
        thetar1[0, k+1] >= np.pi/2 and thetar1[0, k+1] <= np.pi:
        flagplnec = 1
    
    thetar_subc = thetac1[0, k] + 2 * np.pi * flagplnec
    thetae1[0, k] = thetar1[0, k+1] - thetar_subc
    
    # 计算中间变量
    k0_1 = 2 * np.sign(vr1[0, k+1])
    L1_1 = np.sqrt(1 + xe1[0, k]**2 + ye1[0, k]**2)
    thetae_hat1[0, k] = thetae1[0, k] + np.arctan2(k0_1 * ye1[0, k], L1_1.item())
    L2_1 = np.sqrt(1 + xe1[0, k]**2 + (1 + k0_1**2) * ye1[0, k]**2)
    L3_1 = np.sqrt(1 + thetae_hat1[0, k]**2)
    
    # 计算非线性项
    if thetae_hat1[0, k] == 0:
        alp = np.cos(thetae1[0, k])
    else:
        alp = (1/thetae_hat1[0, k]) * (np.sin(thetae1[0, k]) + 
            np.sin(np.arctan2(k0_1 * ye1[0, k], L1_1)))
    
    M0_1 = (k0_1 * vr1[0, k+1] * np.sin(thetae1[0, k]) * (1 + xe1[0, k]**2) - 
            k0_1 * xe1[0, k] * ye1[0, k] * vr1[0, k+1] * np.cos(thetae1[0, k])) / \
            (L1_1 * (L2_1**2))
                    
    # 构建预测模型矩阵
    fxz_1[:, k] = np.array([
        xe1[0, k],
        ye1[0, k],
        thetae_hat1[0, k]
    ]) + t1 * np.array([
        vr1[0, k+1] * np.cos(thetae1[0, k]),
        vr1[0, k+1] * np.sin(thetae1[0, k]),
        wr1[0, k+1] + M0_1.item()
    ])
    
    # 输入矩阵
    gxxz_1 = t1 * np.array([
                [-1, ye1[0, k]],
                [0, -xe1[0, k]],
                [(k0_1 * xe1[0, k] * ye1[0, k])/(L1_1 * L2_1**2).item(), -(1 + (k0_1 * L1_1 * xe1[0, k])/(L2_1**2)).item()]           
                                                                                                                ])


    xe2[0, k] = np.cos(thetac2[0, k]) * (xr2[0, k+1] - xc2[0, k]) + \
            np.sin(thetac2[0, k]) * (yr2[0, k+1] - yc2[0, k])
    ye2[0, k] = np.cos(thetac2[0, k]) * (yr2[0, k+1] - yc2[0, k]) - \
            np.sin(thetac2[0, k]) * (xr2[0, k+1] - xc2[0, k])
    
    # 航向角误差处理
    thetar_subc = 0
    flagplnec = 0
    if thetac2[0, k] >= np.pi/2 and thetac2[0, k] <= np.pi and \
    thetar2[0, k+1] <= -np.pi/2 and thetar2[0, k+1] >= -np.pi:
        flagplnec = -1
    elif thetac2[0, k] <= -np.pi/2 and thetac2[0, k] >= -np.pi and \
        thetar2[0, k+1] >= np.pi/2 and thetar2[0, k+1] <= np.pi:
        flagplnec = 1
    
    thetar_subc = thetac2[0, k] + 2 * np.pi * flagplnec
    thetae2[0, k] = thetar2[0, k+1] - (thetac2[0, k] + flagplnec * 2 * np.pi)
    
    # 计算中间变量
    k0_2 = 2 * np.sign(vr2[0, k+1])
    L1_2 = np.sqrt(1 + xe2[0, k]**2 + ye2[0, k]**2)
    thetae_hat2[0, k] = thetae2[0, k] + np.arctan2(k0_2 * ye2[0, k], L1_2.item())
    L2_2 = np.sqrt(1 + xe2[0, k]**2 + (1 + k0_2**2) * ye2[0, k]**2)
    L3_2 = np.sqrt(1 + thetae_hat2[0, k]**2)
    
    # 计算非线性项
    if thetae_hat2[0, k] == 0:
        alp = np.cos(thetae2[0, k])
    else:
        alp = (1/thetae_hat2[0, k]) * (np.sin(thetae2[0, k]) + 
            np.sin(np.arctan2(k0_2 * ye2[0, k], L1_2)))
    
    M0_2 = (k0_2 * vr2[0, k+1] * np.sin(thetae2[0, k]) * (1 + xe2[0, k]**2) - 
            k0_2 * xe2[0, k] * ye2[0, k] * vr2[0, k+1] * np.cos(thetae2[0, k])) / \
            (L1_2 * (L2_2**2))
                    
    # 构建预测模型矩阵
    fxz_2[:, k] = np.array([
        xe2[0, k],
        ye2[0, k],
        thetae_hat2[0, k]
    ]) + t1 * np.array([
        vr2[0, k+1] * np.cos(thetae2[0, k]),
        vr2[0, k+1] * np.sin(thetae2[0, k]),
        wr2[0, k+1] + M0_2.item()
    ])
    
    # 输入矩阵
    gxxz_2 = t1 * np.array([
                [-1, ye2[0, k]],
                [0, -xe2[0, k]],
                [(k0_2 * xe2[0, k] * ye2[0, k])/(L1_2 * L2_2**2).item(), -(1 + (k0_2 * L1_2 * xe2[0, k])/(L2_2**2)).item()]           
                                                                                                                ])


    xe3[0, k] = np.cos(thetac3[0, k]) * (xr3[0, k+1] - xc3[0, k]) + \
            np.sin(thetac3[0, k]) * (yr3[0, k+1] - yc3[0, k])
    ye3[0, k] = np.cos(thetac3[0, k]) * (yr3[0, k+1] - yc3[0, k]) - \
            np.sin(thetac3[0, k]) * (xr3[0, k+1] - xc3[0, k])
    
    # 航向角误差处理
    thetar_subc = 0
    flagplnec = 0
    if thetac3[0, k] >= np.pi/2 and thetac3[0, k] <= np.pi and \
    thetar3[0, k+1] <= -np.pi/2 and thetar3[0, k+1] >= -np.pi:
        flagplnec = -1
    elif thetac3[0, k] <= -np.pi/2 and thetac3[0, k] >= -np.pi and \
        thetar3[0, k+1] >= np.pi/2 and thetar3[0, k+1] <= np.pi:
        flagplnec = 1
    
    thetar_subc = thetac3[0, k] + 2 * np.pi * flagplnec
    thetae3[0, k] = thetar3[0, k+1] - (thetac3[0, k] + flagplnec * 2 * np.pi)
    
    # 计算中间变量
    k0_3 = 2 * np.sign(vr3[0, k+1])
    L1_3 = np.sqrt(1 + xe3[0, k]**2 + ye3[0, k]**2)
    thetae_hat3[0, k] = thetae3[0, k] + np.arctan2(k0_3 * ye3[0, k], L1_3.item())
    L2_3 = np.sqrt(1 + xe3[0, k]**2 + (1 + k0_3**2) * ye3[0, k]**2)
    L3_3 = np.sqrt(1 + thetae_hat3[0, k]**2)
    
    # 计算非线性项
    if thetae_hat3[0, k] == 0:
        alp = np.cos(thetae3[0, k])
    else:
        alp = (1/thetae_hat3[0, k]) * (np.sin(thetae3[0, k]) + 
            np.sin(np.arctan2(k0_3 * ye3[0, k], L1_3)))
    
    M0_3 = (k0_3 * vr3[0, k+1] * np.sin(thetae3[0, k]) * (1 + xe3[0, k]**2) - 
            k0_3 * xe3[0, k] * ye3[0, k] * vr3[0, k+1] * np.cos(thetae3[0, k])) / \
            (L1_3 * (L2_3**2))
                    
    # 构建预测模型矩阵
    fxz_3[:, k] = np.array([
        xe3[0, k],
        ye3[0, k],
        thetae_hat3[0, k]
    ]) + t1 * np.array([
        vr3[0, k+1] * np.cos(thetae3[0, k]),
        vr3[0, k+1] * np.sin(thetae3[0, k]),
        wr3[0, k+1] + M0_3.item()
    ])
    
    # 输入矩阵
    gxxz_3 = t1 * np.array([
                [-1, ye3[0, k]],
                [0, -xe3[0, k]],
                [(k0_3 * xe3[0, k] * ye3[0, k])/(L1_3 * L2_3**2).item(), -(1 + (k0_3 * L1_3 * xe3[0, k])/(L2_3**2)).item()]           
            
                                                                                                                ])

    xe4[0, k] = np.cos(thetac4[0, k]) * (xr4[0, k+1] - xc4[0, k]) + \
            np.sin(thetac4[0, k]) * (yr4[0, k+1] - yc4[0, k])
    ye4[0, k] = np.cos(thetac4[0, k]) * (yr4[0, k+1] - yc4[0, k]) - \
            np.sin(thetac4[0, k]) * (xr4[0, k+1] - xc4[0, k])
    
    # 航向角误差处理
    thetar_subc = 0
    flagplnec = 0
    if thetac4[0, k] >= np.pi/2 and thetac4[0, k] <= np.pi and \
    thetar4[0, k+1] <= -np.pi/2 and thetar4[0, k+1] >= -np.pi:
        flagplnec = -1
    elif thetac4[0, k] <= -np.pi/2 and thetac4[0, k] >= -np.pi and \
        thetar4[0, k+1] >= np.pi/2 and thetar4[0, k+1] <= np.pi:
        flagplnec = 1

    thetar_subc = thetac4[0, k] + 2 * np.pi * flagplnec
    thetae4[0, k] = thetar4[0, k+1] - (thetac4[0, k] + flagplnec * 2 * np.pi)
    
    # 计算中间变量
    k0_4 = 2 * np.sign(vr4[0, k+1])
    L1_4 = np.sqrt(1 + xe4[0, k]**2 + ye4[0, k]**2)
    thetae_hat4[0, k] = thetae4[0, k] + np.arctan2(k0_4 * ye4[0, k], L1_4.item())
    L2_4 = np.sqrt(1 + xe4[0, k]**2 + (1 + k0_4**2) * ye4[0, k]**2)
    L3_4 = np.sqrt(1 + thetae_hat4[0, k]**2)
    
    # 计算非线性项
    if thetae_hat4[0, k] == 0:
        alp = np.cos(thetae4[0, k])
    else:
        alp = (1/thetae_hat4[0, k]) * (np.sin(thetae4[0, k]) + 
            np.sin(np.arctan2(k0_4 * ye4[0, k], L1_4)))
    
    M0_4 = (k0_4 * vr4[0, k+1] * np.sin(thetae4[0, k]) * (1 + xe4[0, k]**2) - 
            k0_4 * xe4[0, k] * ye4[0, k] * vr4[0, k+1] * np.cos(thetae4[0, k])) / \
            (L1_4 * (L2_4**2))
                    
    # 构建预测模型矩阵
    fxz_4[:, k] = np.array([
        xe4[0, k],
        ye4[0, k],
        thetae_hat4[0, k]
    ]) + t1 * np.array([
        vr4[0, k+1] * np.cos(thetae4[0, k]),
        vr4[0, k+1] * np.sin(thetae4[0, k]),
        wr4[0, k+1] + M0_4.item()
    ])
    
    # 输入矩阵
    gxxz_4 = t1 * np.array([
                [-1, ye4[0, k]],
                [0, -xe4[0, k]],
                [(k0_4 * xe4[0, k] * ye4[0, k])/(L1_4 * L2_4**2).item(), -(1 + (k0_4 * L1_4 * xe4[0, k])/(L2_4**2)).item()]           
                                                                                                                ])


    xe5[0, k] = np.cos(thetac5[0, k]) * (xr5[0, k+1] - xc5[0, k]) + \
            np.sin(thetac5[0, k]) * (yr5[0, k+1] - yc5[0, k])
    ye5[0, k] = np.cos(thetac5[0, k]) * (yr5[0, k+1] - yc5[0, k]) - \
            np.sin(thetac5[0, k]) * (xr5[0, k+1] - xc5[0, k])
    
    # 航向角误差处理
    thetar_subc = 0
    flagplnec = 0
    if thetac5[0, k] >= np.pi/2 and thetac5[0, k] <= np.pi and \
    thetar5[0, k+1] <= -np.pi/2 and thetar5[0, k+1] >= -np.pi:
        flagplnec = -1
    elif thetac5[0, k] <= -np.pi/2 and thetac5[0, k] >= -np.pi and \
        thetar5[0, k+1] >= np.pi/2 and thetar5[0, k+1] <= np.pi:
        flagplnec = 1
    
    thetar_subc = thetac5[0, k] + 2 * np.pi * flagplnec
    thetae5[0, k] = thetar5[0, k+1] - (thetac5[0, k] + flagplnec * 2 * np.pi)
    
    # 计算中间变量
    k0_5 = 2 * np.sign(vr5[0, k+1])
    L1_5 = np.sqrt(1 + xe5[0, k]**2 + ye5[0, k]**2)
    thetae_hat5[0, k] = thetae5[0, k] + np.arctan2(k0_5 * ye5[0, k], L1_5.item())
    L2_5 = np.sqrt(1 + xe5[0, k]**2 + (1 + k0_5**2) * ye5[0, k]**2)
    L3_5 = np.sqrt(1 + thetae_hat5[0, k]**2)
    
    # 计算非线性项
    if thetae_hat5[0, k] == 0:
        alp = np.cos(thetae5[0, k])
    else:
        alp = (1/thetae_hat5[0, k]) * (np.sin(thetae5[0, k]) + 
            np.sin(np.arctan2(k0_5 * ye5[0, k], L1_5)))
    
    M0_5 = (k0_5 * vr5[0, k+1] * np.sin(thetae5[0, k]) * (1 + xe5[0, k]**2) - 
            k0_5 * xe5[0, k] * ye5[0, k] * vr5[0, k+1] * np.cos(thetae5[0, k])) / \
            (L1_5 * (L2_5**2))
                    
    # 构建预测模型矩阵
    fxz_5[:, k] = np.array([
        xe5[0, k],
        ye5[0, k],
        thetae_hat5[0, k]
    ]) + t1 * np.array([
        vr5[0, k+1] * np.cos(thetae5[0, k]),
        vr5[0, k+1] * np.sin(thetae5[0, k]),
        wr5[0, k+1] + M0_5.item()
    ])
    
    # 输入矩阵
    gxxz_5 = t1 * np.array([
                [-1, ye5[0, k]],
                [0, -xe5[0, k]],
                [(k0_5 * xe5[0, k] * ye5[0, k])/(L1_5 * L2_5**2).item(), -(1 + (k0_5 * L1_5 * xe5[0, k])/(L2_5**2)).item()]           
                                                                                                                ])




    # 构建扩展预测模型矩阵
    zz_1 = np.zeros((3, 2))

    zz_2 = np.zeros((3, 2))

    zz_3 = np.zeros((3, 2))

    zz_4 = np.zeros((3, 2))

    zz_5 = np.zeros((3, 2))



    Gz_1 = np.vstack((
        np.hstack((gxxz_1, zz_1)),
        np.hstack((gxxz_1, gxxz_1)),
        np.hstack((gxxz_1, gxxz_1))  ))

    Gz_2 = np.vstack((
        np.hstack((gxxz_2, zz_2)),
        np.hstack((gxxz_2, gxxz_2)),
        np.hstack((gxxz_2, gxxz_2))  ))
    
    Gz_3 = np.vstack((
        np.hstack((gxxz_3, zz_3)),
        np.hstack((gxxz_3, gxxz_3)),
        np.hstack((gxxz_3, gxxz_3))  ))
    
    Gz_4 = np.vstack((
        np.hstack((gxxz_4, zz_4)),
        np.hstack((gxxz_4, gxxz_4)),
        np.hstack((gxxz_4, gxxz_4))  ))
    
    Gz_5 = np.vstack((
        np.hstack((gxxz_5, zz_5)),
        np.hstack((gxxz_5, gxxz_5)),
        np.hstack((gxxz_5, gxxz_5))  ))



    tildrgz_1 = np.vstack((
        gxxz_1 @ uz1[:, k].reshape(-1, 1),
        gxxz_1 @ uz1[:, k].reshape(-1, 1),
        gxxz_1 @ uz1[:, k].reshape(-1, 1)
    ))


    tildrgz_2 = np.vstack((
        gxxz_2 @ uz2[:, k].reshape(-1, 1),
        gxxz_2 @ uz2[:, k].reshape(-1, 1),
        gxxz_2 @ uz2[:, k].reshape(-1, 1)
    ))


    tildrgz_3 = np.vstack((
        gxxz_3 @ uz3[:, k].reshape(-1, 1),
        gxxz_3 @ uz3[:, k].reshape(-1, 1),
        gxxz_3 @ uz3[:, k].reshape(-1, 1)
    ))


    tildrgz_4 = np.vstack((
        gxxz_4 @ uz4[:, k].reshape(-1, 1),
        gxxz_4 @ uz4[:, k].reshape(-1, 1),
        gxxz_4 @ uz4[:, k].reshape(-1, 1)
    ))


    tildrgz_5 = np.vstack((
        gxxz_5 @ uz5[:, k].reshape(-1, 1),
        gxxz_5 @ uz5[:, k].reshape(-1, 1),
        gxxz_5 @ uz5[:, k].reshape(-1, 1)
    ))



    tildrfz_1 = np.vstack((
        fxz_1[:, k].reshape(-1, 1),
        fxz_1[:, k].reshape(-1, 1),
        fxz_1[:, k].reshape(-1, 1)
    ))

    tildrfz_2 = np.vstack((
        fxz_2[:, k].reshape(-1, 1),
        fxz_2[:, k].reshape(-1, 1),
        fxz_2[:, k].reshape(-1, 1)
    ))

    tildrfz_3 = np.vstack((
        fxz_3[:, k].reshape(-1, 1),
        fxz_3[:, k].reshape(-1, 1),
        fxz_3[:, k].reshape(-1, 1)
    ))

    tildrfz_4 = np.vstack((
        fxz_4[:, k].reshape(-1, 1),
        fxz_4[:, k].reshape(-1, 1),
        fxz_4[:, k].reshape(-1, 1)
    ))

    tildrfz_5 = np.vstack((
        fxz_5[:, k].reshape(-1, 1),
        fxz_5[:, k].reshape(-1, 1),
        fxz_5[:, k].reshape(-1, 1)
    ))


    tildrIz_1 = np.eye(4, 4) + np.vstack((
        np.zeros((2, 4)),
        np.hstack((np.eye(2, 2), np.zeros((2, 2))))
    ))

    tildrIz_2 = np.eye(4, 4) + np.vstack((
        np.zeros((2, 4)),
        np.hstack((np.eye(2, 2), np.zeros((2, 2))))
    ))

    tildrIz_3 = np.eye(4, 4) + np.vstack((
        np.zeros((2, 4)),
        np.hstack((np.eye(2, 2), np.zeros((2, 2))))
    ))

    tildrIz_4 = np.eye(4, 4) + np.vstack((
        np.zeros((2, 4)),
        np.hstack((np.eye(2, 2), np.zeros((2, 2))))
    ))

    tildrIz_5 = np.eye(4, 4) + np.vstack((
        np.zeros((2, 4)),
        np.hstack((np.eye(2, 2), np.zeros((2, 2))))
    ))
    


    Irnnz_1 = np.eye(4, 4)

    Irnnz_2 = np.eye(4, 4)

    Irnnz_3 = np.eye(4, 4)

    Irnnz_4 = np.eye(4, 4)

    Irnnz_5 = np.eye(4, 4)


    # 构建QP问题
    Wz_1 = 2 * (Gz_1.T @ Qz @ Gz_1 + Rz)
    Cz_1 = 2 * Gz_1.T @ Qz @ (tildrgz_1 + tildrfz_1)
    Ez_1 = np.vstack((
        -tildrIz_1,
        tildrIz_1,
        -Gz_1,
        Gz_1,
        Irnnz_1
    ))
    
    bz_1 = np.vstack((
        -abarUminz1 + abaruz1[:, k].reshape(-1, 1),
        abarUmaxz1 - abaruz1[:, k].reshape(-1, 1),
        -abarxminz1 + tildrfz_1 + tildrgz_1,
        abarxmaxz1 - tildrfz_1 - tildrgz_1,
        -detabarUminz1,
        detabarUmaxz1
    ))


    Wz_2 = 2 * (Gz_2.T @ Qz @ Gz_2 + Rz)
    Cz_2 = 2 * Gz_2.T @ Qz @ (tildrgz_2 + tildrfz_2)
    Ez_2 = np.vstack((
        -tildrIz_2,
        tildrIz_2,
        -Gz_2,
        Gz_2,
        Irnnz_2
    ))
    
    bz_2 = np.vstack((
        -abarUminz2 + abaruz2[:, k].reshape(-1, 1),
        abarUmaxz2 - abaruz2[:, k].reshape(-1, 1),
        -abarxminz2 + tildrfz_2 + tildrgz_2,
        abarxmaxz2 - tildrfz_2 - tildrgz_2,
        -detabarUminz2,
        detabarUmaxz2
    ))


    Wz_3 = 2 * (Gz_3.T @ Qz @ Gz_3 + Rz)
    Cz_3 = 2 * Gz_3.T @ Qz @ (tildrgz_3 + tildrfz_3)
    Ez_3 = np.vstack((
        -tildrIz_3,
        tildrIz_3,
        -Gz_3,
        Gz_3,
        Irnnz_3
    ))
    
    bz_3 = np.vstack((
        -abarUminz3 + abaruz3[:, k].reshape(-1, 1),
        abarUmaxz3 - abaruz3[:, k].reshape(-1, 1),
        -abarxminz3 + tildrfz_3 + tildrgz_3,
        abarxmaxz3 - tildrfz_3 - tildrgz_3,
        -detabarUminz3,
        detabarUmaxz3
    ))


    Wz_4 = 2 * (Gz_4.T @ Qz @ Gz_4 + Rz)
    Cz_4 = 2 * Gz_4.T @ Qz @ (tildrgz_4 + tildrfz_4)
    Ez_4 = np.vstack((
        -tildrIz_4,
        tildrIz_4,
        -Gz_4,
        Gz_4,
        Irnnz_4
    ))
    
    bz_4 = np.vstack((
        -abarUminz4 + abaruz4[:, k].reshape(-1, 1),
        abarUmaxz4 - abaruz1[:, k].reshape(-1, 1),
        -abarxminz4 + tildrfz_4 + tildrgz_4,
        abarxmaxz4 - tildrfz_4 - tildrgz_4,
        -detabarUminz4,
        detabarUmaxz4
    ))


    Wz_5 = 2 * (Gz_5.T @ Qz @ Gz_5 + Rz)
    Cz_5 = 2 * Gz_5.T @ Qz @ (tildrgz_5 + tildrfz_5)
    Ez_5 = np.vstack((
        -tildrIz_5,
        tildrIz_5,
        -Gz_5,
        Gz_5,
        Irnnz_5
    ))
    
    bz_5 = np.vstack((
        -abarUminz5 + abaruz5[:, k].reshape(-1, 1),
        abarUmaxz5 - abaruz5[:, k].reshape(-1, 1),
        -abarxminz5 + tildrfz_5 + tildrgz_5,
        abarxmaxz5 - tildrfz_5 - tildrgz_5,
        -detabarUminz5,
        detabarUmaxz5
    ))





    # 定义神经网络优化参数
    mz_1 = 4 * Nu + 6 * N
    myInfz_1 = 1e100
    Pinftyz_1 = myInfz_1 * np.ones((mz_1, 1))
    Minftyz_1 = -Pinftyz_1
    
    mz_2 = 4 * Nu + 6 * N
    myInfz_2 = 1e100
    Pinftyz_2 = myInfz_2 * np.ones((mz_2, 1))
    Minftyz_2 = -Pinftyz_2

    mz_3 = 4 * Nu + 6 * N
    myInfz_3 = 1e100
    Pinftyz_3 = myInfz_3 * np.ones((mz_3, 1))
    Minftyz_3 = -Pinftyz_3

    mz_4 = 4 * Nu + 6 * N
    myInfz_4 = 1e100
    Pinftyz_4 = myInfz_4 * np.ones((mz_4, 1))
    Minftyz_4 = -Pinftyz_4

    mz_5 = 4 * Nu + 6 * N
    myInfz_5 = 1e100
    Pinftyz_5 = myInfz_5 * np.ones((mz_5, 1))
    Minftyz_5 = -Pinftyz_5



    # 构建PDNN矩阵
    global Mz_1, pz_1, ypz_1, ymz_1, ImHz_1, IpHtz_1, RIpHtz_1
    pz_1 = -Ez_1 @ np.linalg.inv(Wz_1) @ Cz_1
    Mz_1 = -np.linalg.inv(Wz_1) @ Cz_1
    ypz_1 = np.vstack((bz_1, detabarUmaxz1))
    ymz_1 = np.vstack((Minftyz_1, detabarUminz1))
    ImHz_1 = Ez_1 @ np.linalg.inv(Wz_1) @ Ez_1.T
    IpHtz_1 = np.linalg.inv(Wz_1) @ Ez_1.T
    RIpHtz_1 = (np.linalg.inv(IpHtz_1 @ IpHtz_1.T) @ IpHtz_1).T

    global Mz_2, pz_2, ypz_2, ymz_2, ImHz_2, IpHtz_2, RIpHtz_2
    pz_2 = -Ez_2 @ np.linalg.inv(Wz_2) @ Cz_2
    Mz_2 = -np.linalg.inv(Wz_2) @ Cz_2
    ypz_2 = np.vstack((bz_2, detabarUmaxz2))
    ymz_2 = np.vstack((Minftyz_2, detabarUminz2))
    ImHz_2 = Ez_2 @ np.linalg.inv(Wz_2) @ Ez_2.T
    IpHtz_2 = np.linalg.inv(Wz_2) @ Ez_2.T
    RIpHtz_2 = (np.linalg.inv(IpHtz_2 @ IpHtz_2.T) @ IpHtz_2).T

    global Mz_3, pz_3, ypz_3, ymz_3, ImHz_3, IpHtz_3, RIpHtz_3
    pz_3 = -Ez_3 @ np.linalg.inv(Wz_3) @ Cz_3
    Mz_3 = -np.linalg.inv(Wz_3) @ Cz_3
    ypz_3 = np.vstack((bz_3, detabarUmaxz3))
    ymz_3 = np.vstack((Minftyz_3, detabarUminz3))
    ImHz_3 = Ez_3 @ np.linalg.inv(Wz_3) @ Ez_3.T
    IpHtz_3 = np.linalg.inv(Wz_3) @ Ez_3.T
    RIpHtz_3 = (np.linalg.inv(IpHtz_3 @ IpHtz_3.T) @ IpHtz_3).T

    global Mz_4, pz_4, ypz_4, ymz_4, ImHz_4, IpHtz_4, RIpHtz_4
    pz_4 = -Ez_4 @ np.linalg.inv(Wz_4) @ Cz_4
    Mz_4 = -np.linalg.inv(Wz_4) @ Cz_4
    ypz_4 = np.vstack((bz_4, detabarUmaxz4))
    ymz_4 = np.vstack((Minftyz_4, detabarUminz4))
    ImHz_4 = Ez_4 @ np.linalg.inv(Wz_4) @ Ez_4.T
    IpHtz_4 = np.linalg.inv(Wz_4) @ Ez_4.T
    RIpHtz_4 = (np.linalg.inv(IpHtz_4 @ IpHtz_4.T) @ IpHtz_4).T

    global Mz_5, pz_5, ypz_5, ymz_5, ImHz_5, IpHtz_5, RIpHtz_5
    pz_5 = -Ez_5 @ np.linalg.inv(Wz_5) @ Cz_5
    Mz_5 = -np.linalg.inv(Wz_5) @ Cz_5
    ypz_5 = np.vstack((bz_5, detabarUmaxz5))
    ymz_5 = np.vstack((Minftyz_5, detabarUminz5))
    ImHz_5 = Ez_5 @ np.linalg.inv(Wz_5) @ Ez_5.T
    IpHtz_5 = np.linalg.inv(Wz_5) @ Ez_5.T
    RIpHtz_5 = (np.linalg.inv(IpHtz_5 @ IpHtz_5.T) @ IpHtz_5).T



    # 使用龙格-库塔方法求解神经网络动态方程
    h = t1/10
    n = 10



    ycvz_1 = np.zeros((4, n+1, 1))
    ycvz_1[:, 0] = y0z1[:, k].reshape(-1, 1)

    ycvz_2 = np.zeros((4, n+1, 1))
    ycvz_2[:, 0] = y0z2[:, k].reshape(-1, 1)

    ycvz_3 = np.zeros((4, n+1, 1))
    ycvz_3[:, 0] = y0z3[:, k].reshape(-1, 1)

    ycvz_4 = np.zeros((4, n+1, 1))
    ycvz_4[:, 0] = y0z4[:, k].reshape(-1, 1)

    ycvz_5 = np.zeros((4, n+1, 1))
    ycvz_5[:, 0] = y0z5[:, k].reshape(-1, 1)


    for ii in range(n):
        k11_1 = (-IpHtz_1 @ (ImHz_1 @ RIpHtz_1 @ (ycvz_1[:, ii] - Mz_1) - 
                        gfunction2z_1(ImHz_1 @ RIpHtz_1 @ (ycvz_1[:, ii] - Mz_1) - 
                                RIpHtz_1 @ (ycvz_1[:, ii] - Mz_1) + pz_1) + pz_1))/gamma
        k21_1 = (-IpHtz_1 @ (ImHz_1 @ RIpHtz_1 @ ((ycvz_1[:, ii] + h*k11_1/2) - Mz_1) - 
                        gfunction2z_1(ImHz_1 @ RIpHtz_1 @ ((ycvz_1[:, ii] + h*k11_1/2) - Mz_1) - 
                                RIpHtz_1 @ ((ycvz_1[:, ii] + h*k11_1/2) - Mz_1) + pz_1) + pz_1))/gamma
        k31_1 = (-IpHtz_1 @ (ImHz_1 @ RIpHtz_1 @ ((ycvz_1[:, ii] + h*k21_1/2) - Mz_1) - 
                        gfunction2z_1(ImHz_1 @ RIpHtz_1 @ ((ycvz_1[:, ii] + h*k21_1/2) - Mz_1) - 
                                RIpHtz_1 @ ((ycvz_1[:, ii] + h*k21_1/2) - Mz_1) + pz_1) + pz_1))/gamma
        k41_1 = (-IpHtz_1 @ (ImHz_1 @ RIpHtz_1 @ ((ycvz_1[:, ii] + h*k31_1) - Mz_1) - 
                        gfunction2z_1(ImHz_1 @ RIpHtz_1 @ ((ycvz_1[:, ii] + h*k31_1) - Mz_1) - 
                                RIpHtz_1 @ ((ycvz_1[:, ii] + h*k31_1) - Mz_1) + pz_1) + pz_1))/gamma
        ycvz_1[:, ii+1] = ycvz_1[:, ii] + h*(k11_1 + 2*k21_1 + 2*k31_1 + k41_1)/6


    dot_y1z_1 = ycvz_1[:, n]
    y0z1[:, k+1] = dot_y1z_1.reshape(-1)
    az_1 = y0z1[:, k+1]

    detabarUz1[:, k+1] = az_1[0:2*Nu]
    ddz_1 = detabarUz1[:, k+1]
    abaruz1[:, k+1] = ddz_1
    uz1[:, k+1] = abaruz1[0:2, k+1]

    
    for ii in range(n):
        k11_2 = (-IpHtz_2 @ (ImHz_2 @ RIpHtz_2 @ (ycvz_2[:, ii] - Mz_2) - 
                        gfunction2z_2(ImHz_2 @ RIpHtz_2 @ (ycvz_2[:, ii] - Mz_2) - 
                                RIpHtz_2 @ (ycvz_2[:, ii] - Mz_2) + pz_2) + pz_2))/gamma
        k21_2 = (-IpHtz_2 @ (ImHz_2 @ RIpHtz_2 @ ((ycvz_2[:, ii] + h*k11_2/2) - Mz_2) - 
                        gfunction2z_2(ImHz_2 @ RIpHtz_2 @ ((ycvz_2[:, ii] + h*k11_2/2) - Mz_2) - 
                                RIpHtz_2 @ ((ycvz_2[:, ii] + h*k11_2/2) - Mz_2) + pz_2) + pz_2))/gamma
        k31_2 = (-IpHtz_2 @ (ImHz_2 @ RIpHtz_2 @ ((ycvz_2[:, ii] + h*k21_2/2) - Mz_2) - 
                        gfunction2z_2(ImHz_2 @ RIpHtz_2 @ ((ycvz_2[:, ii] + h*k21_2/2) - Mz_2) - 
                                RIpHtz_2 @ ((ycvz_2[:, ii] + h*k21_2/2) - Mz_2) + pz_2) + pz_2))/gamma
        k41_2 = (-IpHtz_2 @ (ImHz_2 @ RIpHtz_2 @ ((ycvz_2[:, ii] + h*k31_2) - Mz_2) - 
                        gfunction2z_2(ImHz_2 @ RIpHtz_2 @ ((ycvz_2[:, ii] + h*k31_2) - Mz_2) - 
                                RIpHtz_2 @ ((ycvz_2[:, ii] + h*k31_2) - Mz_2) + pz_2) + pz_2))/gamma
        ycvz_2[:, ii+1] = ycvz_2[:, ii] + h*(k11_2 + 2*k21_2 + 2*k31_2 + k41_2)/6


    dot_y1z_2 = ycvz_2[:, n]
    y0z2[:, k+1] = dot_y1z_2.reshape(-1)
    az_2 = y0z2[:, k+1]

    detabarUz2[:, k+1] = az_2[0:2*Nu]
    ddz_2 = detabarUz2[:, k+1]
    abaruz2[:, k+1] = ddz_2
    uz2[:, k+1] = abaruz2[0:2, k+1]


    
    for ii in range(n):
        k11_3 = (-IpHtz_3 @ (ImHz_3 @ RIpHtz_3 @ (ycvz_3[:, ii] - Mz_3) - 
                        gfunction2z_3(ImHz_3 @ RIpHtz_3 @ (ycvz_3[:, ii] - Mz_3) - 
                                RIpHtz_3 @ (ycvz_3[:, ii] - Mz_3) + pz_3) + pz_3))/gamma
        k21_3 = (-IpHtz_3 @ (ImHz_3 @ RIpHtz_3 @ ((ycvz_3[:, ii] + h*k11_3/2) - Mz_3) - 
                        gfunction2z_3(ImHz_3 @ RIpHtz_3 @ ((ycvz_3[:, ii] + h*k11_3/2) - Mz_3) - 
                                RIpHtz_3 @ ((ycvz_3[:, ii] + h*k11_3/2) - Mz_3) + pz_3) + pz_3))/gamma
        k31_3 = (-IpHtz_3 @ (ImHz_3 @ RIpHtz_3 @ ((ycvz_3[:, ii] + h*k21_3/2) - Mz_3) - 
                        gfunction2z_3(ImHz_3 @ RIpHtz_3 @ ((ycvz_3[:, ii] + h*k21_3/2) - Mz_3) - 
                                RIpHtz_3 @ ((ycvz_3[:, ii] + h*k21_3/2) - Mz_3) + pz_3) + pz_3))/gamma
        k41_3 = (-IpHtz_3 @ (ImHz_3 @ RIpHtz_3 @ ((ycvz_3[:, ii] + h*k31_3) - Mz_3) - 
                        gfunction2z_3(ImHz_3 @ RIpHtz_3 @ ((ycvz_3[:, ii] + h*k31_3) - Mz_3) - 
                                RIpHtz_3 @ ((ycvz_3[:, ii] + h*k31_3) - Mz_3) + pz_3) + pz_3))/gamma
        ycvz_3[:, ii+1] = ycvz_3[:, ii] + h*(k11_3 + 2*k21_3 + 2*k31_3 + k41_3)/6


    dot_y1z_3 = ycvz_3[:, n]
    y0z3[:, k+1] = dot_y1z_3.reshape(-1)
    az_3 = y0z3[:, k+1]

    detabarUz3[:, k+1] = az_3[0:2*Nu]
    ddz_3 = detabarUz3[:, k+1]
    abaruz3[:, k+1] = ddz_3
    uz3[:, k+1] = abaruz3[0:2, k+1]


    
    for ii in range(n):
        k11_4 = (-IpHtz_4 @ (ImHz_4 @ RIpHtz_4 @ (ycvz_4[:, ii] - Mz_4) - 
                        gfunction2z_4(ImHz_4 @ RIpHtz_4 @ (ycvz_4[:, ii] - Mz_4) - 
                                RIpHtz_4 @ (ycvz_4[:, ii] - Mz_4) + pz_4) + pz_4))/gamma
        k21_4 = (-IpHtz_4 @ (ImHz_4 @ RIpHtz_4 @ ((ycvz_4[:, ii] + h*k11_4/2) - Mz_4) - 
                        gfunction2z_4(ImHz_4 @ RIpHtz_4 @ ((ycvz_4[:, ii] + h*k11_4/2) - Mz_4) - 
                                RIpHtz_4 @ ((ycvz_4[:, ii] + h*k11_4/2) - Mz_4) + pz_4) + pz_4))/gamma
        k31_4 = (-IpHtz_4 @ (ImHz_4 @ RIpHtz_4 @ ((ycvz_4[:, ii] + h*k21_4/2) - Mz_4) - 
                        gfunction2z_4(ImHz_4 @ RIpHtz_4 @ ((ycvz_4[:, ii] + h*k21_4/2) - Mz_4) - 
                                RIpHtz_4 @ ((ycvz_4[:, ii] + h*k21_4/2) - Mz_4) + pz_4) + pz_4))/gamma
        k41_4 = (-IpHtz_4 @ (ImHz_4 @ RIpHtz_4 @ ((ycvz_4[:, ii] + h*k31_4) - Mz_4) - 
                        gfunction2z_4(ImHz_4 @ RIpHtz_4 @ ((ycvz_4[:, ii] + h*k31_4) - Mz_4) - 
                                RIpHtz_4 @ ((ycvz_4[:, ii] + h*k31_4) - Mz_4) + pz_4) + pz_4))/gamma
        ycvz_4[:, ii+1] = ycvz_4[:, ii] + h*(k11_4 + 2*k21_4 + 2*k31_4 + k41_4)/6


    dot_y1z_4 = ycvz_4[:, n]
    y0z4[:, k+1] = dot_y1z_4.reshape(-1)
    az_4 = y0z4[:, k+1]

    detabarUz4[:, k+1] = az_4[0:2*Nu]
    ddz_4 = detabarUz4[:, k+1]
    abaruz4[:, k+1] = ddz_4
    uz4[:, k+1] = abaruz4[0:2, k+1]


    
    for ii in range(n):
        k11_5 = (-IpHtz_5 @ (ImHz_5 @ RIpHtz_5 @ (ycvz_5[:, ii] - Mz_5) - 
                        gfunction2z_5(ImHz_5 @ RIpHtz_5 @ (ycvz_5[:, ii] - Mz_5) - 
                                RIpHtz_5 @ (ycvz_5[:, ii] - Mz_5) + pz_5) + pz_5))/gamma
        k21_5 = (-IpHtz_5 @ (ImHz_5 @ RIpHtz_5 @ ((ycvz_5[:, ii] + h*k11_5/2) - Mz_5) - 
                        gfunction2z_5(ImHz_5 @ RIpHtz_5 @ ((ycvz_5[:, ii] + h*k11_5/2) - Mz_5) - 
                                RIpHtz_5 @ ((ycvz_5[:, ii] + h*k11_5/2) - Mz_5) + pz_5) + pz_5))/gamma
        k31_5 = (-IpHtz_5 @ (ImHz_5 @ RIpHtz_5 @ ((ycvz_5[:, ii] + h*k21_5/2) - Mz_5) - 
                        gfunction2z_5(ImHz_5 @ RIpHtz_5 @ ((ycvz_5[:, ii] + h*k21_5/2) - Mz_5) - 
                                RIpHtz_5 @ ((ycvz_5[:, ii] + h*k21_5/2) - Mz_5) + pz_5) + pz_5))/gamma
        k41_5 = (-IpHtz_5 @ (ImHz_5 @ RIpHtz_5 @ ((ycvz_5[:, ii] + h*k31_5) - Mz_5) - 
                        gfunction2z_5(ImHz_5 @ RIpHtz_5 @ ((ycvz_5[:, ii] + h*k31_5) - Mz_5) - 
                                RIpHtz_5 @ ((ycvz_5[:, ii] + h*k31_5) - Mz_5) + pz_5) + pz_5))/gamma
        ycvz_5[:, ii+1] = ycvz_5[:, ii] + h*(k11_5 + 2*k21_5 + 2*k31_5 + k41_5)/6


    dot_y1z_5 = ycvz_5[:, n]
    y0z5[:, k+1] = dot_y1z_5.reshape(-1)
    az_5 = y0z5[:, k+1]

    detabarUz5[:, k+1] = az_5[0:2*Nu]
    ddz_5 = detabarUz5[:, k+1]
    abaruz5[:, k+1] = ddz_5
    uz5[:, k+1] = abaruz5[0:2, k+1]
    # if k<= 2:
    #     print(f"时间步={k}, uz1={uz1[:, k+1]}, uz2={uz2[:, k+1]}, uz3={uz3[:, k+1]}, uz4={uz4[:, k+1]}, uz5={uz5[:, k+1]}")

    # 实际控制输入限制和更新
    # 限制线速度
    if uz1[0, k+1] >= 0.22:
        uz1[0, k+1] = 0.22
    elif uz1[0, k+1] < -0.22:
        uz1[0, k+1] = -0.22
    
    # 限制角速度
    if uz1[1, k+1] >= 2.84:
        uz1[1, k+1] = 2.84
    elif uz1[1, k+1] < -2.84:
        uz1[1, k+1] = -2.84
    
    vc1[0, k+1] = uz1[0, k+1]
    wc1[0, k+1] = uz1[1, k+1]
    
    rrr = 0  # 模拟扰动
    # 更新机器人位姿
    thetac1[0, k+1] = thetac1[0, k] + t1 * wc1[0, k+1]
    
    # 位姿跨象限调整
    if thetac1[0, k+1] >= np.pi:
        thetac1[0, k+1] = thetac1[0, k+1] - 2 * np.pi
    elif thetac1[0, k+1] <= -np.pi:
        thetac1[0, k+1] = thetac1[0, k+1] + 2 * np.pi
    


    if uz2[0, k+1] >= 0.22:
        uz2[0, k+1] = 0.22
    elif uz2[0, k+1] < -0.22:
        uz2[0, k+1] = -0.22
    
    # 限制角速度
    if uz2[1, k+1] >= 2.84:
        uz2[1, k+1] = 2.84
    elif uz2[1, k+1] < -2.84:
        uz2[1, k+1] = -2.84
    
    vc2[0, k+1] = uz2[0, k+1]
    wc2[0, k+1] = uz2[1, k+1]
    
    rrr = 0  # 模拟扰动
    # 更新机器人位姿
    thetac2[0, k+1] = thetac2[0, k] + t1 * wc2[0, k+1]
    
    # 位姿跨象限调整
    if thetac2[0, k+1] >= np.pi:
        thetac2[0, k+1] = thetac2[0, k+1] - 2 * np.pi
    elif thetac2[0, k+1] <= -np.pi:
        thetac2[0, k+1] = thetac2[0, k+1] + 2 * np.pi



    if uz3[0, k+1] >= 0.22:
        uz3[0, k+1] = 0.22
    elif uz3[0, k+1] < -0.22:
        uz3[0, k+1] = -0.22
    
    # 限制角速度
    if uz3[1, k+1] >= 2.84:
        uz3[1, k+1] = 2.84
    elif uz3[1, k+1] < -2.84:
        uz3[1, k+1] = -2.84
    
    vc3[0, k+1] = uz3[0, k+1]
    wc3[0, k+1] = uz3[1, k+1]
    
    rrr = 0  # 模拟扰动
    # 更新机器人位姿
    thetac3[0, k+1] = thetac3[0, k] + t1 * wc3[0, k+1]
    
    # 位姿跨象限调整
    if thetac3[0, k+1] >= np.pi:
        thetac3[0, k+1] = thetac3[0, k+1] - 2 * np.pi
    elif thetac3[0, k+1] <= -np.pi:
        thetac3[0, k+1] = thetac3[0, k+1] + 2 * np.pi



    if uz4[0, k+1] >= 0.22:
        uz4[0, k+1] = 0.22
    elif uz4[0, k+1] < -0.22:
        uz4[0, k+1] = -0.22
    
    # 限制角速度
    if uz4[1, k+1] >= 2.84:
        uz4[1, k+1] = 2.84
    elif uz4[1, k+1] < -2.84:
        uz4[1, k+1] = -2.84
    
    vc4[0, k+1] = uz4[0, k+1]
    wc4[0, k+1] = uz4[1, k+1]
    
    rrr = 0  # 模拟扰动
    # 更新机器人位姿
    thetac4[0, k+1] = thetac4[0, k] + t1 * wc4[0, k+1]
    
    # 位姿跨象限调整
    if thetac4[0, k+1] >= np.pi:
        thetac4[0, k+1] = thetac4[0, k+1] - 2 * np.pi
    elif thetac4[0, k+1] <= -np.pi:
        thetac4[0, k+1] = thetac4[0, k+1] + 2 * np.pi



    if uz5[0, k+1] >= 0.22:
        uz5[0, k+1] = 0.22
    elif uz5[0, k+1] < -0.22:
        uz5[0, k+1] = -0.22
    
    # 限制角速度
    if uz5[1, k+1] >= 2.84:
        uz5[1, k+1] = 2.84
    elif uz5[1, k+1] < -2.84:
        uz5[1, k+1] = -2.84
    
    vc5[0, k+1] = uz5[0, k+1]
    wc5[0, k+1] = uz5[1, k+1]
    
    # print(f"时间步={k+1}, "
    #       f"机器人1：速度={vc1[0, k+1]:.3f}, 角速度={wc1[0, k+1]:.3f} | "
    #       f"机器人2：速度={vc2[0, k+1]:.3f}, 角速度={wc2[0, k+1]:.3f} | "
    #       f"机器人3：速度={vc3[0, k+1]:.3f}, 角速度={wc3[0, k+1]:.3f} | "
    #       f"机器人4：速度={vc4[0, k+1]:.3f}, 角速度={wc4[0, k+1]:.3f} | "
    #       f"机器人5：速度={vc5[0, k+1]:.3f}, 角速度={wc5[0, k+1]:.3f})")


    rrr = 0  # 模拟扰动
    # 更新机器人位姿
    thetac5[0, k+1] = thetac5[0, k] + t1 * wc5[0, k+1]
    
    # 位姿跨象限调整
    if thetac5[0, k+1] >= np.pi:
        thetac5[0, k+1] = thetac5[0, k+1] - 2 * np.pi
    elif thetac5[0, k+1] <= -np.pi:
        thetac5[0, k+1] = thetac5[0, k+1] + 2 * np.pi


    # 更新机器人位置
    
    xc1[0, k+1] = xc1[0, k] + vc1[0, k+1] * t1 * np.cos(thetac1[0, k+1]) + \
                (np.random.random() - 0.5) * rrr
    yc1[0, k+1] = yc1[0, k] + vc1[0, k+1] * t1 * np.sin(thetac1[0, k+1]) + \
                (np.random.random() - 0.5) * rrr

    xc2[0, k+1] = xc2[0, k] + vc2[0, k+1] * t1 * np.cos(thetac2[0, k+1]) + \
                (np.random.random() - 0.5) * rrr
    yc2[0, k+1] = yc2[0, k] + vc2[0, k+1] * t1 * np.sin(thetac2[0, k+1]) + \
                (np.random.random() - 0.5) * rrr
    
    xc3[0, k+1] = xc3[0, k] + vc3[0, k+1] * t1 * np.cos(thetac3[0, k+1]) + \
                (np.random.random() - 0.5) * rrr
    yc3[0, k+1] = yc3[0, k] + vc3[0, k+1] * t1 * np.sin(thetac3[0, k+1]) + \
                (np.random.random() - 0.5) * rrr
    
    xc4[0, k+1] = xc4[0, k] + vc4[0, k+1] * t1 * np.cos(thetac4[0, k+1]) + \
                (np.random.random() - 0.5) * rrr
    yc4[0, k+1] = yc4[0, k] + vc4[0, k+1] * t1 * np.sin(thetac4[0, k+1]) + \
                (np.random.random() - 0.5) * rrr

    xc5[0, k+1] = xc5[0, k] + vc5[0, k+1] * t1 * np.cos(thetac5[0, k+1]) + \
                (np.random.random() - 0.5) * rrr
    yc5[0, k+1] = yc5[0, k] + vc5[0, k+1] * t1 * np.sin(thetac5[0, k+1]) + \
                (np.random.random() - 0.5) * rrr




    # 更新质心位置
    xccc[0, k+1] = np.sum(xc1[:, k+1]+xc2[:, k+1]+xc3[:, k+1]+xc4[:, k+1]+xc5[:, k+1])/Rnum
    yccc[0, k+1] = np.sum(yc1[:, k+1]+yc2[:, k+1]+yc3[:, k+1]+yc4[:, k+1]+yc5[:, k+1])/Rnum

    # 存储位置误差
    
    # zx1[:, k+1] = np.array([
    #     x_hat1[0, k+1] - px1[0, k+1],
    #     y_hat1[0, k+1] - py1[0, k+1]
    # ])

    # zx2[:, k+1] = np.array([
    #     x_hat2[0, k+1] - px2[0, k+1],
    #     y_hat2[0, k+1] - py2[0, k+1]
    # ])

    # zx3[:, k+1] = np.array([
    #     x_hat3[0, k+1] - px3[0, k+1],
    #     y_hat3[0, k+1] - py3[0, k+1]
    # ])


    # zx4[:, k+1] = np.array([
    #     x_hat4[0, k+1] - px4[0, k+1],
    #     y_hat4[0, k+1] - py4[0, k+1]
    # ])


    # zx5[:, k+1] = np.array([
    #     x_hat5[0, k+1] - px5[0, k+1],
    #     y_hat5[0, k+1] - py5[0, k+1]
    # ])


    # z0[:, k+1] = np.array([x0[0, k+1], y0[0, k+1]])

    t2 = t2 + t1


# 可视化
tclc = np.array([1, int(k/2), k+1])



# 图1：机器人轨迹（含障碍物）
plt.figure(1, figsize=(10, 8))

# 绘制机器人轨迹
plt.plot(xc1[0, :], yc1[0, :], linewidth=2, label='Robot_1')
plt.plot(xc2[0, :], yc2[0, :], linewidth=2, label='Robot_2')
plt.plot(xc3[0, :], yc3[0, :], linewidth=2, label='Robot_3')
plt.plot(xc4[0, :], yc4[0, :], linewidth=2, label='Robot_4')
plt.plot(xc5[0, :], yc5[0, :], linewidth=2, label='Robot_5')

plt.plot(x0[0, :], y0[0, :], '--', linewidth=2, label='Robot_L')
plt.plot(xccc[0, :], yccc[0, :], linewidth=2, label='Actual centroid')

# 绘制障碍物 - 根据新的28个障碍物配置
colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan',
          'magenta', 'yellow', 'lime', 'teal', 'navy', 'maroon', 'gold', 'coral', 'salmon', 'khaki',
          'plum', 'tan', 'lightblue', 'lightgreen', 'wheat', 'lavender', 'silver', 'darkgray']

# 绘制每个障碍物
for obs_idx in range(n_obstacles):
    start_idx = obs_idx * points_per_obstacle
    end_idx = (obs_idx + 1) * points_per_obstacle
    
    obs_x = xobs[start_idx:end_idx]
    obs_y = yobs[start_idx:end_idx]
    
    # 根据障碍物类型选择不同的绘制样式
    obs_config = obstacles_config[obs_idx]
    if obs_config['type'] == 'cylinder':
        plt.plot(obs_x, obs_y, 'o', color=colors[obs_idx % len(colors)], 
                markersize=2, alpha=0.7, label=f'{obs_config["name"]} (R={obs_config["radius"]:.3f})')
    else:
        plt.plot(obs_x, obs_y, 's', color=colors[obs_idx % len(colors)], 
                markersize=2, alpha=0.7, label=f'{obs_config["name"]} ({obs_config["width"]:.2f}×{obs_config["height"]:.2f})')

# 或者简化显示，只显示边界点而不显示标签
plt.plot(xobs, yobs, 'ko', markersize=1, alpha=0.6, label='All Obstacles')

# 绘制编队连线（在几个关键时刻）
for j in range(3):
    plt.plot([xc1[0, tclc[j]], xc2[0, tclc[j]]],
            [yc1[0, tclc[j]], yc2[0, tclc[j]]],
            color=[0.7, 0.3, 0.9], linewidth=3, alpha=0.7)

    plt.plot([xc2[0, tclc[j]], xc3[0, tclc[j]]],
            [yc2[0, tclc[j]], yc3[0, tclc[j]]],
            color=[0.7, 0.3, 0.9], linewidth=3, alpha=0.7)

    plt.plot([xc3[0, tclc[j]], xc4[0, tclc[j]]],
            [yc3[0, tclc[j]], yc4[0, tclc[j]]],
            color=[0.7, 0.3, 0.9], linewidth=3, alpha=0.7)

    plt.plot([xc4[0, tclc[j]], xc5[0, tclc[j]]],
            [yc4[0, tclc[j]], yc5[0, tclc[j]]],
            color=[0.7, 0.3, 0.9], linewidth=3, alpha=0.7)

    plt.plot([xc5[0, tclc[j]], xc1[0, tclc[j]]],
            [yc5[0, tclc[j]], yc1[0, tclc[j]]],
            color=[0.7, 0.3, 0.9], linewidth=3, alpha=0.7)

plt.axis('equal')
plt.xlabel('X coordinate (m)')
plt.ylabel('Y coordinate (m)')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True, alpha=0.3)
plt.title('Robot Trajectories with Obstacles')


# 图2：机器人与障碍物最小距离
plt.figure(2, figsize=(10, 6))

plt.plot(t[:-1], dobsmin_1[0, :], linewidth=2, label='dobsmin_1')
plt.plot(t[:-1], dobsmin_2[0, :], linewidth=2, label='dobsmin_2')
plt.plot(t[:-1], dobsmin_3[0, :], linewidth=2, label='dobsmin_3')
plt.plot(t[:-1], dobsmin_4[0, :], linewidth=2, label='dobsmin_4')
plt.plot(t[:-1], dobsmin_5[0, :], linewidth=2, label='dobsmin_5')

# 添加安全距离阈值线
plt.axhline(y=ord_safe, color='red', linestyle='--', linewidth=2, 
           label=f'Safety threshold ({ord_safe}m)', alpha=0.8)
plt.axhline(y=ord_avoid, color='orange', linestyle=':', linewidth=2, 
           label=f'Avoidance threshold ({ord_avoid}m)', alpha=0.8)

plt.xlabel('Time (s)')
plt.ylabel('Min distance of obstacle')
plt.legend()
plt.grid(True, alpha=0.3)
plt.title('Minimum Distance between Robots and Obstacles')
plt.xlim([0, k*t1])
plt.ylim([0, 4.0])  # 根据图像调整y轴范围

# 图3：线速度
plt.figure(3)

plt.plot(t, vc1[0, :], linewidth=2)
plt.plot(t, vc2[0, :], linewidth=2)
plt.plot(t, vc3[0, :], linewidth=2)
plt.plot(t, vc4[0, :], linewidth=2)
plt.plot(t, vc5[0, :], linewidth=2)


plt.plot(t, v0[0, :], '--', linewidth=2)
plt.axis([0, k*0.1, -0.51, 0.51])
plt.grid(True)
plt.xlabel('Time(s)')
plt.ylabel('Linear velocities')
plt.legend(['v_1', 'v_2', 'v_3', 'v_4', 'v_5', 'v_L'])

# 图4：角速度
plt.figure(4)

plt.plot(t, wc1[0, :], linewidth=2)
plt.plot(t, wc2[0, :], linewidth=2)
plt.plot(t, wc3[0, :], linewidth=2)
plt.plot(t, wc4[0, :], linewidth=2)
plt.plot(t, wc5[0, :], linewidth=2)


plt.plot(t, w0[0, :], '--', linewidth=2)
plt.axis([0, k*0.1, -2.6, 2.6])
plt.grid(True)
plt.xlabel('Time(s)')
plt.ylabel('Angular velocities')
plt.legend(['ω_1', 'ω_2', 'ω_3', 'ω_4', 'ω_5', 'ω_L'])

# 图5：X方向误差
plt.figure(5)

plt.plot(t, xc1[0, :] - z0[0, :] - px1[0, :], linewidth=2)
plt.plot(t, xc2[0, :] - z0[0, :] - px2[0, :], linewidth=2)
plt.plot(t, xc3[0, :] - z0[0, :] - px3[0, :], linewidth=2)
plt.plot(t, xc4[0, :] - z0[0, :] - px4[0, :], linewidth=2)
plt.plot(t, xc5[0, :] - z0[0, :] - px5[0, :], linewidth=2)


plt.grid(True)
plt.xlabel('Time(s)')
plt.ylabel('Errors of x_i')
plt.legend(['x_1-x_L-p_1x', 'x_2-x_L-p_2x', 'x_3-x_L-p_3x', 
           'x_4-x_L-p_4x', 'x_5-x_L-p_5x'])





# 图6的Y方向误差部分
plt.figure(6)

plt.plot(t, yc1[0, :] - z0[1, :] - py1[0, :], linewidth=2)
plt.plot(t, yc2[0, :] - z0[1, :] - py2[0, :], linewidth=2)
plt.plot(t, yc3[0, :] - z0[1, :] - py3[0, :], linewidth=2)
plt.plot(t, yc4[0, :] - z0[1, :] - py4[0, :], linewidth=2)
plt.plot(t, yc5[0, :] - z0[1, :] - py5[0, :], linewidth=2)



plt.grid(True)
plt.xlabel('Time(s)')
plt.ylabel('Errors of y_i')
plt.legend(['y_1-y_L-p_1y', 'y_2-y_L-p_2y', 'y_3-y_L-p_3y', 
           'y_4-y_L-p_4y', 'y_5-y_L-p_5y'])




# 图7：航向角误差
plt.figure(7)

plt.plot(t, thetac1[0, :] - theta0[0, :], linewidth=2)
plt.plot(t, thetac2[0, :] - theta0[0, :], linewidth=2)
plt.plot(t, thetac3[0, :] - theta0[0, :], linewidth=2)
plt.plot(t, thetac4[0, :] - theta0[0, :], linewidth=2)
plt.plot(t, thetac5[0, :] - theta0[0, :], linewidth=2)

plt.grid(True)
plt.xlabel('Time(s)')
plt.ylabel('Errors of θ_i')
plt.legend(['θ_1-θ_L', 'θ_2-θ_L', 'θ_3-θ_L', 'θ_4-θ_L', 'θ_5-θ_L'])


# # 图7：实际朝向角
# plt.figure(7)

# plt.plot(t, thetac1[0, :], linewidth=2)
# plt.plot(t, thetac2[0, :], linewidth=2)
# plt.plot(t, thetac3[0, :], linewidth=2)
# plt.plot(t, thetac4[0, :], linewidth=2)
# plt.plot(t, thetac5[0, :], linewidth=2)

# plt.grid(True)
# plt.xlabel('Time(s)')
# plt.ylabel('θ_i')
# plt.legend(['θ_1', 'θ_2', 'θ_3', 'θ_4', 'θ_5'])

# # 图8：领导者朝向角
# plt.figure(8)
# plt.plot(t, theta0[0, :], linewidth=2)
# plt.grid(True)
# plt.xlabel('Time(s)')
# plt.ylabel('θ_L')

# # 图9：实际X位置
# plt.figure(9)

# plt.plot(t, xc1[0, :], linewidth=2)
# plt.plot(t, xc2[0, :], linewidth=2)
# plt.plot(t, xc3[0, :], linewidth=2)
# plt.plot(t, xc4[0, :], linewidth=2)
# plt.plot(t, xc5[0, :], linewidth=2)


# plt.grid(True)
# plt.xlabel('Time(s)')
# plt.ylabel(' x_i')
# plt.legend(['x_1', 'x_2', 'x_3', 'x_4', 'x_5'])


# # 图10：实际领导者位置
# plt.figure(10)

# plt.plot(t,  z0[0, :] , linewidth=2)
# plt.grid(True)
# plt.xlabel('Time(s)')
# plt.ylabel('x_L')
# plt.legend(['x_L'])


# # 图11：x方向偏移
# plt.figure(11)

# plt.plot(t, px1[0, :], linewidth=2)
# plt.plot(t, px2[0, :], linewidth=2)
# plt.plot(t, px3[0, :], linewidth=2)
# plt.plot(t, px4[0, :], linewidth=2)
# plt.plot(t, px5[0, :], linewidth=2)

# plt.grid(True)
# plt.xlabel('Time(s)')
# plt.ylabel('p_xi')
# plt.legend(['p_1x', 'p_2x', 'p_3x', 'p_4x', 'p_5x'])


# # 图12：Y方向实际位置
# plt.figure(12)

# plt.plot(t, yc1[0, :] ,linewidth=2)
# plt.plot(t, yc2[0, :], linewidth=2)
# plt.plot(t, yc3[0, :], linewidth=2)
# plt.plot(t, yc4[0, :], linewidth=2)
# plt.plot(t, yc5[0, :], linewidth=2)



# plt.grid(True)
# plt.xlabel('Time(s)')
# plt.ylabel(' y_i')
# plt.legend(['y_1', 'y_2', 'y_3', 'y_4', 'y_5'])


# # 图13：领导者Y方向位置
# plt.figure(13)

# plt.plot(t,  z0[1, :], linewidth=2)
# plt.grid(True)
# plt.xlabel('Time(s)')
# plt.ylabel('y_L')
# plt.legend(['y_L'])



# # 图14：Y方向偏移
# plt.figure(14)

# plt.plot(t,  py1[0, :], linewidth=2)
# plt.plot(t,  py2[0, :], linewidth=2)
# plt.plot(t,  py3[0, :], linewidth=2)
# plt.plot(t,  py4[0, :], linewidth=2)
# plt.plot(t,  py5[0, :], linewidth=2)

# plt.grid(True)
# plt.xlabel('Time(s)')
# plt.ylabel('py_i')
# plt.legend(['p_1y', 'p_2y', 'p_3y', 'p_4y', 'p_5y'])


# # 图15：线速度
# plt.figure(15)
# plt.plot(t, vc1[0, :], linewidth=2)
# plt.plot(t, vc2[0, :], linewidth=2)
# plt.plot(t, vc3[0, :], linewidth=2)
# plt.plot(t, vc4[0, :], linewidth=2)
# plt.plot(t, vc5[0, :], linewidth=2)
# plt.grid(True)
# plt.xlabel('Time(s)')
# plt.ylabel(' v_i')
# plt.legend(['v_1', 'v_2', 'v_3', 'v_4', 'v_5'])

# # 图16：角速度
# plt.figure(16)
# plt.plot(t, wc1[0, :], linewidth=2)
# plt.plot(t, wc2[0, :], linewidth=2)
# plt.plot(t, wc3[0, :], linewidth=2)
# plt.plot(t, wc4[0, :], linewidth=2)
# plt.plot(t, wc5[0, :], linewidth=2)
# plt.grid(True)
# plt.xlabel('Time(s)')
# plt.ylabel(' ω_i')
# plt.legend(['ω_1', 'ω_2', 'ω_3', 'ω_4', 'ω_5'])


# # 图17：轨迹规划ux
# plt.figure(17)
# plt.plot(t, ux1[0, :], linewidth=2)
# plt.plot(t, ux2[0, :], linewidth=2)
# plt.plot(t, ux3[0, :], linewidth=2)
# plt.plot(t, ux4[0, :], linewidth=2)
# plt.plot(t, ux5[0, :], linewidth=2)
# plt.grid(True)
# plt.xlabel('Time(s)')
# plt.ylabel(' u_x')
# plt.legend(['u_x1', 'u_x2', 'u_x3', 'u_x4', 'u_x5'])

# # 图18：轨迹规划uy
# plt.figure(18)
# plt.plot(t, uy1[0, :], linewidth=2)
# plt.plot(t, uy2[0, :], linewidth=2)
# plt.plot(t, uy3[0, :], linewidth=2)
# plt.plot(t, uy4[0, :], linewidth=2)
# plt.plot(t, uy5[0, :], linewidth=2)
# plt.grid(True)
# plt.xlabel('Time(s)')
# plt.ylabel(' u_y')
# plt.legend(['u_y1', 'u_y2', 'u_y3', 'u_y4', 'u_y5'])

# # 图19：期望x:x_hat
# plt.figure(19)
# plt.plot(t, x_hat1[0, :], linewidth=2)
# plt.plot(t, x_hat2[0, :], linewidth=2)
# plt.plot(t, x_hat3[0, :], linewidth=2)
# plt.plot(t, x_hat4[0, :], linewidth=2)
# plt.plot(t, x_hat5[0, :], linewidth=2)
# plt.grid(True)
# plt.xlabel('Time(s)')
# plt.ylabel(' x_hat')
# plt.legend(['x_hat1', 'x_hat2', 'x_hat3', 'x_hat4', 'x_hat5'])

# # 图20：期望y:y_hat
# plt.figure(20)
# plt.plot(t, y_hat1[0, :], linewidth=2)
# plt.plot(t, y_hat2[0, :], linewidth=2)
# plt.plot(t, y_hat3[0, :], linewidth=2)
# plt.plot(t, y_hat4[0, :], linewidth=2)
# plt.plot(t, y_hat5[0, :], linewidth=2)
# plt.grid(True)
# plt.xlabel('Time(s)')
# plt.ylabel(' y_hat')
# plt.legend(['y_hat1', 'y_hat2', 'y_hat3', 'y_hat4', 'y_hat5'])

# # 图21：ex
# plt.figure(21)
# plt.plot(t[:-1], ex1[0, :], linewidth=2)
# plt.plot(t[:-1], ex1[1, :], linewidth=2)
# plt.plot(t[:-1], ex2[0, :], linewidth=2)
# plt.plot(t[:-1], ex2[1, :], linewidth=2)
# plt.plot(t[:-1], ex3[0, :], linewidth=2)
# plt.plot(t[:-1], ex3[1, :], linewidth=2)
# plt.plot(t[:-1], ex4[0, :], linewidth=2)
# plt.plot(t[:-1], ex4[1, :], linewidth=2)
# plt.plot(t[:-1], ex5[0, :], linewidth=2)
# plt.plot(t[:-1], ex5[1, :], linewidth=2)

# plt.grid(True)
# plt.xlabel('Time(s)')
# plt.ylabel(' ex1')
# plt.legend(['ex1_1', 'ex1_2', 'ex1_3', 'ex1_4', 'ex1_5', 'ex1_6', 'ex1_7', 'ex1_8', 'ex1_9', 'ex1_10'])

# # 图22：fx
# plt.figure(22)
# plt.plot(t[:-1], fx1[0, :], linewidth=2)
# plt.plot(t[:-1], fx1[1, :], linewidth=2)
# plt.plot(t[:-1], fx2[0, :], linewidth=2)
# plt.plot(t[:-1], fx2[1, :], linewidth=2)
# plt.plot(t[:-1], fx3[0, :], linewidth=2)
# plt.plot(t[:-1], fx3[1, :], linewidth=2)
# plt.plot(t[:-1], fx4[0, :], linewidth=2)
# plt.plot(t[:-1], fx4[1, :], linewidth=2)
# plt.plot(t[:-1], fx5[0, :], linewidth=2)
# plt.plot(t[:-1], fx5[1, :], linewidth=2)
# plt.grid(True)
# plt.xlabel('Time(s)')
# plt.ylabel(' fx')
# plt.legend(['fx_1', 'fx_2', 'fx_3', 'fx_4', 'fx_5', 'fx_6', 'fx_7', 'fx_8', 'fx_9', 'fx_10'])













plt.show()
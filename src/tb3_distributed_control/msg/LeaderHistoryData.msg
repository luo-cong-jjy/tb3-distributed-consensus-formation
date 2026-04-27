# ROS话题优化版本：领导者历史数据消息类型

# 时间戳信息
float64 trajectory_time    # 轨迹相对时间（从0开始）
float64 ros_timestamp     # ROS时间戳

# 位置和姿态数据  
float64 x0               # 领导者x坐标
float64 y0               # 领导者y坐标
float64 theta0           # 领导者航向角

# 速度数据
float64 v0               # 线速度
float64 w0               # 角速度
float64 u0x              # x方向速度分量
float64 u0y              # y方向速度分量
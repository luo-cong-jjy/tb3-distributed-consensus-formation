# ROS话题优化版本：机器人历史数据消息类型
# 设计目标：减少网络传输，提高实时性，降低roscore负载

# 机器人标识
int32 robot_id

# 时间戳信息
float64 trajectory_time    # 轨迹相对时间（从0开始）
float64 ros_timestamp     # ROS时间戳（用于数据时效性检查）

# 位置和姿态数据
float64 xc               # 当前x坐标
float64 yc               # 当前y坐标  
float64 thetac           # 当前航向角

# 控制输入数据
float64 vc               # 线速度
float64 wc               # 角速度

# 跟踪误差数据
float64 xe               # x方向误差
float64 ye               # y方向误差
float64 thetae           # 航向角误差

# 参考轨迹数据
float64 xr               # 参考x坐标
float64 yr               # 参考y坐标

# 观测器估计数据（对领导者位置的估计）
float64 zxeo_x           # 观测器估计的领导者X坐标
float64 zxeo_y           # 观测器估计的领导者Y坐标

# 避障相关数据（统一处理所有障碍物）
float64 raw_min_obstacle_distance   # 雷达原始数据的最小距离（直接从range获取）
float64 closest_obstacle_distance   # 最近障碍物点到参考点的距离（基于聚类分析）
int32 total_clusters_count          # 检测到的障碍物聚类总数
float64 avoidance_force_magnitude   # 避障力大小

# 性能分析数据
float64 computation_time  # 算法计算时间（秒）
float64 full_cycle_time  # 完整周期时间（秒）
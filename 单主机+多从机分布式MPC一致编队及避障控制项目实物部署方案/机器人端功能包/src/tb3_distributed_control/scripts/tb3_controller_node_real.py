#!/usr/bin/env python3
import rospy
import numpy as np
import math  # 添加数学计算支持
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64MultiArray, Bool
from sensor_msgs.msg import LaserScan  # 添加激光雷达数据支持
from tb3_distributed_control.msg import RobotHistoryData  # 导入自定义消息类型
import tf.transformations as tf

class TurtleBot3Controller:
    def __init__(self, robot_id):
        # 机器人配置（适配tb3_0~4）
        self.robot_id = robot_id  # 0-4
        self.ns = f"/tb3_{robot_id}"  # 命名空间：/tb3_0, /tb3_1, ..., /tb3_4
        
        # 控制参数（PDNN相关）
        self.N = 3
        self.Nu = 2
        self.gamma = 0.1
        self.t1 = 0.1  # 控制周期(s)
        self.Q = 1 *1e9 * np.eye(2*self.N)
        self.R = 1 *1e4 * np.eye(2*self.Nu)

        # 设置邻接矩阵
        # self.A = np.array([[0, 0, 1, 0, 0], # 机器人0的邻居：2
        #                    [1, 0, 1, 0, 0],  # 机器人1的邻居：0、2
        #                    [0, 0, 0, 1, 0],  # 机器人2的邻居：3
        #                    [1, 0, 0, 0, 0],  # 机器人3的邻居：0
        #                    [0, 1, 0, 0, 0]]) # 机器人4的邻居：1

        self.A = np.array([[0, 0, 0, 0, 0],
                           [1, 0, 0, 0, 0],
                           [0, 1, 0, 0, 0],
                           [0, 0, 1, 0, 0],
                           [0, 0, 0, 1, 0]])

        self.D = np.diag(np.sum(self.A, axis=1))
        self.L = self.D - self.A
        self.B = np.diag([1, 0, 0, 0, 0])
        self.F = self.L + self.B
        self.leader_direct = self.B[self.robot_id, self.robot_id]  # 用于判断是否直接连接领导者
        self.neighbor_ids = [i for i, val in enumerate(self.A[self.robot_id]) if val == 1] # 预计算邻居ID列表
        self.expected_neighbors = len(self.neighbor_ids) # 计算预期邻居数量
        self.indegree = self.F[self.robot_id, self.robot_id]
        self.Fx = self.indegree * np.eye(2)  # 自己的总入度
        # 编队队形参数
        self.Rnum = 5  # 编队机器人数量
        self.aa = 0
        self.bb = 1
        self.formation_radius = 0.4  # 编队半径参数

        # 实物修改点0
        #轨迹跟踪权重 - 定义两组参数
        
        # 【默认权重组】适用于直线段和其他轨迹
        self.em_default = 100
        self.Qx_default = 1000 * self.em_default
        self.Qy_default = 1000 * self.em_default
        self.Qtheta_default = 10 * self.em_default
        self.I0 = np.eye(1*self.N)
        self.Qxyt_default = np.array([[self.Qx_default, 0, 0],
                                      [0, self.Qy_default, 0],
                                      [0, 0, self.Qtheta_default]])
        self.Qz_default = np.kron(self.I0, self.Qxyt_default)
        self.Rz_default = 100 * np.eye(2*self.Nu)

        # 【S形半圆权重组】适用于半圆轨迹（原轨迹时间段：15-31s, 39-55s）
        self.em_circle = 100
        self.Qx_circle = 1000 * self.em_circle
        self.Qy_circle = 1000 * self.em_circle
        self.Qtheta_circle = 10 * self.em_circle
        self.Qxyt_circle = np.array([[self.Qx_circle, 0, 0],
                                     [0, self.Qy_circle, 0],
                                     [0, 0, self.Qtheta_circle]])
        self.Qz_circle = np.kron(self.I0, self.Qxyt_circle)
        self.Rz_circle = 100 * np.eye(2*self.Nu)
        
        # 初始化当前使用的权重（默认使用默认组）
        self.Qz = self.Qz_default
        self.Rz = self.Rz_default
        self.current_weight_mode = "default"  # 用于调试输出


        #自己调的，发现虽然震荡有所减小但是里程计却偏的很大
        # self.Qx = 2000
        # self.Qy = 2000
        # self.Qtheta = 300
        # self.I0 = np.eye(1*self.N)
        # self.Qxyt = np.array([[self.Qx, 0, 0],
        #                 [0, self.Qy, 0],
        #                 [0, 0, self.Qtheta]])
        # self.Qz = np.kron(self.I0, self.Qxyt)
        # self.Rz = 60 * np.eye(2*self.Nu)

        # 初始化轨迹规划输入
        self.ux = 0
        self.uy = 0
        self.u = np.zeros((2,1))

        # 初始化中间变量
        self.abaru = np.zeros((2*self.Nu, 1))
        self.detabarU = np.zeros((2*self.Nu, 1))
        self.abaruz = np.zeros((2*self.Nu, 1))
        self.detabarUz = np.zeros((2*self.Nu, 1))

        # 初始化PDNN状态变量
        self.y0x = np.zeros((2*self.Nu, 1))
        self.y0z = np.zeros((2*self.Nu, 1))

        # 参考位置初始化，实际的位置也放在同样的位置(仿真轨迹用)
        # 实物修改点1
        initial_positions = [           
            # 实物直线位置
            # 虚拟领导者位置(-0.15, 0.15 )
            # [ 0.20,  0.00],     # robot 0 (对应原代码 x_hat1, y_hat1)
            # [ -0.30,  0.50],     # robot 1 (对应原代码 x_hat2, y_hat2)
            # [ -0.50,  1.00],     # robot 2 (对应原代码 x_hat3, y_hat3)
            # [-0.50,  0.00],     # robot 3 (对应原代码 x_hat4, y_hat4)
            # [ 0.20, -0.30]      # robot 4 (对应原代码 x_hat5, y_hat5)

            # 虚拟领导者位置( -0.3, 0.0 )
            # [ 0.00, 0.40],     # robot 0 (对应原代码 x_hat1, y_hat1)
            # [-0.70, 0.20],     # robot 1 (对应原代码 x_hat2, y_hat2)
            # [-0.70,-0.20],     # robot 2 (对应原代码 x_hat3, y_hat3)
            # [ 0.00,-0.40],     # robot 3 (对应原代码 x_hat4, y_hat4)
            # [ 0.20, 0.10]      # robot 4 (对应原代码 x_hat5, y_hat5)


            # 实物S形位置
            # 虚拟领导者位置( 0.0, 0.0 )
            [ 0.15, 0.40],     # robot 0 (对应原代码 x_hat1, y_hat1)
            [-0.40, 0.30],     # robot 1 (对应原代码 x_hat2, y_hat2)
            [-0.40,-0.20],     # robot 2 (对应原代码 x_hat3, y_hat3)
            [ 0.20,-0.30],     # robot 3 (对应原代码 x_hat4, y_hat4)
            [ 0.40,-0.10]      # robot 4 (对应原代码 x_hat5, y_hat5)
        ]

        self.x_hat = initial_positions[self.robot_id][0]  
        self.y_hat = initial_positions[self.robot_id][1]  
        self.theta_hat = 0  # 规划的航向角
        
        # 初始化参考轨迹x和y方向坐标，用于保存理想轨迹，计算跟踪误差，感觉也有点多余
        self.xr = self.x_hat
        self.yr = self.y_hat
        self.thetar = self.theta_hat

        # 实物取消注释点①
        #机器人局部坐标系与全局坐标系的偏差（用于实物机器人的里程计回调数据处理）
        self.detar_x     = initial_positions[self.robot_id][0]
        self.detar_y     = initial_positions[self.robot_id][1]

        # 初始化当前位置(需要从里程计/导航栈获取)
        self.xc = 0
        self.yc = 0
        self.thetac = 0  # 真实航向角
        
        # 调试：PDNN算法执行时间统计
        self.pdnn_execution_times = []
        self.pdnn_call_count = 0
        self.node_start_time = rospy.get_time()

        # 初始化误差
        self.xe = 0
        self.ye = 0
        self.thetae = 0  # 航向角误差
        
        # 初始化速度相关
        self.vr = 0
        self.vc = 0
        self.wr = 0
        self.wc = 0
        
        #初始化轨迹跟踪控制输入
        self.uz = np.zeros((2,1))
        
        # 初始化误差矩阵
        self.ex = np.zeros((2, 1))
        self.fx = np.zeros((2, 1))
        self.zx = np.zeros((2, 1))

        # 初始化中间变量
        self.L1 = 0
        self.L2 = 0
        self.L3 = 0
        self.M0 = 0

        # 控制输入约束
        self.abarUmin1 = -5 * np.ones((2*self.Nu, 1))
        self.abarUmax1 = 5 * np.ones((2*self.Nu, 1))
        self.detabarUmin = -5 * np.ones((2*self.Nu, 1))
        self.detabarUmax = 5 * np.ones((2*self.Nu, 1))
        self.abarUminz = -0.5 * np.ones((2*self.Nu, 1))
        self.abarUmaxz = 0.5 * np.ones((2*self.Nu, 1))
        self.detabarUminz = -0.5 * np.ones((2*self.Nu, 1))
        self.detabarUmaxz = 0.5 * np.ones((2*self.Nu, 1))

        # 位置约束
        self.xmin = -5
        self.xmax = 5

        self.abarxmin = self.xmin * np.ones((2*self.N, 1))
        self.abarxmax = self.xmax * np.ones((2*self.N, 1))
        self.abarxminz = self.xmin * np.ones((3*self.N, 1))
        self.abarxmaxz = self.xmax * np.ones((3*self.N, 1))

        # 初始化位置偏移
        self.px = 0
        self.py = 0

        # 初始化预测模型状态矩阵 fxz
        self.fxz = np.zeros((3, 1))

        self.gx = self.t1 * self.Fx @ np.eye(2)

        # 获取矩阵gx的行数和列数
        self.n_gx_x, self.m_gx_u = self.gx.shape
        self.z = np.zeros((self.n_gx_x, self.m_gx_u))
        self.gxxz = np.zeros((3, 2))

        # 定义pdnn步长和迭代次数
        self.h = self.t1/10
        self.n = 10

        # 初始化时钟和时间参数
        self.leader_time = 0.0  # 领导者时间（从领导者消息获取）
        self.local_time = 0.0   # 统一本地时钟：同步前=仿真时间，同步后=领导者时间
        self.simulation_start_time = None  # 仿真开始的ROS时间基准
        self.is_clock_synced = False  # 是否已与领导者时钟同步
        self.first_leader_msg_time = None  # 第一次接收领导者消息的时间戳（用于分析）
        
        # 领导者状态初始化
        self.leader_state = {
            "t": 0.0, "x0": 0.0, "y0": 0.0, "u0": np.zeros(2), "theta0": 0.0,
        }
        self.received_leader_states = {}  # 存储接收到的领导者状态，key为时间步
        
        # 【新增】节点关闭标志，防止关闭过程中继续执行控制
        self.is_shutting_down = False
                
        # 🚀 观测器相关参数初始化
        # 实物修改点2
        # 观测器参数设置，8字形&直线0.6，0.8，S形0.7，0.8
        self.ob_eta = 0.7  # 观测器增益参数1
        self.ob_alp = 0.8  # 观测器增益参数2

        # 🚀 观测器状态变量初始化
        self.zxeo = np.zeros((2, 1))  # 当前机器人对领导者状态的观测估计
        self.dzxeo = np.zeros((2, 1))  # 观测状态导数

        # 🚀 避障相关参数初始化（统一处理所有障碍物）
        # 实物修改点3（需要根据实验效果进行调整）
        self.ord_avoid = 0.30   # 避障力计算距离参数
        self.ord_safe  = 0.25     # 安全距离阈值
        
        #  激光雷达配置（从 launch 参数读取）
        self.lidar_type = rospy.get_param('~lidar_type', 'LDS-02')  # 默认LDS-02(实物)，可选LDS-01(仿真)
        
        # 雷达规格配置（支持LDS-01和LDS-02）
        self.lidar_specs = {
            "LDS-01": {
                "min_range": 0.12,    # 最小检测距离 (m)
                "max_range": 3.5,     # 最大检测距离 (m)
                "resolution": 1.0,    # 角度分辨率 (度)
            },
            "LDS-02": {
                "min_range": 0.16,    # 最小检测距离 (m)
                "max_range": 8.0,     # 最大检测距离 (m) 
                "resolution": 1.0,    # 角度分辨率 (度)
            }
        }
        
        # 初始化默认参数
        self.distance_jump_threshold = 0.068  # 距离跳跃阈值（与测试脚本一致：6.8cm）
        self.min_detection_range = 0.16  # 最小检测距离（优化后：减少近距离噪声）
        self.max_detection_range = 3.0  # 最大检测距离（人为设置，用于限制检测范围,减小计算）
    
        # 聚类结果存储
        self.filtered_clusters = []  # 所有障碍物聚类结果（不再区分类型）
        self.scan_count = 0  # 激光扫描计数
        
        # 分离的避障力向量（更清晰的设计）
        self.pxy_avoid = np.zeros(2)  # 障碍物避障力向量 [px_offset, py_offset]
        
        # ==================== 📦 异步缓存数据结构 ====================
        # 里程计缓存（异步更新，控制循环快照）
        self.odom_cache = {
            'xc': 0.0,
            'yc': 0.0,
            'thetac': 0.0,
            'timestamp': 0.0
        }
        
        # 激光雷达缓存（异步更新，控制循环快照）
        self.laser_cache = {
            'data': None,  # LaserScan消息
            'timestamp': 0.0
        }
        
        # 邻居观测器缓存（异步更新，控制循环快照）
        self.neighbor_observer_cache = {i: {
            'zxeo': np.zeros(2),
            'dzxeo': np.zeros(2),
            'timestamp': 0.0
        } for i in range(5)}
        
        # ==================== 📸 控制循环快照数据 ====================
        # 控制循环开始时统一快照，保证计算一致性
        self.snapshot = {
            'odom': {'xc': 0.0, 'yc': 0.0, 'thetac': 0.0},
            'laser': None,  # LaserScan数据
            'neighbors': {},  # 邻居观测器状态
            'timestamp': 0.0  # 快照时间戳
        }

        # 调试相关变量
        self.debug_counter = 0  # 用于控制调试输出频率（只在控制循环中递增）
        self.debug_interval = 10  # 每10个控制周期输出一次详细调试信息
       
        # 注册节点关闭回调（确保最终状态记录）
        rospy.on_shutdown(self.save_final_history)

        # ROS通信（适配命名空间）
        rospy.Subscriber(f"{self.ns}/odom", Odometry, self.odom_callback)  # 订阅自身里程计
        rospy.Subscriber(f"{self.ns}/scan", LaserScan, self.laser_callback)  # 订阅激光雷达数据
        
        # 🚀 订阅所有机器人的观测器状态
        # 📝 设计说明：虽然实际计算时只用到邻居的数据（根据邻接矩阵self.neighbor_ids）
        #             但为了简化代码结构和避免拓扑变化时的重新订阅，统一订阅所有机器人
        #             在compute_consensus_error()中通过neighbor_ids过滤使用
        for robot_id in range(5):
            rospy.Subscriber(f"/tb3_{robot_id}/observer_state", Float64MultiArray,
                        self.all_robot_observer_callback, callback_args=robot_id)

        # 获取虚拟领导者命名空间并订阅其状态
        virtual_leader_ns = rospy.get_param("/virtual_leader_ns", "tb3_virtual_leader")
        rospy.Subscriber(f"/{virtual_leader_ns}/state", Float64MultiArray, self.leader_callback)  # 订阅领导者状态
        rospy.loginfo(f"Robot {self.robot_id} 订阅虚拟领导者状态话题: /{virtual_leader_ns}/state")
        
        rospy.Subscriber("/system/shutdown", Bool, self.shutdown_callback)  # 订阅系统停止信号
        self.cmd_vel_pub = rospy.Publisher(f"{self.ns}/cmd_vel", Twist, queue_size=1)  # 🚀 优化: 速度指令实时性
        self.observer_state_pub = rospy.Publisher(f"{self.ns}/observer_state", Float64MultiArray, queue_size=1) # 🚀 优化: 观测器状态实时性

        # 🚀 ROS话题优化：发布历史数据到专用话题（替代参数服务器）
        self.robot_history_pub = rospy.Publisher(f"/tb3_{self.robot_id}/history", RobotHistoryData, queue_size=1)  # 🚀 优化: 数据新鲜度
        
        # rospy.loginfo(f"tb3_{self.robot_id} 仿真机器人节点基础初始化完成")
        rospy.loginfo(f"tb3_{self.robot_id} 真实机器人节点基础初始化完成")
        
        # 实物修改点4
        # ✅ 完全实物部署：统一同步等待机制
        # 🔄 等待所有机器人 + 领导者全部上线
        # 这确保所有机器人（tb3_0~tb3_4）在相同条件下启动
        if not self.wait_for_all_robots():
            rospy.logerr(f"tb3_{self.robot_id} 同步等待失败（邻居或领导者未就绪），节点退出")
            return

        # 【重要改进】立即启动独立定时器
        # 定时器内部会等待首次领导者消息，收到后立即在当前周期执行控制
        self.control_timer = rospy.Timer(rospy.Duration(self.t1), self.control_loop)
        
        rospy.loginfo(f"🎯 tb3_{self.robot_id} 控制定时器已启动，周期={self.t1}s，等待领导者消息...")
        
        # 应用LiDAR配置
        self.apply_lidar_config(self.lidar_type)
        
        # 📊 新增数据记录：避障与聚类分析
        self.raw_min_distance_history = []          # 记录雷达原始最小距离
        self.obstacle_distance_history = []         # 记录最近障碍物点到参考点的距离
        self.clustering_analysis_history = []       # 记录每个时间步的聚类分析结果
        
        # ⏱️ 时间统计列表（用于程序结束时计算平均时间）
        self.clustering_avoidance_times = []  # 聚类与避障计算时间列表
        self.algorithm_times = []             # 控制算法计算时间列表
        self.last_full_cycle_duration = 0.001  # 初始化为1ms，避免使用t1作为默认值
        
        rospy.loginfo(f"🚀 tb3_{self.robot_id} 初始化完成，LiDAR类型: {self.lidar_type}")
        rospy.loginfo(f"tb3_{self.robot_id} 节点初始化完成，等待虚拟领导者，准备分布式一致编队控制")

    def check_robot_online(self, robot_id, timeout=0.5):
        """检查单个机器人是否在线（检测里程计话题，避免循环依赖）
        
        ⚠️ 关键设计：不能检测observer_state话题，因为：
            - observer_state在control_loop中发布
            - control_loop在wait_for_all_robots()返回后才启动
            - 会造成循环依赖死锁！
        
        ✅ 正确方案：检测机器人底盘的odom话题（TurtleBot3启动后立即发布）
        
        Args:
            robot_id: 机器人ID字符串，如'tb3_0'
            timeout: 等待超时时间（秒）
            
        Returns:
            bool: 机器人是否在线
        """
        # 检测里程计话题（机器人底盘启动后立即发布，无循环依赖）
        odom_topic = f"/{robot_id}/odom"
        try:
            rospy.wait_for_message(odom_topic, Odometry, timeout=timeout)
            return True
        except rospy.ROSException:
            return False
    
    def check_leader_online(self, timeout=0.5):
        """检查虚拟领导者是否在线
        
        Args:
            timeout: 等待超时时间（秒）
            
        Returns:
            bool: 领导者是否在线
        """
        leader_topic = "/tb3_virtual_leader/state"
        try:
            rospy.wait_for_message(leader_topic, Float64MultiArray, timeout=timeout)
            return True
        except rospy.ROSException:
            return False
    
    def wait_for_first_leader_message(self, timeout=30.0):
        """
        等待首次接收到领导者消息
        
        这是确保所有机器人同步启动的关键步骤。
        所有机器人（无论有无邻居）都必须等到接收到领导者消息后，
        才能开始控制循环，避免因邻居检测时间差异导致的启动不同步。
        
        参数：
            timeout - 等待超时时间（秒）
        
        返回值：
            True  - 成功接收到领导者消息
            False - 超时失败
        """
        rospy.loginfo(f"⏳ tb3_{self.robot_id} 等待首次接收领导者消息...")
        
        start_time = rospy.get_time()
        rate = rospy.Rate(100)  # 100Hz高频检查，快速响应领导者消息
        
        while not rospy.is_shutdown():
            # 检查是否已接收到领导者消息
            if self.is_clock_synced:
                rospy.loginfo(f"✅ tb3_{self.robot_id} 已接收到领导者消息（延迟={(rospy.get_time()-self.first_leader_msg_time)*1000:.1f}ms），准备开始控制")
                return True
            
            # 检查超时
            elapsed = rospy.get_time() - start_time
            if elapsed > timeout:
                rospy.logerr(f"❌ tb3_{self.robot_id} 等待领导者消息超时 ({timeout}s)")
                return False
            
            # 定期提示
            if int(elapsed) % 5 == 0 and elapsed > 0:
                rospy.loginfo(f"⏳ tb3_{self.robot_id} 仍在等待领导者消息... ({elapsed:.0f}s/{timeout}s)")
            
            rate.sleep()
        
        return False
    
    def wait_for_all_robots(self):
        """等待邻居机器人上线（第一阶段同步）
        
        完全实物部署架构：
        - 5个真实TurtleBot3机器人（tb3_0 ~ tb3_4）
        - 1个虚拟领导者节点（运行在中心PC上）
        - 基于邻接矩阵的分布式通信拓扑
        
        🔄 三种融合策略：
        【策略1-理想】所有机器人+领导者都在线 → 立即启动
        【策略2-关键】所有邻居在线+领导者在线(如需) → 满足最小分布式要求
        【策略3-降级】超过5分钟+一半邻居在线 → 容错启动(避免个别故障阻塞)
        """
        expected_robots = ['tb3_0', 'tb3_1', 'tb3_2', 'tb3_3', 'tb3_4']
        rospy.loginfo("=== 🔄 分布式控制同步等待机制 (完全实物部署) ===")
        rospy.loginfo(f"当前机器人: tb3_{self.robot_id}")
        rospy.loginfo(f"邻居机器人ID: {self.neighbor_ids}")
        rospy.loginfo(f"是否直接连接领导者: {'是' if self.leader_direct else '否'}")
        
        # 🔍 先检查自己的里程计话题是否正常（验证ROS环境）
        rospy.loginfo("🔍 检查自身里程计话题...")
        try:
            rospy.wait_for_message(f"{self.ns}/odom", Odometry, timeout=5.0)
            rospy.loginfo(f"✅ 自身里程计话题正常: {self.ns}/odom")
        except rospy.ROSException:
            rospy.logerr(f"❌ 无法接收自身里程计数据！请检查TurtleBot3底盘是否已启动")
            rospy.logerr(f"   启动命令: ROS_NAMESPACE=tb3_{self.robot_id} roslaunch turtlebot3_bringup turtlebot3_robot.launch multi_robot_name:=tb3_{self.robot_id}")
            return False
        
        rospy.sleep(0.5)  # 缩短网络稳定等待时间，加快启动
        
        timeout_count = 0
        max_timeout = 300  # 最大等待600秒（10分钟）
        
        while not rospy.is_shutdown() and timeout_count < max_timeout:
            # 1. 检查所有机器人在线状态
            active_robots = []
            for robot_id in expected_robots:
                if self.check_robot_online(robot_id, timeout=0.5):
                    active_robots.append(robot_id)
            
            other_robots = [r for r in active_robots if r != f"tb3_{self.robot_id}"]
            
            # 2. 判断是否可以启动：所有机器人都在线即可
            can_start = False
            reason = ""
            
            # 策略1：理想情况 - 所有机器人都在线
            if len(active_robots) == len(expected_robots):
                can_start = True
                reason = "所有机器人已就绪"
            
            # 策略2：降级启动 - 至少一半机器人在线
            elif timeout_count > 150 and len(active_robots) >= len(expected_robots) // 2 + 1:
                can_start = True
                reason = f"降级启动：{len(active_robots)}/{len(expected_robots)}机器人在线"
            
            if can_start:
                rospy.loginfo(f"🎉 {reason}，启动控制定时器")
                rospy.loginfo(f"✅ 在线机器人: {active_robots}")
                return True
            
            # 3. 每5次循环输出一次状态（减少日志频率）
            if timeout_count % 5 == 0:
                rospy.loginfo(f"📊 在线机器人: {len(active_robots)}/{len(expected_robots)} {other_robots}")
                rospy.loginfo(f"🔍 检测方法: 里程计话题 (/<robot_id>/odom)")
                
                missing_robots = [r for r in expected_robots if r not in active_robots]
                if missing_robots:
                    rospy.loginfo(f"⏳ 等待机器人: {missing_robots}")
            
            # 4. 超时检查
            timeout_count += 1
            if timeout_count >= max_timeout:
                rospy.logerr("❌ 等待超时！请检查：")
                rospy.logerr(f"   1. 其他机器人是否已启动？当前在线: {other_robots}")
                rospy.logerr(f"   2. ROS网络是否配置正确？(ROS_MASTER_URI)")
                return False
            
            rospy.sleep(2.0)
        
        return False

    #其他实用函数
    def odom_callback(self, msg):
        """📦 异步更新里程计缓存（不进行任何计算）"""
        if self.is_shutting_down:
            return
        
        # 提取位姿数据并更新缓存
        q = [msg.pose.pose.orientation.x, msg.pose.pose.orientation.y,
             msg.pose.pose.orientation.z, msg.pose.pose.orientation.w]
        
        # self.odom_cache['xc'] = msg.pose.pose.position.x
        # self.odom_cache['yc'] = msg.pose.pose.position.y
        # 实物修改点5
        self.odom_cache['xc'] = msg.pose.pose.position.x + self.detar_x
        self.odom_cache['yc'] = msg.pose.pose.position.y + self.detar_y
        self.odom_cache['thetac'] = tf.euler_from_quaternion(q)[2]
        self.odom_cache['timestamp'] = rospy.get_time()
        
        rospy.logdebug(f"📦 tb3_{self.robot_id} 里程计缓存更新: x={self.odom_cache['xc']:.3f}, y={self.odom_cache['yc']:.3f}, theta={self.odom_cache['thetac']:.3f}")

    def laser_callback(self, msg):
        """📦 异步更新激光雷达缓存（不进行聚类分析）"""
        if self.is_shutting_down:
            return
        
        # 更新激光雷达缓存
        self.laser_cache['data'] = msg
        self.laser_cache['timestamp'] = rospy.get_time()
        
        rospy.logdebug(f"📦 tb3_{self.robot_id} 激光雷达缓存更新: 数据点数={len(msg.ranges)}")

    def apply_lidar_config(self, lidar_type):
        """应用指定雷达类型的配置"""
        if lidar_type in self.lidar_specs:
            self.lidar_type = lidar_type
            current_spec = self.lidar_specs[lidar_type]
            
            rospy.loginfo(f"🎯 tb3_{self.robot_id} 应用{lidar_type}配置: "
                         f"雷达范围={current_spec['min_range']}-{current_spec['max_range']}m, "
                         f"检测范围={self.min_detection_range}-{self.max_detection_range}m")
            
        else:
            rospy.logwarn(f"tb3_{self.robot_id} 未知雷达类型: {lidar_type}")



    def perform_laser_clustering_analysis(self, laser_data=None):
        """
        执行激光雷达聚类分析（使用快照数据）
        Args:
            laser_data: LaserScan消息，如果为None则跳过分析
        """
        if laser_data is None:
            return
            
        self.scan_count += 1
        
        # 记录雷达原始最小距离（在任何过滤之前）
        ranges = np.array(laser_data.ranges)
        valid_raw_ranges = ranges[(~np.isnan(ranges)) & (~np.isinf(ranges)) & (ranges > 0)]
        if len(valid_raw_ranges) > 0:
            raw_min_range = float(np.min(valid_raw_ranges))
            self.raw_min_distance_history.append({
                'timestamp': self.leader_time,
                'min_distance': raw_min_range
            })
        else:
            self.raw_min_distance_history.append({
                'timestamp': self.leader_time,
                'min_distance': float('inf')
            })
        
        # 基于雷达数据连续性进行分区（不考虑距离跳跃）
        clusters = self.cluster_by_continuity(laser_data)
        
        if len(clusters) == 0:
            return  # 静默处理无有效分区
        
        # 检查首尾连接（处理360°跨越问题）
        clusters = self.merge_wraparound_clusters(clusters, laser_data)
        
        # 实物修改点6
        # 过滤单点噪声（至少1点才算有效分区！！！）
        filtered_clusters = [cluster for cluster in clusters if len(cluster) >= 1]
        
        # 如果没有有效分区，静默返回
        if len(filtered_clusters) == 0:
            return
        
        # 计算每个分区的长度并分类
        self.analyze_clusters(filtered_clusters)
        
        # 调试信息：输出前3次聚类结果（已注释以提升性能）
        # if self.debug_counter < 3:
        #     clusters = len(getattr(self, 'filtered_clusters', []))
        #     rospy.loginfo(f"[时间步{self.debug_counter-1}] [tb3_{self.robot_id}] 聚类检测: 总聚类{clusters}个")

    def extract_valid_points(self, msg):
        """
        提取有效的激光点（NumPy优化版，返回结构化数组）
        
        Returns:
            np.ndarray: 结构化数组，包含 'index', 'angle', 'range', 'x', 'y' 字段
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
            ~np.isnan(ranges) &
            ~np.isinf(ranges) &
            (ranges != 0.0) &
            (ranges >= min_range) &
            (ranges <= max_range)
        )
        
        # 提取有效数据
        valid_indices = indices[valid_mask]
        valid_angles = angles[valid_mask]
        valid_ranges = ranges[valid_mask]
        
        # 向量化计算笛卡尔坐标
        x = valid_ranges * np.cos(valid_angles)
        y = valid_ranges * np.sin(valid_angles)
        
        # 返回结构化数组（更高效）
        valid_points = np.empty(len(valid_indices), dtype=[
            ('index', 'i4'),
            ('angle', 'f8'),
            ('range', 'f8'),
            ('x', 'f8'),
            ('y', 'f8')
        ])
        valid_points['index'] = valid_indices
        valid_points['angle'] = valid_angles
        valid_points['range'] = valid_ranges
        valid_points['x'] = x
        valid_points['y'] = y
        
        return valid_points

    def cluster_by_continuity(self, laser_data):
        """
        基于雷达数据连续性进行分区（NumPy优化版）
        
        分区条件：
        1. 索引不连续（有无效点）
        2. 🔥 距离跳变（相邻点距离差 > 阈值）
        
        Args:
            laser_data: LaserScan消息
            
        Returns:
            List[np.ndarray]: 分区后的点集列表，每个点包含 'index', 'angle', 'range', 'x', 'y' 字段
        """
        # 1. 提取所有有效点（已包含笛卡尔坐标）
        valid_points = self.extract_valid_points(laser_data)
        
        if len(valid_points) == 0:
            return []
        
        # 2. 找到索引断点（不连续的位置）
        indices = valid_points['index']
        index_breaks = np.where(np.diff(indices) != 1)[0] + 1
        
        # 3. 🔥 找到距离跳变点（相邻点距离差过大）
        ranges = valid_points['range']
        range_diffs = np.abs(np.diff(ranges))
        distance_breaks = np.where(range_diffs > self.distance_jump_threshold)[0] + 1
        
        # 4. 合并两种断点
        all_breaks = np.unique(np.concatenate([index_breaks, distance_breaks]))
        
        # 5. 使用np.split快速分割
        clusters = np.split(valid_points, all_breaks)
        
        return clusters

    def merge_wraparound_clusters(self, clusters, laser_data):
        """
        处理360°跨越问题：检查第一个和最后一个分区是否应该合并
        
        原理：如果雷达在0°和359°附近都检测到障碍物，可能是同一个障碍物被分成两段
        
        Args:
            clusters: 原始分区列表
            laser_data: LaserScan消息
            
        Returns:
            List[List[dict]]: 合并后的分区列表
        """
        if len(clusters) < 2:
            return clusters
        
        first_cluster = clusters[0]
        last_cluster = clusters[-1]
        
        if len(first_cluster) == 0 or len(last_cluster) == 0:
            return clusters
        
        # 获取首尾分区的边界点
        first_point = first_cluster[0]  # 第一个分区的第一个点
        last_point = last_cluster[-1]   # 最后一个分区的最后一个点
        
        # 检查是否跨越360°边界
        first_angle = first_point['angle']
        last_angle = last_point['angle']
        
        # 第一个点应该在0°附近，最后一个点应该在360°附近
        first_near_zero = first_angle >= -0.2 and first_angle <= 0.5  # ±11°范围
        last_near_360 = last_angle >= 5.8 and last_angle <= 6.5      # 约332°-372°
        
        if not (first_near_zero and last_near_360):
            return clusters  # 不是360°跨越
        
        # 向量化计算空间距离
        dx = first_point['x'] - last_point['x']
        dy = first_point['y'] - last_point['y']
        spatial_distance = np.sqrt(dx**2 + dy**2)
        
        # 合并条件：空间距离足够小（说明是连续的同一障碍物）
        merge_threshold = 0.15  # 15cm空间距离阈值
        
        if spatial_distance < merge_threshold:
            # 使用np.concatenate快速合并
            merged_cluster = np.concatenate([last_cluster, first_cluster])
            # 返回合并后的分区列表：合并分区 + 中间分区（排除首尾）
            return [merged_cluster] + clusters[1:-1]
        
        return clusters

    def analyze_clusters(self, clusters):
        """
        分析每个分区的长度并筛选出最近的障碍点
        
        流程：
        1. 计算每个分区的长度
        2. 过滤掉长度过小的分区（噪声）
        3. 筛选每个分区中最近的点（用于避障计算）
        
        Args:
            clusters: 分区后的点集列表
        """
        # 计算所有分区的长度
        cluster_lengths = self.calculate_all_cluster_lengths(clusters)
        
        # 实物修改点7
        # 设置长度过滤阈值（过滤过小的分区）避障重要参数2
        min_cluster_length = 0.001  # 0.1cm，小于此长度的分区视为噪声即无效分区
        
        # 第一步过滤：长度过滤
        valid_clusters = []
        for cluster_id, cluster in enumerate(clusters):
            length = cluster_lengths[cluster_id]
            if length >= min_cluster_length:
                valid_clusters.append((cluster_id, cluster, length))
        
        # 第二步筛选：为每个有效分区筛选最近的点
        filtered_clusters = []
        for cluster_id, cluster, length in valid_clusters:
            filtered_cluster = self.filter_closest_points_in_cluster(cluster, max_points=20)
            filtered_clusters.append((cluster_id, filtered_cluster, length))
        
        # 存储结果
        self.filtered_clusters = filtered_clusters  # [(cluster_id, filtered_points_list, length), ...]
        
        # 调试信息
        if self.scan_count == 1:
            rospy.loginfo(f"🎯 [时间步{self.scan_count}] [tb3_{self.robot_id}]: "
                         f"障碍物检测 - 原始分区:{len(clusters)}, "
                         f"长度过滤后:{len(valid_clusters)}, "
                         f"最终有效:{len(filtered_clusters)}")
        
    def calculate_all_cluster_lengths(self, clusters):
        """
        批量计算所有分区的长度（NumPy优化版）
        
        Args:
            clusters: 分区列表
            
        Returns:
            np.ndarray: 每个分区的长度
        """
        if not clusters:
            return np.array([])
        
        lengths = np.zeros(len(clusters))
        
        for i, cluster in enumerate(clusters):
            if len(cluster) < 2:
                continue
            
            r1 = cluster[0]['range']
            r2 = cluster[-1]['range']
            angle1 = cluster[0]['angle']
            angle2 = cluster[-1]['angle']
            
            # 处理角度跨越
            angle_diff = angle2 - angle1
            if angle_diff < 0:
                angle_diff += 2 * np.pi
            
            # 余弦定理计算长度
            length_squared = r1**2 + r2**2 - 2*r1*r2*np.cos(angle_diff)
            lengths[i] = np.sqrt(max(length_squared, 0))
        
        return lengths

    def filter_closest_points_in_cluster(self, cluster, max_points=20):
        """
        筛选分区中的有效点（NumPy优化版）
        
        策略：
        1. 小分区(<20点): 不筛选，使用全部点以保证避障效果
        2. 大分区(≥20点): 按雷达距离筛选最近20个点，平衡效果与性能
        
        🔥 当前策略：保留所有分区点，不进行点数筛选
        
        Args:
            cluster: 分区点集（NumPy结构化数组）
            max_points: 最大保留点数，默认20个（当前未使用）
            
        Returns:
            np.ndarray: 筛选后的点集
        """
        # 🔥 注释掉原有的点数筛选逻辑，直接返回所有点（按角度排序保持扫描顺序）
        angle_sort_indices = np.argsort(cluster['angle'])
        return cluster[angle_sort_indices]
        
        # # 原有筛选逻辑（已注释）
        # if len(cluster) <= max_points:
        #     # 小分区：按雷达距离排序
        #     sort_indices = np.argsort(cluster['range'])
        #     return cluster[sort_indices]
        # 
        # # 大分区：按雷达距离排序，选择最近的max_points个点
        # sort_indices = np.argsort(cluster['range'])
        # closest_indices = sort_indices[:max_points]
        # 
        # # 按角度重新排序（保持扫描顺序）
        # closest_points = cluster[closest_indices]
        # angle_sort_indices = np.argsort(closest_points['angle'])
        # 
        # return closest_points[angle_sort_indices]

    def calculate_cluster_based_avoidance_force(self):
        """
        基于聚类分析计算避障力 - 核心避障算法
        
        算法流程：
        1. 对每个聚类的当前位置最近n个点（根据雷达点云距离参数筛选）转换到全局坐标
        2. 计算每个点与下一步参考轨迹点的距离
        3. 找到每个聚类中距离参考轨迹最近的点
        4. 判断是否小于安全阈值
        5. 计算避障力并叠加
        """
        # 初始化避障力
        self.pxy_avoid.fill(0.0)
        
        if not hasattr(self, 'filtered_clusters'):
            return
        
        total_avoidance_force = np.zeros(2)
        global_min_distance = float('inf')  # 记录所有聚类中的全局最小距离
        
        # 统一处理所有聚类
        for cluster_id, cluster_points, cluster_length in self.filtered_clusters:
            cluster_force, cluster_min_dist = self.calculate_cluster_avoidance_force(
                cluster_points, 
                self.ord_safe,  # 使用统一的安全距离
                self.ord_avoid,  # 使用统一的避障距离
                cluster_length   # 传递聚类长度
            )
            total_avoidance_force += cluster_force
            # 更新全局最小距离
            if cluster_min_dist < global_min_distance:
                global_min_distance = cluster_min_dist
            
        # 更新避障力
        self.pxy_avoid = total_avoidance_force
        
        # 📊 记录最近障碍物点距离（用于图表）
        if global_min_distance != float('inf'):
            self.obstacle_distance_history.append({
                'timestamp': self.leader_time,
                'min_distance': global_min_distance
            })
        else:
            # 无障碍物情况：记录人为设定的最大检测距离
            self.obstacle_distance_history.append({
                'timestamp': self.leader_time,
                'min_distance': self.max_detection_range
            })
        
        # 📊 记录聚类结果
        cluster_count = len(self.filtered_clusters)
        
        self.clustering_analysis_history.append({
            'timestamp': self.leader_time,
            'total_clusters_count': cluster_count,
            'avoidance_force_magnitude': np.linalg.norm(self.pxy_avoid)
        })
        
        # 调试信息（前3次）
        if self.scan_count <= 3:
            force_magnitude = np.linalg.norm(self.pxy_avoid)
            rospy.loginfo(f"🎯 [时间步{self.scan_count}] [tb3_{self.robot_id}]: 聚类避障 - 总聚类:{cluster_count}, 避障力:{force_magnitude:.4f}")

    def calculate_cluster_avoidance_force(self, cluster_points, safe_distance, avoid_distance, cluster_length=0.0):
        """
        计算单个聚类的避障力
        
        Args:
            cluster_points: 聚类中的点集
            safe_distance: 安全距离阈值
            avoid_distance: 避障计算距离参数
            cluster_length: 聚类的实际长度（单位：米，用于调整避障力系数）
            
        Returns:
            tuple: (避障力向量 [fx, fy], 该聚类到参考点的最小距离)
        """
        if len(cluster_points) == 0:
            return np.zeros(2), float('inf')
        
        # 获取聚类点数（用于避障力增强判断）
        cluster_point_count = len(cluster_points)
        
        # 将聚类点转换为全局坐标
        cluster_global_coords = []
        cos_theta = np.cos(self.thetac)
        sin_theta = np.sin(self.thetac)
        
        for point in cluster_points:
            # 极坐标转本地直角坐标
            local_x = point['range'] * math.cos(point['angle'])
            local_y = point['range'] * math.sin(point['angle'])
            
            # 本地坐标转全局坐标
            global_x = self.xc + (cos_theta * local_x - sin_theta * local_y)
            global_y = self.yc + (sin_theta * local_x + cos_theta * local_y)
            
            cluster_global_coords.append({'x': global_x, 'y': global_y})
        
        # 计算每个点与下一步参考轨迹的距离
        min_distance = float('inf')
        closest_point = None
        
        for coord in cluster_global_coords:
            # 计算与下一步参考轨迹点的距离
            dx = coord['x'] - self.xr
            dy = coord['y'] - self.yr
            distance = math.sqrt(dx**2 + dy**2)
            
            if distance < min_distance:
                min_distance = distance
                closest_point = coord
        
        # 检查是否需要避障
        if min_distance <= safe_distance and closest_point is not None:
            # 计算避障力大小（参考纯仿真代码公式）
            force_magnitude = (avoid_distance / min_distance) * (avoid_distance - min_distance)
            
            # 实物修改点8，根据实验效果调整
            # 🔥 避障力调整：点数<10时减弱避障力，用于规避其他机器人形成的动态障碍物
            if cluster_point_count < 10:
                reduction_factor = 0.2  # 衰减系数（可根据实际调整，小于1）
                force_magnitude *= reduction_factor
            
            # if cluster_point_count > 40:
            #     reduction_factor = 0.0  # 衰减系数（临时避免墙的干扰，可根据实际调整，小于1）
            #     force_magnitude *= reduction_factor

            # 计算避障力方向（从障碍物指向机器人）
            angle_o2r = math.atan2(
                closest_point['y'] - self.yr,  # 障碍物y - 参考轨迹y
                closest_point['x'] - self.xr   # 障碍物x - 参考轨迹x
            )
            
            # 计算避障力分量
            force_x = force_magnitude * math.cos(angle_o2r)
            force_y = force_magnitude * math.sin(angle_o2r)
            
            return np.array([force_x, force_y]), min_distance
            
        return np.zeros(2), min_distance

    def calculate_obstacles_single_closest_force(self, laser_data):
        """
        计算障碍物的避障力 - 基于原始雷达数据的全局最近点方法
        
        ⚠️ 注意：这是与 calculate_cluster_based_avoidance_force() 并列的备选方法
        
        策略（不依赖聚类分析）：
        1. 直接从雷达原始数据提取所有有效点
        2. 将所有有效点转换到全局坐标系
        3. 计算每个点到下一步参考点(xr, yr)的距离
        4. 找出距离最近的一个点
        5. 仅对这一个全局最近点计算避障力
        
        优点：计算简单，无需聚类
        缺点：只考虑单个最近点，可能忽略多障碍物情况
        
        Args:
            laser_data: LaserScan消息
            
        Returns:
            np.array: 障碍物避障力向量 [fx, fy]
        """
        # 初始化避障力
        self.pxy_avoid.fill(0.0)
        
        # 1. 提取所有有效雷达点
        valid_points = self.extract_valid_points(laser_data)
        
        if len(valid_points) == 0:
            return np.zeros(2)
        
        # 2. 坐标变换参数
        cos_theta = np.cos(self.thetac)
        sin_theta = np.sin(self.thetac)
        
        # 3. 遍历所有有效点，找到距离参考点最近的点
        global_min_distance = float('inf')
        global_closest_point = None
        
        for point in valid_points:
            # 极坐标 → 机器人本体坐标
            local_x = point['range'] * math.cos(point['angle'])
            local_y = point['range'] * math.sin(point['angle'])
            
            # 机器人本体坐标 → 全局坐标
            global_x = self.xc + (cos_theta * local_x - sin_theta * local_y)
            global_y = self.yc + (sin_theta * local_x + cos_theta * local_y)
            
            # 计算到下一步参考点的距离
            dx = global_x - self.xr
            dy = global_y - self.yr
            distance = math.sqrt(dx**2 + dy**2)
            
            # 更新全局最近点
            if distance < global_min_distance:
                global_min_distance = distance
                global_closest_point = {'x': global_x, 'y': global_y}
        
        # 📊 记录最近障碍物点距离（用于图表）
        if global_min_distance != float('inf'):
            self.obstacle_distance_history.append({
                'timestamp': self.leader_time,
                'min_distance': global_min_distance
            })
        else:
            # 无障碍物情况：记录一个大值
            self.obstacle_distance_history.append({
                'timestamp': self.leader_time,
                'min_distance': 10.0
            })
        
        # 4. 检查是否需要避障（只对全局最近点）
        if global_min_distance <= self.ord_safe and global_closest_point is not None:
            # 计算避障力大小
            force_magnitude = (self.ord_avoid / global_min_distance) * (self.ord_avoid - global_min_distance)
            
            # 计算避障力方向（从障碍物指向参考点）
            angle_o2r = math.atan2(
                global_closest_point['y'] - self.yr,
                global_closest_point['x'] - self.xr
            )
            
            # 计算避障力分量
            force_x = force_magnitude * math.cos(angle_o2r)
            force_y = force_magnitude * math.sin(angle_o2r)
            
            self.pxy_avoid = np.array([force_x, force_y])
        
        return 

    def all_robot_observer_callback(self, msg, robot_id):
        """📦 异步更新邻居观测器缓存（不进行计算）"""
        if self.is_shutting_down:
            return
        # 🕐 检查消息格式：需要包含时间戳（第5个字段）
        if len(msg.data) >= 5:
            # 🕐 时间戳新鲜度检查（借鉴无人机项目实现）
            received_timestamp = msg.data[4]
            current_time = rospy.get_time()
            data_age = abs(current_time - received_timestamp)
            
            # 🕐 0.15秒新鲜度容差（与find_matching_leader_state的tolerance一致）
            freshness_tolerance = 0.15
            
            if data_age > freshness_tolerance:
                # 🚨 数据过时，记录警告并丢弃（类似无人机项目的处理）
                if data_age < 10.0:  # 10秒内可能是时钟不同步
                    rospy.logwarn_throttle(5.0, f"🕐 tb3_{self.robot_id} 收到过时观测器数据 from robot_{robot_id}: "
                                         f"数据年龄={data_age:.3f}s > 容差={freshness_tolerance}s")
                else:  # 超过10秒可能是严重的时钟问题
                    rospy.logerr_throttle(10.0, f"🕐 tb3_{self.robot_id} 收到严重过时数据 from robot_{robot_id}: "
                                        f"数据年龄={data_age:.3f}s，可能存在时钟同步问题！")
                return  # 🚫 丢弃过时数据
            
            # ✅ 数据新鲜，正常处理 - 更新缓存
            self.neighbor_observer_cache[robot_id] = {
                'zxeo': np.array([msg.data[0], msg.data[1]]),
                'dzxeo': np.array([msg.data[2], msg.data[3]]),
                'timestamp': received_timestamp
            }
            
            # 🔍 调试：记录观测器邻居状态接收（只在启动初期或出现异常时输出）
            if self.leader_time < 0.5 or (robot_id in self.neighbor_ids and hasattr(self, 'debug_counter')):
                is_neighbor = robot_id in self.neighbor_ids
                if is_neighbor and robot_id != self.robot_id:
                    rospy.logdebug(f"📨 tb3_{self.robot_id} 接收到邻居{robot_id}观测器状态: "
                                 f"[{msg.data[0]:.4f}, {msg.data[1]:.4f}, {msg.data[2]:.4f}, {msg.data[3]:.4f}] "
                                 f"时间戳={received_timestamp:.6f}, 延迟={data_age:.3f}s")
                elif robot_id == self.robot_id:
                    rospy.logdebug(f"🔄 tb3_{self.robot_id} 接收到自身观测器状态回环: "
                                 f"[{msg.data[0]:.4f}, {msg.data[1]:.4f}, {msg.data[2]:.4f}, {msg.data[3]:.4f}] "
                                 f"延迟={data_age:.3f}s")
                    
        elif len(msg.data) >= 4:
            # 🔄 向后兼容：处理没有时间戳的旧格式消息
            rospy.logwarn_throttle(10.0, f"🕐 tb3_{self.robot_id} 收到无时间戳的观测器数据 from robot_{robot_id}，"
                                 f"使用兼容模式处理")
            
            self.neighbor_observer_cache[robot_id] = {
                'zxeo': np.array([msg.data[0], msg.data[1]]),
                'dzxeo': np.array([msg.data[2], msg.data[3]]),
                'timestamp': rospy.get_time()
            }
        else:
            # ❌ 消息格式错误
            rospy.logerr(f"🚨 tb3_{self.robot_id} 收到格式错误的观测器数据 from robot_{robot_id}: "
                        f"长度={len(msg.data)} < 4，丢弃该消息")



    def leader_callback(self, msg):
        """接收并存储领导者状态，计算时钟偏移"""
        # 检查节点是否正在关闭
        if self.is_shutting_down:
            return
            
        # 检查消息格式
        if not msg.data or len(msg.data) < 6:
            rospy.logwarn(f"tb3_{self.robot_id} 领导者消息格式错误，长度不足6")
            return
        
        leader_time = msg.data[0]
        
        # 首次接收领导者消息时：切换到领导者时钟
        if not self.is_clock_synced:
            self.is_clock_synced = True
            self.first_leader_msg_time = rospy.get_time()
            import time
            wall_time = time.time()
            rospy.loginfo(f"🕐 tb3_{self.robot_id} 第一次接收领导者数据: ROS时间={self.first_leader_msg_time:.5f}s, 墙上时间={wall_time:.5f}s, 领导者时间={leader_time:.5f}s, 当前本地时间={self.local_time:.5f}s")
        
        # 同步后：更新本地时间为领导者时间（仅在control_loop中使用）
        # 注意：这里不直接修改 self.local_time，避免与 control_loop 冲突
        
        # 存储领导者状态到缓存中，等待定时器匹配使用
        self.received_leader_states[leader_time] = {
            "trajectory_time": msg.data[0],
            "x0": msg.data[1],
            "y0": msg.data[2],
            "u0": np.array([msg.data[3], msg.data[4]]),
            "theta0": msg.data[5],
            "received_at": rospy.get_time()
        }
        
        # 调试信息
        self.local_time = getattr(self, 'local_time', 0.0)
        # rospy.loginfo(f"📨 tb3_{self.robot_id} 在本地时间t ={self.local_time:.5f} 接收领导者数据: t={leader_time:.5f}, 缓存数量={len(self.received_leader_states)}")
        
        # 🚀 优化：限制缓存大小，只保留最近的N条数据
        max_cache_size = 5  # 只保留5条最新数据（0.5秒）足够匹配使用
        if len(self.received_leader_states) >= max_cache_size:
            # 删除最旧的数据（按轨迹时间排序）
            oldest_time = min(self.received_leader_states.keys())
            del self.received_leader_states[oldest_time]
            rospy.logdebug(f"🧹 tb3_{self.robot_id} 清理最旧缓存: t={oldest_time:.5f}")
        
        # 🔄 备用清理：基于接收时间的过期清理（防止时钟异常导致缓存爆炸）
        current_time = rospy.get_time()
        stale_threshold = 2.0  # 删除2秒前接收的数据
        stale_times = [t for t, state in list(self.received_leader_states.items()) 
                      if current_time - state.get('received_at', 0) > stale_threshold]
        if stale_times:
            for t in stale_times:
                del self.received_leader_states[t]
            rospy.logdebug(f"🧹 tb3_{self.robot_id} 清理过期缓存: {len(stale_times)}条")
    
    def control_loop(self, event):
        """📸 统一时钟控制循环：异步缓存+同步快照架构"""
        if self.is_shutting_down:
            return
        
        # ⏰ 关键检查：如果还未接收到领导者消息，直接返回等待
        # 避免在未同步时做无效的数据快照和计算
        if not self.is_clock_synced:
            rospy.logdebug(f"⏳ tb3_{self.robot_id} 等待首次领导者消息...")
            return
        
        # ⏱️ 记录控制循环开始时间（用于计算完整周期时间）
        cycle_start_time = rospy.get_time()
            
        # 初始化仿真时钟基准（仅首次执行）
        if not hasattr(self, 'simulation_start_time') or self.simulation_start_time is None:
            self.simulation_start_time = rospy.get_time()  # 记录仿真开始时间
            rospy.loginfo(f"🚀 tb3_{self.robot_id} 控制循环已启动，仿真基准时间={self.simulation_start_time:.3f}s")
        
        # ==================== 📸 统一快照所有传感器数据 ====================
        snapshot_time = rospy.get_time()
        
        # 快照里程计数据
        self.snapshot['odom'] = {
            'xc': self.odom_cache['xc'],
            'yc': self.odom_cache['yc'],
            'thetac': self.odom_cache['thetac']
        }
        
        # 快照激光雷达数据
        self.snapshot['laser'] = self.laser_cache['data']
        
        # 快照邻居观测器数据
        self.snapshot['neighbors'] = {}
        for robot_id in range(5):
            self.snapshot['neighbors'][robot_id] = {
                'zxeo': self.neighbor_observer_cache[robot_id]['zxeo'].copy(),
                'dzxeo': self.neighbor_observer_cache[robot_id]['dzxeo'].copy(),
                'timestamp': self.neighbor_observer_cache[robot_id]['timestamp']
            }
        
        self.snapshot['timestamp'] = snapshot_time
        
        rospy.logdebug(f"📸 tb3_{self.robot_id} 数据快照完成: t={snapshot_time:.3f}s, "
                      f"odom=({self.snapshot['odom']['xc']:.3f}, {self.snapshot['odom']['yc']:.3f}), "
                      f"laser={'有效' if self.snapshot['laser'] is not None else '无'}")
        
        # 计算本地时间（修正：第一次从最小时间开始，后续递增）
        if not hasattr(self, 'local_time'):
            # 第一次初始化：从领导者数据的最小时间开始
            if self.received_leader_states:
                self.local_time = min(self.received_leader_states.keys())
                rospy.loginfo(f"🕐 tb3_{self.robot_id} 初始化本地时间={self.local_time:.5f}s")
            else:
                self.local_time = 0.0
        else:
            # 后续递增（每次增加控制周期）
            self.local_time += self.t1
        
        # ==================== 🎯 基于快照执行控制计算 ====================
        control_computed = False
        
        # 尝试匹配领导者数据并执行控制
        matched_leader_state = self.find_matching_leader_state(self.local_time)
        
        if matched_leader_state is not None:
            matched_time = matched_leader_state["trajectory_time"]
            
            # 🔒 防止重复执行：检查是否已处理过该领导者时间
            if not hasattr(self, 'last_processed_leader_time'):
                self.last_processed_leader_time = -1.0
            
            if matched_time > self.last_processed_leader_time:
                # 更新领导者状态
                self.leader_state = matched_leader_state
                self.leader_time = matched_time
                self.last_processed_leader_time = matched_time
                
                rospy.logdebug(f"🎯 tb3_{self.robot_id} 匹配到领导者数据: t={self.leader_time:.5f}s")
                
                # 🔄 动态切换权重参数（基于领导者时间）
                self.update_weight_parameters()
                
                # 执行控制计算（内部会使用快照数据进行所有计算）
                self.execute_control_step()
                control_computed = True
            else:
                rospy.logdebug(f"⏭️ tb3_{self.robot_id} 跳过重复时间: t={matched_time:.5f}s (已处理)")
                control_computed = False
        else:
            rospy.logdebug(f"⏳ tb3_{self.robot_id} 等待领导者数据: 本地时间={self.local_time:.5f}s")
            control_computed = False
        
        # ==================== 📤 循环末尾统一发布控制输出 ====================
        if control_computed and not self.is_shutting_down:
            try:
                # 发布速度指令
                if hasattr(self, 'cmd_vel_pub'):
                    cmd_msg = Twist()
                    cmd_msg.linear.x = getattr(self, 'vc', 0.0)
                    cmd_msg.angular.z = getattr(self, 'wc', 0.0)
                    self.cmd_vel_pub.publish(cmd_msg)
                
                # 发布观测器状态（邻居通信）
                self.publish_own_observer_state()
                
                # 发布历史数据（使用execute_control_step缓存的消息）
                if hasattr(self, 'robot_history_msg_cache') and hasattr(self, 'robot_history_pub'):
                    self.robot_history_pub.publish(self.robot_history_msg_cache)
                
                # ⏱️ 计算完整控制循环周期时间
                cycle_end_time = rospy.get_time()
                full_cycle_duration = cycle_end_time - cycle_start_time
                
                rospy.logdebug(f"📤 tb3_{self.robot_id} 统一发布完成: v={getattr(self, 'vc', 0):.3f}, w={getattr(self, 'wc', 0):.3f}, 周期={full_cycle_duration*1000:.2f}ms")
                
                # 保存周期时间供历史数据使用
                self.last_full_cycle_duration = full_cycle_duration
            except Exception as e:
                rospy.logwarn(f"tb3_{self.robot_id} 发布控制输出时出错：{e}")
    
    def find_matching_leader_state(self, target_time, tolerance=0.15):
        """🚀 优化的领导者状态匹配算法（减少遍历开销）"""
        if not self.received_leader_states:
            return None
        
        # 🚀 优化：直接查找最接近的时间（避免遍历所有数据）
        available_times = sorted(self.received_leader_states.keys())
        
        # 策略1：二分查找最接近的时间（O(log n) 而不是 O(n)）
        import bisect
        insert_pos = bisect.bisect_left(available_times, target_time)
        
        candidates = []
        # 检查插入位置前后的1-2个候选时间
        for i in range(max(0, insert_pos-1), min(len(available_times), insert_pos+2)):
            if i < len(available_times):
                t = available_times[i]
                time_diff = abs(t - target_time)
                candidates.append((time_diff, t))
        
        # 按时间差排序，选择最接近的
        candidates.sort()
        
        for time_diff, leader_time in candidates:
            # 精确匹配（容差范围内）
            if time_diff <= tolerance:
                rospy.logdebug(f"✅ tb3_{self.robot_id} 精确匹配: 目标={target_time:.5f} → 使用={leader_time:.5f}, 差值={time_diff:.5f}s")
                return self.received_leader_states[leader_time]
            
            # 向前兼容（使用较早数据，但不超过1秒）
            if leader_time <= target_time and (target_time - leader_time) < 1.0:
                rospy.logdebug(f"🔄 tb3_{self.robot_id} 向前兼容: 目标={target_time:.5f} → 使用={leader_time:.5f}, 差值={target_time-leader_time:.5f}s")
                return self.received_leader_states[leader_time]
        
        # 容错：如果没有找到，使用最接近的未来数据（时钟不同步）
        if candidates and candidates[0][0] < 0.5:  # 未来数据在0.5秒内
            time_diff, leader_time = candidates[0]
            rospy.logwarn_throttle(5.0, f"⚠️ tb3_{self.robot_id} 使用未来数据: 目标={target_time:.5f} → 使用={leader_time:.5f}, 可能时钟不同步")
            return self.received_leader_states[leader_time]
        
        # 完全失败
        rospy.logwarn_throttle(2.0, f"❌ tb3_{self.robot_id} 无法匹配: 目标={target_time:.5f}, 可用={[f'{t:.3f}' for t in available_times[:3]]}...")
        return None
    
    def update_weight_parameters(self):
        """
        🔄 根据领导者时间动态切换权重参数
        
        时间段划分：
        - 15-31秒：第一个半圆段（使用S形半圆权重）
        - 39-55秒：第二个半圆段（使用S形半圆权重）
        - 其他时间：直线段或其他轨迹（使用默认权重）
        
        设计说明：
        - 两组权重参数已在__init__中定义
        - 此函数根据self.leader_time动态切换self.Qz和self.Rz
        - 在control_loop中每次更新领导者时间后调用
        """
        if not hasattr(self, 'leader_time'):
            return
        
        t = self.leader_time
        
        # 判断是否在半圆时间段内（15-31s 或 39-55s）
        is_circle_segment = (15 <= t <= 31) or (39 <= t <= 55)
        
        if is_circle_segment:
            # 切换到S形半圆权重组
            if self.current_weight_mode != "circle":
                self.Qz = self.Qz_circle
                self.Rz = self.Rz_circle
                self.current_weight_mode = "circle"
                rospy.loginfo(f"🔄 tb3_{self.robot_id} 切换权重参数 → S形半圆组 (t={t:.2f}s)")
        else:
            # 切换到默认权重组
            if self.current_weight_mode != "default":
                self.Qz = self.Qz_default
                self.Rz = self.Rz_default
                self.current_weight_mode = "default"
                rospy.loginfo(f"🔄 tb3_{self.robot_id} 切换权重参数 → 默认组 (t={t:.2f}s)")
        
    def shutdown_callback(self, msg):
        """接收系统停止信号并优雅关闭"""
        if msg.data:
            rospy.loginfo(f"tb3_{self.robot_id} 收到系统停止信号，开始优雅关闭...")
            
            # 设置关闭标志，防止继续执行控制逻辑
            self.is_shutting_down = True
            
            # 停止机器人运动
            stop_cmd = Twist()
            stop_cmd.linear.x = 0.0
            stop_cmd.angular.z = 0.0
            
            # 安全发布停止指令（检查发布器是否仍然有效）
            try:
                self.cmd_vel_pub.publish(stop_cmd)
            except Exception as e:
                rospy.logwarn(f"tb3_{self.robot_id} 发布停止指令时出错：{e}")
            
            # 保存最终历史数据
            self.save_final_history()
            
            # 优雅关闭节点
            rospy.signal_shutdown(f"tb3_{self.robot_id} 接收到系统停止信号，正常关闭")
        
    def gfunction(self, u, yp, ym):
        """约束函数（限制控制输入范围）"""
        gf = np.zeros_like(u)
        for i in range(len(u)):
            if u[i] > yp[i]:
                gf[i] = yp[i]
            elif u[i] < ym[i]:
                gf[i] = ym[i]
            else:
                gf[i] = u[i]
        return gf

    @staticmethod
    def angle_difference_and_velocity(target_angle, current_angle, dt=None):
        """
        计算角度差并可选地计算角速度，自动处理跨象限问题
        
        Args:
            target_angle: 目标角度（弧度）
            current_angle: 当前角度（弧度）
            dt: 时间间隔（秒），如果提供则返回角速度，否则返回角度差
            
        Returns:
            如果dt为None：角度差值（弧度），范围 [-π, π]
            如果dt不为None：角速度（弧度/秒）
        """
        diff = target_angle - current_angle
        angle_diff = np.arctan2(np.sin(diff), np.cos(diff))
        
        if dt is not None:
            return angle_diff / dt
        else:
            return angle_diff


    def update_formation_offset(self):
        """更新编队偏移（使用领导者时间，集成避障功能）"""
        # 计算编队偏移
        # 实物修改点9
        # "real_experiment_trajectory_line":
        # self.px = self.bb * self.formation_radius * np.cos(self.aa * self.leader_time + self.robot_id * 2 * np.pi / self.Rnum)
        # self.py = self.bb * self.formation_radius * np.sin(self.aa * self.leader_time + self.robot_id * 2 * np.pi / self.Rnum)
    
        # # "real_experiment_trajectory":
        self.px = self.bb * self.formation_radius * np.cos(self.aa * self.leader_time + ((self.robot_id + 1) % self.Rnum) * 2 * np.pi / self.Rnum)
        self.py = self.bb * self.formation_radius * np.sin(self.aa * self.leader_time + ((self.robot_id + 1) % self.Rnum) * 2 * np.pi / self.Rnum)

        # 应用避障力修正（基于聚类计算的避障力）
        self.px -= self.pxy_avoid[0]  # px方向避障修正
        self.py -= self.pxy_avoid[1]  # py方向避障修正
        
        # 调试信息：输出前3次避障修正结果（仅在有避障力时输出）
        if self.debug_counter <= 3:
            avoidance_force_magnitude = np.linalg.norm(self.pxy_avoid)
            if avoidance_force_magnitude > 0.001:
                rospy.loginfo(f"[时间步{self.debug_counter-1}] [tb3_{self.robot_id}] 避障修正: px={self.px:.3f}, py={self.py:.3f}, "
                             f"避障力幅度={avoidance_force_magnitude:.4f}, 偏移=[{self.pxy_avoid[0]:.3f}, {self.pxy_avoid[1]:.3f}]")

        # 计算相对偏差（与邻居节点期望的格式一致）
        self.zx = np.array([self.x_hat - self.px, self.y_hat - self.py]).reshape(-1, 1)

    def publish_own_observer_state(self):
        """🚀 发布自身观测器状态供其他机器人使用（带时间戳验证）"""
        if self.is_shutting_down:
            return
            
        # 🚀 修复: 检查发布器是否已初始化
        if not hasattr(self, 'observer_state_pub'):
            rospy.logwarn(f"tb3_{self.robot_id} 观测器状态发布器尚未初始化，跳过发布")
            return

        # 🚀 调试：确认函数被调用
        # rospy.loginfo(f"tb3_{self.robot_id} 正在发布观测器状态: zxeo=[{self.zxeo[0,0]:.3f}, {self.zxeo[1,0]:.3f}], dzxeo=[{self.dzxeo[0,0]:.3f}, {self.dzxeo[1,0]:.3f}]")

        # 🕐 获取当前ROS时间作为时间戳（借鉴无人机项目的实现）
        current_timestamp = rospy.get_time()

        # 发布观测器状态消息：[zxeo[0], zxeo[1], dzxeo[0], dzxeo[1], timestamp]
        observer_msg = Float64MultiArray()
        observer_msg.data = [
            self.zxeo[0, 0], self.zxeo[1, 0],
            self.dzxeo[0, 0], self.dzxeo[1, 0],
            current_timestamp  # 🕐 新增：时间戳字段
        ]
        
        try:
            self.observer_state_pub.publish(observer_msg)
            # rospy.loginfo(f"tb3_{self.robot_id} 观测器状态发布成功，时间戳: {current_timestamp:.6f}")
        except Exception as e:
            rospy.logwarn(f"tb3_{self.robot_id} 发布观测器状态时出错：{e}")

    def compute_consensus_error(self):
        """计算基于观测器的一致性误差（使用快照数据）"""
        
        # 📸 使用快照数据：直接从self.snapshot['neighbors']获取邻居观测器状态
        if self.snapshot['neighbors']:
            # 计算观测器更新需要的邻居项
            sum_dzxeo_j = np.zeros((2, 1))
            sum_consensus_error_zxeo = np.zeros((2, 1))
            
            # 基于邻接矩阵A计算邻居观测器状态的影响
            for neighbor_id in self.neighbor_ids:
                if neighbor_id in self.snapshot['neighbors']:
                    neighbor_zxeo = self.snapshot['neighbors'][neighbor_id]["zxeo"].reshape(2, 1)
                    neighbor_dzxeo = self.snapshot['neighbors'][neighbor_id]["dzxeo"].reshape(2, 1)
                    
                    # 🔍 前3个时间步打印使用的邻居观测器数据(与纯仿真一致的位置)
                    if self.debug_counter <= 3:
                        rospy.loginfo(f"[时间步{self.debug_counter-1}] [tb3_{self.robot_id}] 使用邻居 [tb3_{neighbor_id}] 的观测器数据: "
                                    f"zxeo=[{neighbor_zxeo[0,0]:.6f}, {neighbor_zxeo[1,0]:.6f}], "
                                    f"dzxeo=[{neighbor_dzxeo[0,0]:.6f}, {neighbor_dzxeo[1,0]:.6f}]")
                    
                    # 累加邻居的观测器状态和导数
                    sum_dzxeo_j += self.A[self.robot_id, neighbor_id] * neighbor_dzxeo
                    sum_consensus_error_zxeo += self.A[self.robot_id, neighbor_id] * (self.zxeo - neighbor_zxeo)

        # 计算SS项（滑模观测器设计中的滑模面）
        SS = sum_consensus_error_zxeo + self.leader_direct * (self.zxeo - np.array([self.leader_state["x0"], self.leader_state["y0"]]).reshape(2, 1))
        
        # 观测器状态增量更新（基于滑模观测器设计）
        self.dzxeo = (
            (1.0 / self.indegree) * (sum_dzxeo_j + self.leader_direct * self.leader_state["u0"].reshape(2, 1))
            - self.ob_eta * (1.0 / self.indegree) * np.sign(SS) * np.power(np.abs(SS), self.ob_alp)
        ).reshape(-1, 1)
        
        # 计算误差：使用观测器估计的领导者状态而不是实际领导者状态
        self.ex = self.zx - self.zxeo
        # 观测器状态积分更新
        self.zxeo = self.zxeo + self.dzxeo * self.t1

        #错误的顺序
        # # 观测器状态积分更新
        # self.zxeo = self.zxeo + self.dzxeo * self.t1
        # # 计算误差：使用观测器估计的领导者状态而不是实际领导者状态
        # self.ex = self.zx - self.zxeo

        # 动态反馈项：考虑观测器动态
        self.fx = self.ex - self.t1 * self.dzxeo

        # if self.debug_counter < 4:
        #     print(f"[时间步{self.debug_counter-1}] [tb3_{robot_id}] zx=[{self.zx[0,0]:.10f}, {self.zx[1,0]:.10f}],"
        #            f" 误差计算: ex=[{self.ex[0,0]:.10f}, {self.ex[1,0]:.10f}], "
        #           f"fx=[{self.fx[0,0]:.10f}, {self.fx[1,0]:.10f}]")

    def compute_solver_planner(self):
        """pdnn控制算法计算"""
        # 🕐 开始计时PDNN算法执行
        self.pdnn_start_time = rospy.get_time()
        self.pdnn_call_count += 1
        
        G = np.vstack((
            np.hstack((self.gx, np.zeros_like(self.gx))),
            np.hstack((self.gx, self.gx)),
            np.hstack((self.gx, self.gx))
        ))

        tildrg = np.vstack((self.gx @ self.u.reshape(-1, 1),
                            self.gx @ self.u.reshape(-1, 1),
                            self.gx @ self.u.reshape(-1, 1)))

        tildrf = np.vstack((self.fx.reshape(-1, 1),
                            self.fx.reshape(-1, 1),
                            self.fx.reshape(-1, 1)))

        tildrI = np.eye(self.Nu * self.m_gx_u) + np.vstack((np.zeros((2, self.Nu * self.m_gx_u)),
                                            np.hstack((np.eye(self.m_gx_u), np.zeros((self.m_gx_u, self.m_gx_u))))))
        
        Irnn = np.eye(self.Nu * self.n_gx_x, self.Nu * self.m_gx_u)

        # 计算二次规划问题的矩阵W、C1和E
        W = 2 * (G.T @ self.Q @ G + self.R)
        C1 = 2 * G.T @ self.Q @ (tildrg + tildrf)
        E = np.vstack((-tildrI, tildrI, -G, G, Irnn))

        # 定义约束向量b1
        b1 = np.vstack((-self.abarUmin1 + self.abaru.reshape(-1, 1),
                         self.abarUmax1 - self.abaru.reshape(-1, 1),
                        -self.abarxmin + tildrg + tildrf,
                         self.abarxmax - tildrg - tildrf,
                        -self.detabarUmin,
                         self.detabarUmax))

        # 定义一些常量
        m = b1.shape[0]
        myInf = 1e10

        Pinfty = myInf * np.ones((m, 1))
        Minfty = -Pinfty

        p  = -E @ np.linalg.inv(W) @ C1
        M = -np.linalg.inv(W) @ C1
        yp = np.vstack((b1, self.detabarUmax))
        ym = np.vstack((Minfty, self.detabarUmin))
        ImH = E @ np.linalg.inv(W) @ E.T
        IpHt = np.linalg.inv(W) @ E.T
        RIpHt = (np.linalg.inv(IpHt @ IpHt.T) @ IpHt).T
        
        # 初始化变量ycv
        ycv = np.zeros((2*self.Nu, self.n+1, 1))
        for i in range(2*self.Nu):
            ycv[i, 0, 0] = self.y0x[i]

        # 使用龙格库塔方法进行数值求解
        for ii in range(self.n):
            k11 = (-IpHt @ (self.gfunction(ImH @ RIpHt @ (ycv[:, ii] - M) + p - RIpHt @ (ycv[:, ii] - M), yp, ym) - 
                        ImH @ RIpHt @ (ycv[:, ii] - M) - p))/self.gamma
            k21 = (-IpHt @ (ImH @ RIpHt @ ((ycv[:, ii] + self.h*k11/2) - M) - 
                            self.gfunction(ImH @ RIpHt @ ((ycv[:, ii] + self.h*k11/2) - M) - 
                                    RIpHt @ ((ycv[:, ii] + self.h*k11/2) - M) + p, yp, ym) + p))/self.gamma
            k31 = (-IpHt @ (ImH @ RIpHt @ ((ycv[:, ii] + self.h*k21/2) - M) - 
                            self.gfunction(ImH @ RIpHt @ ((ycv[:, ii] + self.h*k21/2) - M) - 
                                    RIpHt @ ((ycv[:, ii] + self.h*k21/2) - M) + p, yp, ym) + p))/self.gamma
            k41 = (-IpHt @ (ImH @ RIpHt @ ((ycv[:, ii] + self.h*k31) - M) - 
                            self.gfunction(ImH @ RIpHt @ ((ycv[:, ii] + self.h*k31) - M) - 
                                    RIpHt @ ((ycv[:, ii] + self.h*k31) - M) + p, yp, ym) + p))/self.gamma
            ycv[:, ii+1] = ycv[:, ii] + self.h*(k11 + 2*k21 + 2*k31 + k41)/6

        dot_y1 = ycv[:, self.n]
        # ✅ 修复后：
        self.y0x = dot_y1.ravel().copy()  # 独立拷贝
        a = self.y0x

        self.detabarU = a[0:2*self.Nu]
        dd = self.detabarU
        # 🔧 修复：abaru使用拷贝保持原始PDNN输出，避免被限幅操作影响
        self.abaru = self.detabarU.copy()  # 独立拷贝，保持PDNN原始输出
        self.u = dd[0:2].copy()  # 独立拷贝，避免影响原始数据

         # 打印前三个时间步的u值（debug_counter在调用此函数前已被递增）
        if self.debug_counter < 3:
            rospy.loginfo(f"[时间步{self.debug_counter-1}] [tb3_{robot_id}]: u = [{self.u[0]:.6f}, {self.u[1]:.6f}]")

        # 控制输入限制和轨迹更新
    
        # 限制x方向输入
        if self.u[0] >= 0.22:
            self.u[0] = 0.22
        elif self.u[0] < -0.22:
            self.u[0] = -0.22

        # 限制y方向输入
        if self.u[1] >= 0.22:
            self.u[1] = 0.22
        elif self.u[1] < -0.22:
            self.u[1] = -0.22
            
        # 提取控制输入
        self.ux = self.u[0]
        self.uy = self.u[1]

    def update_reference_trajectory(self):
        """更新期望的期望及参考轨迹和计算参考线角速度"""
        self.x_hat = self.x_hat + self.ux * self.t1
        self.y_hat = self.y_hat + self.uy * self.t1
        self.xr = self.x_hat
        self.yr = self.y_hat

        # 计算期望航向角
        self.theta_hat = np.arctan2(self.uy, self.ux)
        
        # 【优化】使用统一的角度处理函数计算角速度
        self.wr = self.angle_difference_and_velocity(self.theta_hat, self.thetar, self.t1)
        self.vr = np.sqrt(self.ux**2 + self.uy**2)

        self.thetar = self.theta_hat # 利用thetar是theta_hat相等来计算wr后（处理角度变换）即可更新了

    def compute_track_error(self):
        """计算跟踪误差"""

        self.xe = np.cos(self.thetac) * (self.xr - self.xc) + \
        np.sin(self.thetac) * (self.yr - self.yc)
        self.ye = np.cos(self.thetac) * (self.yr - self.yc) - \
        np.sin(self.thetac) * (self.xr - self.xc)

        # 【优化】使用统一的角度处理函数计算角度误差
        self.thetae = self.angle_difference_and_velocity(self.thetar, self.thetac)

    def compute_solver_track(self):
        # 计算中间变量
        k0 = 2 * np.sign(self.vr)
        self.L1 = np.sqrt(1 + self.xe**2 + self.ye**2)
        self.thetae_hat = self.thetae + np.arctan2(k0 * self.ye, self.L1.item())
        self.L2 = np.sqrt(1 + self.xe**2 + (1 + k0**2) * self.ye**2)
        self.L3 = np.sqrt(1 + self.thetae_hat**2)
        
        # 计算非线性项
        if self.thetae_hat == 0:
            alp = np.cos(self.thetae)
        else:
            alp = (1/self.thetae_hat) * (np.sin(self.thetae) + 
                np.sin(np.arctan2(k0 * self.ye, self.L1)))
        
        self.M0 = (k0 * self.vr * np.sin(self.thetae) * (1 + self.xe**2) - 
                k0 * self.xe * self.ye * self.vr * np.cos(self.thetae)) / \
                (self.L1 * (self.L2**2))

        # 构建预测模型矩阵
        self.fxz = np.array([
            self.xe,
            self.ye,
            self.thetae_hat
        ]) + self.t1 * np.array([
            self.vr * np.cos(self.thetae),
            self.vr * np.sin(self.thetae),
            self.wr + self.M0.item()
        ])
        
        # 输入矩阵
        self.gxxz = self.t1 * np.array([
                    [-1, self.ye],
                    [0, -self.xe],
                    [(k0 * self.xe * self.ye)/(self.L1 * self.L2**2).item(), -(1 + (k0 * self.L1 * self.xe)/(self.L2**2)).item()]           
                                                                                                                    ])
        # 构建扩展预测模型矩阵
        zz = np.zeros((3, 2))

        Gz = np.vstack((
        np.hstack((self.gxxz, zz)),
        np.hstack((self.gxxz, self.gxxz)),
        np.hstack((self.gxxz, self.gxxz))
        ))

        tildrgz = np.vstack((
            self.gxxz @ self.uz.reshape(-1, 1),
            self.gxxz @ self.uz.reshape(-1, 1),
            self.gxxz @ self.uz.reshape(-1, 1)
        ))

        tildrfz = np.vstack((
            self.fxz.reshape(-1, 1),
            self.fxz.reshape(-1, 1),
            self.fxz.reshape(-1, 1)
        ))

        tildrIz = np.eye(4, 4) + np.vstack((
                    np.zeros((2, 4)),
                    np.hstack((np.eye(2, 2), np.zeros((2, 2))))
        ))

        Irnnz = np.eye(4, 4)

        # 构建QP问题
        Wz = 2 * (Gz.T @ self.Qz @ Gz + self.Rz)
        Cz = 2 * Gz.T @ self.Qz @ (tildrgz + tildrfz)
        Ez = np.vstack((
            -tildrIz,
            tildrIz,
            -Gz,
            Gz,
            Irnnz
        ))
        
        bz = np.vstack((
            -self.abarUminz + self.abaruz.reshape(-1, 1),
            self.abarUmaxz - self.abaruz.reshape(-1, 1),
            -self.abarxminz + tildrfz + tildrgz,
            self.abarxmaxz - tildrfz - tildrgz,
            -self.detabarUminz,
            self.detabarUmaxz
        ))

        # 定义神经网络优化参数
        mz = 4 * self.Nu + 6 * self.N
        myInfz = 1e100
        Pinftyz = myInfz * np.ones((mz, 1))
        Minftyz = -Pinftyz
        
        pz = -Ez @ np.linalg.inv(Wz) @ Cz
        Mz = -np.linalg.inv(Wz) @ Cz
        ypz = np.vstack((bz, self.detabarUmaxz))
        ymz = np.vstack((Minftyz, self.detabarUminz))
        ImHz = Ez @ np.linalg.inv(Wz) @ Ez.T
        IpHtz = np.linalg.inv(Wz) @ Ez.T
        RIpHtz = (np.linalg.inv(IpHtz @ IpHtz.T) @ IpHtz).T

        # 初始化变量ycvz
        ycvz = np.zeros((4, self.n+1, 1))
        ycvz[:, 0] = self.y0z.reshape(-1, 1)

        for ii in range(self.n):
            k11 = (-IpHtz @ (ImHz @ RIpHtz @ (ycvz[:, ii] - Mz) - 
                            self.gfunction(ImHz @ RIpHtz @ (ycvz[:, ii] - Mz) - 
                                    RIpHtz @ (ycvz[:, ii] - Mz) + pz, ypz, ymz) + pz))/self.gamma
            k21 = (-IpHtz @ (ImHz @ RIpHtz @ ((ycvz[:, ii] + self.h*k11/2) - Mz) - 
                            self.gfunction(ImHz @ RIpHtz @ ((ycvz[:, ii] + self.h*k11/2) - Mz) - 
                                    RIpHtz @ ((ycvz[:, ii] + self.h*k11/2) - Mz) + pz, ypz, ymz) + pz))/self.gamma
            k31 = (-IpHtz @ (ImHz @ RIpHtz @ ((ycvz[:, ii] + self.h*k21/2) - Mz) - 
                            self.gfunction(ImHz @ RIpHtz @ ((ycvz[:, ii] + self.h*k21/2) - Mz) - 
                                    RIpHtz @ ((ycvz[:, ii] + self.h*k21/2) - Mz) + pz, ypz, ymz) + pz))/self.gamma
            k41 = (-IpHtz @ (ImHz @ RIpHtz @ ((ycvz[:, ii] + self.h*k31) - Mz) - 
                            self.gfunction(ImHz @ RIpHtz @ ((ycvz[:, ii] + self.h*k31) - Mz) - 
                                    RIpHtz @ ((ycvz[:, ii] + self.h*k31) - Mz) + pz, ypz, ymz) + pz))/self.gamma
            ycvz[:, ii+1] = ycvz[:, ii] + self.h*(k11 + 2*k21 + 2*k31 + k41)/6

        dot_y1z = ycvz[:, self.n]
        # ✅ 修复后：
        self.y0z = dot_y1z.reshape(-1).copy()  # 独立拷贝
        az = self.y0z

        detabarUz = az[0:2*self.Nu]
        ddz = detabarUz
        # abaruz = ddz
        # self.uz = abaruz[0:2]
        # ✅ 修复后：
        self.abaruz = detabarUz.copy()  # 独立拷贝
        self.uz = ddz[0:2].copy()  # 独立拷贝

        # 实际控制输入限制和更新
        # 限制线速度
        if self.uz[0] >= 0.22:
            self.uz[0] = 0.22
        elif self.uz[0] < -0.22:
            self.uz[0] = -0.22

        # 限制角速度
        if self.uz[1] >= 2.84:
            self.uz[1] = 2.84
        elif self.uz[1] < -2.84:
            self.uz[1] = -2.84
        
        self.vc = self.uz[0]
        self.wc = self.uz[1]
        
        # 🕐 结束PDNN算法计时并记录
        if hasattr(self, 'pdnn_start_time'):
            pdnn_end_time = rospy.get_time()
            pdnn_duration = pdnn_end_time - self.pdnn_start_time
            self.pdnn_execution_times.append(pdnn_duration)

    def save_final_history(self):
        """🚀 话题优化版：节点关闭时记录最终状态"""
        
        rospy.loginfo(f"\n" + "="*70)
        rospy.loginfo(f"⏱️  tb3_{self.robot_id} 控制系统性能统计总结")
        rospy.loginfo(f"="*70)
        
        # 💾 输出聚类与避障计算时间统计
        if hasattr(self, 'clustering_avoidance_times') and len(self.clustering_avoidance_times) > 0:
            total_calls = len(self.clustering_avoidance_times)
            avg_time = sum(self.clustering_avoidance_times) / total_calls
            min_time = min(self.clustering_avoidance_times)
            max_time = max(self.clustering_avoidance_times)
            rospy.loginfo(f"\n📊 [tb3_{self.robot_id}] 聚类与避障: {total_calls}次, 平均{avg_time*1000:.2f}ms, 最小{min_time*1000:.2f}ms, 最大{max_time*1000:.2f}ms")
        
        # 💾 输出PDNN算法性能总结
        if hasattr(self, 'pdnn_execution_times') and len(self.pdnn_execution_times) > 0:
            total_calls = len(self.pdnn_execution_times)
            avg_time = sum(self.pdnn_execution_times) / total_calls
            min_time = min(self.pdnn_execution_times)
            max_time = max(self.pdnn_execution_times)
            rospy.loginfo(f"📊 [tb3_{self.robot_id}] PDNN算法: {total_calls}次, 平均{avg_time*1000:.2f}ms, 最小{min_time*1000:.2f}ms, 最大{max_time*1000:.2f}ms")
     
        # 💾 输出控制算法计算时间统计
        if hasattr(self, 'algorithm_times') and len(self.algorithm_times) > 0:
            total_calls = len(self.algorithm_times)
            avg_time = sum(self.algorithm_times) / total_calls
            min_time = min(self.algorithm_times)
            max_time = max(self.algorithm_times)
            rospy.loginfo(f"📊 [tb3_{self.robot_id}] 控制算法(一致性误差计算到控制输入计算结果): {total_calls}次, 平均{avg_time*1000:.2f}ms, 最小{min_time*1000:.2f}ms, 最大{max_time*1000:.2f}ms")
          
        rospy.loginfo(f"\n" + "="*70 + "\n")
        
        #  已优化：历史数据现在通过话题实时发布，无需保存本地缓存
        rospy.loginfo(f"🚀 tb3_{self.robot_id} 话题数据流已停止，控制节点正常关闭")

    def execute_control_step(self, leader_time=None):
        """执行一次控制计算（由独立定时器驱动，使用匹配的领导者数据）"""
        
        # 🔢 递增调试计数器（用于控制调试输出）
        self.debug_counter += 1
        
        # 📸 ==== 步骤1: 快照数据赋值 ==== 
        # 将快照数据赋值给控制变量，保证所有计算使用快照数据
        self.xc = self.snapshot['odom']['xc']
        self.yc = self.snapshot['odom']['yc']
        self.thetac = self.snapshot['odom']['thetac']
        
        # 使用传入的领导者时间（已经通过find_matching_leader_state匹配）
        if leader_time is not None:
            self.leader_time = leader_time
        else:
            # 如果没有传入时间，从当前leader_state获取（向后兼容）
            self.leader_time = self.leader_state.get("trajectory_time", 0.0)
        
        # 记录控制开始时间，用于调试时序
        rospy.logdebug(f"🎯 tb3_{self.robot_id} 定时器驱动控制计算，目标时间：{self.leader_time:.5f}s")

        # 📸 ==== 步骤2: 使用激光雷达快照数据进行避障力计算 ====
        clustering_avoidance_start_time = rospy.get_time()
        
        if self.snapshot['laser'] is not None:
            # 方法1: 基于聚类的多障碍物避障（当前使用）
            self.perform_laser_clustering_analysis(self.snapshot['laser'])
            self.calculate_cluster_based_avoidance_force()
            
            # 方法2: 基于原始点的全局最近点避障（备选方法，已注释）
            # self.calculate_obstacles_single_closest_force(self.snapshot['laser'])
        
        clustering_avoidance_end_time = rospy.get_time()
        clustering_avoidance_duration = clustering_avoidance_end_time - clustering_avoidance_start_time
        
        # 📸 ==== 步骤3: 控制算法计算 ====
        # 记录算法计算开始时间（控制算法部分，不含聚类与避障）
        algorithm_start_time = rospy.get_time()
        
        # 使用避障力修正编队偏移
        self.update_formation_offset()

        # 计算一致性误差（直接使用观测器快照数据）
        self.compute_consensus_error()
        # rospy.loginfo(f"【Debug】tb3_{self.robot_id} 在领导者时间{leader_time:.3f}时 计算的一致性误差：ex={self.ex}, fx={self.fx}")  # 使用领导者时间验证误差计算
    
        # 计算轨迹规划控制输入
        self.compute_solver_planner()
        # rospy.loginfo(f"【Debug】tb3_{self.robot_id} 在领导者时间{leader_time:.3f}时 计算的轨迹规划速度：ux={self.ux:.3f}, uy={self.uy:.3f}")  # 使用领导者时间验证速度

        # 计算参考轨迹
        self.update_reference_trajectory()

        # 计算跟踪误差
        self.compute_track_error()

        # 计算轨迹跟踪控制输入
        self.compute_solver_track()
        # rospy.loginfo(f"【Debug】tb3_{self.robot_id} 在领导者时间{leader_time:.3f}时 计算得到的最终控制输入：速度：vc={self.vc:.3f}, wc={self.wc:.3f}，纯算法耗时：{algorithm_duration*1000:.2f}ms")  # 使用已获取的领导者时间

        # 记录算法计算结束时间
        algorithm_end_time = rospy.get_time()
        algorithm_duration = algorithm_end_time - algorithm_start_time
        
        # 计算总耗时（包含聚类与避障、控制算法）
        total_computation_duration = clustering_avoidance_duration + algorithm_duration
        
        # ⏱️ 记录各阶段耗时到统计列表（跳过第一次数据，避免初始化开销影响统计）
        # 📝 注意：首次执行时间会明显偏高（通常100-200ms），原因包括：
        #    - NumPy首次矩阵运算需要加载BLAS/LAPACK库和初始化线程池
        #    - Python对象首次创建和内存分配开销
        #    - 系统缓存预热
        #    跳过首次数据后，后续执行趋于稳定（通常30-50ms）
        if self.debug_counter > 1:  # 跳过第一次
            self.clustering_avoidance_times.append(clustering_avoidance_duration)
            self.algorithm_times.append(algorithm_duration)
                         
        # 📸 异步缓存架构：控制输出由control_loop末尾统一发布
        # 这里只记录计算结果，不发布
        rospy.logdebug(f"🎯 tb3_{self.robot_id} 控制计算完成: v={self.vc:.3f}, w={self.wc:.3f}")
        rospy.logdebug(f"   ⏱️ 耗时分析: 聚类与避障={clustering_avoidance_duration*1000:.2f}ms, "
                      f"控制算法={algorithm_duration*1000:.2f}ms, 总计={total_computation_duration*1000:.2f}ms")
    
        # 🔧 计算与仿真代码一致的编队误差（xc - leader_x - px, yc - leader_y - py, thetac - leader_theta）
        formation_error_x = self.xc - self.leader_state["x0"] - self.px
        formation_error_y = self.yc - self.leader_state["y0"] - self.py
        # 🔧 修正：使用角度差计算函数处理角度跨越问题
        formation_error_theta = self.angle_difference_and_velocity(self.leader_state["theta0"], self.thetac)

        # 🚀 ROS话题优化：发布历史数据到专用话题（替代参数服务器）
        robot_history_msg = RobotHistoryData()
        robot_history_msg.robot_id = self.robot_id
        robot_history_msg.trajectory_time = float(self.leader_time)
        robot_history_msg.ros_timestamp = float(rospy.get_time())
        robot_history_msg.xc = float(self.xc)
        robot_history_msg.yc = float(self.yc)
        robot_history_msg.thetac = float(self.thetac)
        robot_history_msg.vc = float(self.uz[0].item())
        robot_history_msg.wc = float(self.uz[1].item())
        robot_history_msg.xe = float(formation_error_x)
        robot_history_msg.ye = float(formation_error_y)
        robot_history_msg.thetae = float(formation_error_theta)
        robot_history_msg.xr = float(self.xr)
        robot_history_msg.yr = float(self.yr)
        # 🎯 观测器估计数据（对领导者位置的估计）
        robot_history_msg.zxeo_x = float(self.zxeo[0, 0])
        robot_history_msg.zxeo_y = float(self.zxeo[1, 0])
        
        # ⏱️ 时间数据：computation_time记录算法耗时，full_cycle_time由control_loop末尾更新
        robot_history_msg.computation_time = float(total_computation_duration)
        robot_history_msg.full_cycle_time = float(getattr(self, 'last_full_cycle_duration', self.t1))
        
        # 📊 避障相关数据（直接从历史列表获取最新值，绘图脚本负责处理异常值）
        robot_history_msg.raw_min_obstacle_distance = float(self.raw_min_distance_history[-1]['min_distance']) if self.raw_min_distance_history else float('inf')
        robot_history_msg.closest_obstacle_distance = float(self.obstacle_distance_history[-1]['min_distance']) if self.obstacle_distance_history else float('inf')
        robot_history_msg.total_clusters_count = int(self.clustering_analysis_history[-1]['total_clusters_count']) if self.clustering_analysis_history else 0
        robot_history_msg.avoidance_force_magnitude = float(self.clustering_analysis_history[-1]['avoidance_force_magnitude']) if self.clustering_analysis_history else 0.0
        
        # 📸 异步缓存架构：数据发布由control_loop末尾统一执行
        # 将robot_history_msg保存为实例变量供后续发布
        self.robot_history_msg_cache = robot_history_msg


if __name__ == "__main__":
    try:
        # 步骤1：先初始化节点（用固定名称，避免依赖参数）
        rospy.init_node("tb3_controller", anonymous=True)  # anonymous=True避免节点名冲突
        # 步骤2：再获取私有参数（此时节点已初始化，可解析~robot_id）
        robot_id = rospy.get_param("~robot_id")
        # 步骤3：创建控制器实例
        controller = TurtleBot3Controller(robot_id)
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
    except KeyError:
        rospy.logerr("请为节点设置私有参数 '~robot_id'（0-4）！")
#!/usr/bin/env python3 
#######
#用于纯仿真测试单机 TurtleBot3 分布式控制算法核心逻辑
#######
import numpy as np
import matplotlib.pyplot as plt

class TurtleBot3Controller:
    def __init__(self, robot_id):
        # 机器人配置（适配tb3_0~4）
        self.robot_id = robot_id  # 0-4
        
        # 控制参数（GPNN相关）
        self.N = 3
        self.Nu = 2
        self.gamma = 0.1
        self.t1 = 0.1  # 控制周期(s)
        self.Q = 1*1e9 * np.eye(2*self.N)
        self.R = 1*1e4* np.eye(2*self.Nu)


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

        #轨迹跟踪权重
        # 更新权重矩阵
        self.em = 100
        self.Qx = 1000 * self.em
        self.Qy = 1000 * self.em
        self.Qtheta = 10 * self.em
        self.I0 = np.eye(1*self.N)
        self.Qxyt = np.array([[self.Qx, 0, 0],
                        [0, self.Qy, 0],
                        [0, 0, self.Qtheta]])
        self.Qz = np.kron(self.I0, self.Qxyt)
        self.Rz = 10 * np.eye(2*self.Nu)

        # 初始化轨迹规划输入
        self.ux = 0
        self.uy = 0
        self.u = np.zeros((2,1))

        # 初始化中间变量
        self.abaru = np.zeros((2*self.Nu, 1))
        self.detabarU = np.zeros((2*self.Nu, 1))
        self.abaruz = np.zeros((2*self.Nu, 1))
        self.detabarUz = np.zeros((2*self.Nu, 1))

        # 初始化GPNN状态变量
        self.y0x = np.zeros((2*self.Nu, 1))
        self.y0z = np.zeros((2*self.Nu, 1))


        # 参考位置初始化，实际的位置也放在同样的位置
        initial_positions = [
            [0.5, 0],     # robot 0 (对应原代码 x_hat1, y_hat1)
            [0.5, 1],     # robot 1 (对应原代码 x_hat2, y_hat2)
            [0, 0.5],     # robot 2 (对应原代码 x_hat3, y_hat3)
            [0, -0.5],    # robot 3 (对应原代码 x_hat4, y_hat4)
            [0, -1]       # robot 4 (对应原代码 x_hat5, y_hat5)
        ]
        self.x_hat = initial_positions[self.robot_id][0]  
        self.y_hat = initial_positions[self.robot_id][1]  
        self.theta_hat = 0  # 规划的航向角
        
        # 初始化参考轨迹x和y方向坐标，用于保存理想轨迹，计算跟踪误差，感觉也有点多余
        # self.xr = 0
        self.xr = self.x_hat
        # self.yr = 0
        self.yr = self.y_hat
        # self.thetar = 0  # 参考航向角
        self.thetar = self.theta_hat

        # # 初始化当前位置（仿真）
        # self.xc = 0
        # self.xc = self.xr
        # self.yc = 0
        # self.yc = self.yr

        # 初始化当前位置（纯仿真：与参考相同起点）
        self.xc = self.xr
        self.yc = self.yr
        self.thetac = 0  # 真实航向角

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
        
        # 领导者状态初始化
        self.leader_state = {
            "trajectory_time": 0.0,
            "x0": 0.3,
            "y0": 0.0,
            "u0": np.zeros(2),
            "theta0": 0.0,
        }
        
        # # 存储所有机器人zx偏差（0-4）
        # self.all_robot_states = {i: {"zx0": 0.0, "zx1": 0.0} for i in range(5)}  # 统一使用字典格式

        # # 初始化邻居状态为空列表
        # self.neighbor_states = []
        
        # 🚀 观测器相关参数初始化
        self.ob_eta = 0.6  # 观测器增益参数1
        self.ob_alp = 0.8  # 观测器增益参数2
        
        # 🚀 观测器状态变量初始化
        self.zxeo = np.zeros((2, 1))  # 当前机器人对领导者状态的观测估计
        self.dzxeo = np.zeros((2, 1))  # 观测状态导数
        
        # 🚀 存储所有机器人的观测器状态（用于计算邻居观测器项）
        self.all_robot_observer_states = {i: {"zxeo": np.zeros(2), "dzxeo": np.zeros(2)} for i in range(5)}

        # 初始化邻居观测器状态为空列表
        self.neighbor_observer_states = []


        # 调试相关变量
        self.debug_counter = 0  # 用于控制调试输出频率
        self.debug_interval = 10  # 每10个控制周期输出一次详细调试信息

    # 纯仿真：外部可直接设置 self.xc, self.yc, self.thetac
        
    # def all_robot_state_callback(self, msg, robot_id):
    #     """更新所有机器人的状态缓存，包含时间戳"""
    #     if len(msg.data) >= 2:
    #         # 存储状态时使用领导者相对时间作为时间戳
    #         self.all_robot_states[robot_id] = {
    #             "zx0": msg.data[0],
    #             "zx1": msg.data[1]
    #         }
            
    #         # 🔍 调试：记录邻居状态接收（只在启动初期或出现异常时输出）
    #         if self.leader_time < 0.5 or (robot_id in self.neighbor_ids and hasattr(self, 'debug_counter')):
    #             is_neighbor = robot_id in self.neighbor_ids
    #             if is_neighbor and robot_id != self.robot_id:
    #                 rospy.logdebug(f"📨 tb3_{self.robot_id} 接收到邻居{robot_id}状态: [{msg.data[0]:.4f}, {msg.data[1]:.4f}]")
    #             elif robot_id == self.robot_id:
    #                 rospy.logdebug(f"🔄 tb3_{self.robot_id} 接收到自身状态回环: [{msg.data[0]:.4f}, {msg.data[1]:.4f}]")

    def set_all_robot_observer_states(self, external_states):
        """外部设置所有机器人的观测器状态: {robot_id: {"zxeo": np.array(2,), "dzxeo": np.array(2,)}}"""
        for rid, val in external_states.items():
            self.all_robot_observer_states[rid] = {
                "zxeo": np.array(val["zxeo"]).reshape(2),
                "dzxeo": np.array(val["dzxeo"]).reshape(2),
            }



    # def get_neighbor_states(self):
    #     """根据预计算的邻居ID直接获取邻居状态，高效简洁"""
    #     return [self.all_robot_states[n_id] for n_id in self.neighbor_ids]       

    def get_neighbor_observer_states(self):
        """根据预计算的邻居ID直接获取邻居观测器状态，高效简洁"""
        return [self.all_robot_observer_states[n_id] for n_id in self.neighbor_ids] 

    # def debug_neighbor_info_timeliness(self):
    #     """简化的邻居信息检查"""
    #     self.debug_counter += 1
        
    #     # 检查预期邻居数量与实际接收数量
    #     expected_count = len(self.neighbor_ids)
    #     actual_count = len(self.neighbor_states)
        
    #     # 只在有问题时输出警告
    #     if actual_count < expected_count:
    #         missing_neighbors = [n_id for n_id in self.neighbor_ids 
    #                            if n_id >= len(self.neighbor_states) or 
    #                            (self.all_robot_states[n_id]["zx0"] == 0.0 and self.all_robot_states[n_id]["zx1"] == 0.0)]
    #         rospy.logwarn(f"tb3_{self.robot_id} 邻居数据不完整: 预期{expected_count}, 实际{actual_count}, 缺失{missing_neighbors}")
        
    #     # 检查数据新鲜度（只在有过时数据时警告）
    #     stale_neighbors = [neighbor_id for neighbor_id in self.neighbor_ids
    #                      if self.all_robot_states[neighbor_id]["zx0"] == 0.0 and 
    #                         self.all_robot_states[neighbor_id]["zx1"] == 0.0]
        
    #     if stale_neighbors:
    #         rospy.logwarn(f"tb3_{self.robot_id} 可能过时的邻居数据: {stale_neighbors}")

    def debug_neighbor_observer_info_timeliness(self):
        """简化的邻居观测器信息检查"""
        self.debug_counter += 1
        
        # 检查预期邻居数量与实际接收数量
        expected_count = len(self.neighbor_ids)
        actual_count = len(self.neighbor_observer_states)

        
        # 只在有问题时输出警告
        if actual_count < expected_count:
            missing_neighbors = [n_id for n_id in self.neighbor_ids
                               if n_id >= len(self.neighbor_observer_states) or
                               (np.array_equal(self.all_robot_observer_states[n_id]["zxeo"], np.zeros(2)) and 
                                np.array_equal(self.all_robot_observer_states[n_id]["dzxeo"], np.zeros(2)))]
            print(f"[WARN] tb3_{self.robot_id} 邻居数据不完整: 预期{expected_count}, 实际{actual_count}, 缺失{missing_neighbors}")
        

        # 检查数据新鲜度（只在有过时数据时警告，第一次循环不报警告）
        if self.debug_counter > 0:
            observer_stale_neighbors = [neighbor_id for neighbor_id in self.neighbor_ids
                             if np.array_equal(self.all_robot_observer_states[neighbor_id]["zxeo"], np.zeros(2)) and
                                np.array_equal(self.all_robot_observer_states[neighbor_id]["dzxeo"], np.zeros(2))]

            # if observer_stale_neighbors:
            #     rospy.logwarn(f"tb3_{self.robot_id} 可能过时的邻居数据: {observer_stale_neighbors}")


    def set_leader_state(self, t, x0, y0, u0x, u0y, theta0):
        """外部设置领导者状态（纯仿真）"""
        self.leader_state = {
            "trajectory_time": float(t),
            "x0": float(x0),
            "y0": float(y0),
            "u0": np.array([float(u0x), float(u0y)]),
            "theta0": float(theta0),
        }
    
    def control_step_once(self, local_time):
        """纯仿真单步控制：调用前请先设置 leader_state 与邻居观测器"""
        self.local_time = local_time
        self.update_formation_offset_local()
        self.execute_control_step(leader_time=self.leader_state["trajectory_time"])
    
    def update_formation_offset_local(self):
        """使用统一的本地时间更新编队偏移"""
        self.px = self.bb * 0.5 * np.cos(self.aa * self.local_time + self.robot_id * 2 * np.pi / self.Rnum)
        self.py = self.bb * 0.5 * np.sin(self.aa * self.local_time + self.robot_id * 2 * np.pi / self.Rnum)
    
    # 纯仿真无需匹配缓存领导者数据
        
    # 纯仿真无需ROS关机流程
        
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

    ### 控制核心函数
    # def update_formation_offset(self):
    #     """更新预测状态（使用领导者时间确保时钟同步）"""
    #     self.px = self.bb * 0.5 * np.cos(self.aa * self.leader_time + self.robot_id * 2 * np.pi / self.Rnum)
    #     self.py = self.bb * 0.5 * np.sin(self.aa * self.leader_time + self.robot_id * 2 * np.pi / self.Rnum)

    def update_formation_offset(self):
        """更新预测状态（使用领导者时间确保时钟同步）"""
        self.px = self.bb * 0.5 * np.cos(self.aa * self.leader_time + self.robot_id * 2 * np.pi / self.Rnum)
        self.py = self.bb * 0.5 * np.sin(self.aa * self.leader_time + self.robot_id * 2 * np.pi / self.Rnum)

        # 计算相对偏差（与邻居节点期望的格式一致）
        self.zx = np.array([self.x_hat - self.px, self.y_hat - self.py]).reshape(-1, 1)

    # def publish_own_zx_state(self):
    #     """发布自身状态供邻居通信节点使用"""
    #     # 检查节点是否正在关闭
    #     if self.is_shutting_down:
    #         return  # 如果正在关闭，不发布状态
        
    #     # 🚀 修复: 检查发布器是否已初始化
    #     if not hasattr(self, 'state_pub'):
    #         rospy.logwarn(f"tb3_{self.robot_id} 状态发布器尚未初始化，跳过发布")
    #         return
            
    #     # 计算相对偏差（与邻居节点期望的格式一致）
    #     self.zx = np.array([self.x_hat - self.px, self.y_hat - self.py]).reshape(-1, 1)

    #     # 发布状态消息
    #     state_msg = Float64MultiArray()
    #     state_msg.data = [self.zx[0, 0], self.zx[1, 0]]
        
    #     # 安全发布状态（检查发布器是否仍然有效）
    #     try:
    #         self.state_pub.publish(state_msg)
    #     except Exception as e:
    #         rospy.logwarn(f"tb3_{self.robot_id} 发布状态时出错：{e}")

    



    # 纯仿真：无需话题发布观测器状态


    # def compute_consensus_error(self):
    #     """计算一致性误差"""
        
    #     # 🚀 优化: 直接使用邻居状态求和，避免重复列表推导
    #     if self.neighbor_states:
    #         # 计算邻居状态的求和（一致性控制理论要求）
    #         neighbor_zx = np.sum([np.array([n["zx0"], n["zx1"]]) 
    #                               for n in self.neighbor_states], axis=0).reshape(-1, 1)
    #     else:
    #         neighbor_zx = np.zeros((2, 1))  # 如果没有邻居，使用零向量

    #     self.ex = self.Fx @ self.zx - neighbor_zx - self.leader_direct * np.array([self.leader_state["x0"], self.leader_state["y0"]]).reshape(-1, 1)
    #     self.fx = self.ex - self.t1 * np.array([self.leader_state["u0"]]).reshape(-1, 1)


    def compute_consensus_error(self):
        """计算基于观测器的一致性误差"""
        
        # 🚀 优化: 直接使用邻居状态求和，避免重复列表推导
        if self.all_robot_observer_states:
            # 计算观测器更新需要的邻居项
            sum_dzxeo_j = np.zeros((2, 1))
            sum_consensus_error_zxeo = np.zeros((2, 1))
            
            # 基于邻接矩阵A计算邻居观测器状态的影响
            for neighbor_id in self.neighbor_ids:
                if neighbor_id in self.all_robot_observer_states:
                    neighbor_zxeo = self.all_robot_observer_states[neighbor_id]["zxeo"].reshape(2, 1)
                    neighbor_dzxeo = self.all_robot_observer_states[neighbor_id]["dzxeo"].reshape(2, 1)
                    
                    # 🔍 前5个时间步打印使用的邻居观测器数据(与纯仿真一致的位置)
                    # if self.debug_counter < 4:
                    #     print(f"[时间步{self.debug_counter-1}] Robot {self.robot_id} 使用邻居 {neighbor_id} 的观测器数据: "
                    #                 f"zxeo=[{neighbor_zxeo[0,0]:.6f}, {neighbor_zxeo[1,0]:.6f}], "
                    #                 f"dzxeo=[{neighbor_dzxeo[0,0]:.6f}, {neighbor_dzxeo[1,0]:.6f}]")
                    
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
        
        #正确是先更新再计算误差
        # 计算误差：使用观测器估计的领导者状态而不是实际领导者状态
        self.ex = self.zx - self.zxeo
        
        # 观测器状态积分更新
        self.zxeo = self.zxeo + self.dzxeo * self.t1
        
        # if self.debug_counter < 4:
        #     print(f"[时间步{self.debug_counter-1}] Robot {self.robot_id} 计算结果: sum_dzxeo_j=[{sum_dzxeo_j[0,0]:.10f}, {sum_dzxeo_j[1,0]:.10f}], "
        #           f"SS=[{SS[0,0]:.10f}, {SS[1,0]:.10f}], "
        #           f"dzxeo=[{self.dzxeo[0,0]:.10f}, {self.dzxeo[1,0]:.10f}],"
        #           f"self.zxeo=[{self.zxeo[0,0]:.10f}, {self.zxeo[1,0]:.10f}],")
        

        # 动态反馈项：考虑观测器动态
        self.fx = self.ex - self.t1 * self.dzxeo

        if self.debug_counter < 4:
            print(f"[时间步{self.debug_counter-1}] Robot {self.robot_id} zx=[{self.zx[0,0]:.10f}, {self.zx[1,0]:.10f}],"
                   f" 误差计算: ex=[{self.ex[0,0]:.10f}, {self.ex[1,0]:.10f}], "
                  f"fx=[{self.fx[0,0]:.10f}, {self.fx[1,0]:.10f}]")

    def compute_solver_planner(self):
        """pdnn控制算法计算"""
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

        if self.debug_counter < 4:
            print(f"[时间步{self.debug_counter-1}] Robot {self.robot_id} G矩阵:\n{G}")
            print(f"[时间步{self.debug_counter-1}] Robot {self.robot_id} Q矩阵:\n{self.Q}")
            print(f"[时间步{self.debug_counter-1}] Robot {self.robot_id} tildrg:\n{tildrg}")
            print(f"[时间步{self.debug_counter-1}] Robot {self.robot_id} tildrf:\n{tildrf}")
            print(f"[时间步{self.debug_counter-1}] Robot {self.robot_id} tildrI:\n{tildrI}")
            print(f"[时间步{self.debug_counter-1}] Robot {self.robot_id} Irnn:\n{Irnn}")
                
        # 计算二次规划问题的矩阵W、C1和E
        W = 2 * (G.T @ self.Q @ G + self.R)
        C1 = 2 * G.T @ self.Q @ (tildrg + tildrf)
        E = np.vstack((-tildrI, tildrI, -G, G, Irnn))

        if self.debug_counter < 4:
            print(f"[时间步{self.debug_counter-1}] Robot {self.robot_id} abarUmin1:\n{self.abarUmin1.flatten()}")
            print(f"[时间步{self.debug_counter-1}] Robot {self.robot_id} abaru:\n{self.abaru.flatten()}")

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

        if self.debug_counter < 4:
            print(f"[时间步{self.debug_counter-1}] Robot {self.robot_id} W矩阵:\n{W.flatten()}")
            print(f"[时间步{self.debug_counter-1}] Robot {self.robot_id} C1矩阵:\n{C1.flatten()}")
            print(f"[时间步{self.debug_counter-1}] Robot {self.robot_id} E矩阵:\n{E.flatten()}")
            print(f"[时间步{self.debug_counter-1}] Robot {self.robot_id} b1向量:\n{b1.flatten()}")
            print(f"[时间步{self.debug_counter-1}] Robot {self.robot_id} Pinfty向量:\n{Pinfty.flatten()}")

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
        # 🔧 修复：使用拷贝避免内存共享，保护GPNN状态变量
        self.y0x = dot_y1.ravel().copy()  # 独立拷贝
        a = self.y0x

        self.detabarU = a[0:2*self.Nu]
        dd = self.detabarU
        # 🔧 修复：abaru使用拷贝保持原始GPNN输出，避免被限幅操作影响
        self.abaru = self.detabarU.copy()  # 独立拷贝，保持GPNN原始输出
        self.u = dd[0:2].copy()  # 独立拷贝，避免影响detabarU

         # 打印前五个时间步的u值（debug_counter在调用此函数前已被递增）
        if self.debug_counter <= 3:
            print(f"Robot {self.robot_id} - 时间步 {self.debug_counter - 1}: detabarU = [{self.detabarU[0]:.6f}, {self.detabarU[1]:.6f},{self.detabarU[2]:.6f}, {self.detabarU[3]:.6f}]")
            print(f"Robot {self.robot_id} - 时间步 {self.debug_counter - 1}: abaru = [{self.abaru[0]:.6f}, {self.abaru[1]:.6f},{self.abaru[2]:.6f}, {self.abaru[3]:.6f}]")
            print(f"Robot {self.robot_id} - 时间步 {self.debug_counter - 1}: u(限幅前) = [{self.u[0]:.6f}, {self.u[1]:.6f}]")

        

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
            
        # 🔍 调试：显示限幅后的结果和验证内存独立性
        if self.debug_counter <= 3:
            print(f"Robot {self.robot_id} - 时间步 {self.debug_counter - 1}: u(限幅后) = [{self.u[0]:.6f}, {self.u[1]:.6f}]")
            print(f"Robot {self.robot_id} - 时间步 {self.debug_counter - 1}: abaru(验证不变) = [{self.abaru[0]:.6f}, {self.abaru[1]:.6f},{self.abaru[2]:.6f}, {self.abaru[3]:.6f}]")
            print(f"Robot {self.robot_id} - 时间步 {self.debug_counter - 1}: detabarU(验证不变) = [{self.detabarU[0]:.6f}, {self.detabarU[1]:.6f},{self.detabarU[2]:.6f}, {self.detabarU[3]:.6f}]")
            
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
        # 🔧 修复：使用拷贝避免内存共享，保护GPNN状态变量
        self.y0z = dot_y1z.reshape(-1).copy()  # 独立拷贝
        az = self.y0z

        detabarUz = az[0:2*self.Nu]
        ddz = detabarUz
        # 🔧 修复：abaruz使用拷贝保持原始GPNN输出，避免被限幅操作影响
        self.abaruz = detabarUz.copy()  # 独立拷贝，保持GPNN原始输出用于约束计算
        self.uz = ddz[0:2].copy()  # 独立拷贝，用于限幅而不影响abaruz
        # 打印前5个时间步的轨迹跟踪QP输出（在限幅前）
        if self.debug_counter <= 3:
            print(f"Robot {self.robot_id} - 时间步 {self.debug_counter - 1}: uz(before limit) = [{float(self.uz[0]):.6f}, {float(self.uz[1]):.6f}]")

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

    def save_final_history(self):
        pass
    
    def execute_control_step(self, leader_time=None):
        """执行一次控制计算（纯仿真）"""
        algorithm_start_time = 0.0  # 纯仿真此处不计时
        if leader_time is not None:
            self.leader_time = leader_time
        else:
            self.leader_time = self.leader_state.get("trajectory_time", 0.0)

        # 更新编队偏移量
        self.update_formation_offset()

        # # 更新邻居状态（从全局状态中筛选）
        # self.neighbor_states = self.get_neighbor_states()

        # 更新邻居观测器状态（从全局状态中筛选）
        self.neighbor_observer_states = self.get_neighbor_observer_states()

        # # 简化的邻居信息检查（只在有问题时输出）
        # self.debug_neighbor_info_timeliness()

        # 简化的邻居信息检查（只在有问题时输出）
        self.debug_neighbor_observer_info_timeliness()

        # 计算一致性误差
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
        algorithm_end_time = 0.0
        algorithm_duration = 0.0
                         
        # 纯仿真：不发布指令，由外部主循环更新位姿
    
        # 🔧 计算与仿真代码一致的编队误差（xc - leader_x - px, yc - leader_y - py, thetac - leader_theta）
        formation_error_x = self.xc - self.leader_state["x0"] - self.px
        formation_error_y = self.yc - self.leader_state["y0"] - self.py
        # 🔧 修正：使用角度差计算函数处理角度跨越问题
        formation_error_theta = self.angle_difference_and_velocity(self.leader_state["theta0"], self.thetac)

        # 纯仿真：返回关键指标以便主循环记录
        return {
            "t": float(self.leader_time),
            "xc": float(self.xc),
            "yc": float(self.yc),
            "thetac": float(self.thetac),
            "vc": float(self.vc),
            "wc": float(self.wc),
            "xe": float(formation_error_x),
            "ye": float(formation_error_y),
            "thetae": float(formation_error_theta),
            "xr": float(self.xr),
            "yr": float(self.yr),
        }
     

def default_neighbor_observer_provider(k, robot_id, A):
    """默认邻居观测器提供器：返回全零（用户可替换为真实/记录数据）"""
    states = {}
    for rid in range(A.shape[0]):
        states[rid] = {"zxeo": np.zeros(2), "dzxeo": np.zeros(2)}
    return states


def constant_neighbor_observer_provider_factory(states_dict):
    """
    创建一个常量邻居观测器提供器：始终返回同一份手动指定的数据。
    参数 states_dict 形如：
        { rid: {"zxeo": [x, y], "dzxeo": [dx, dy]} }
    使用：neighbor_provider=constant_neighbor_observer_provider_factory(my_states)
    """
    def _provider(k, robot_id, A):
        # 不依赖 k，始终返回同一份手动数据
        return states_dict
    return _provider


def list_neighbor_observer_provider_factory(states_list):
    """
    创建一个按时间步序列的邻居观测器提供器：
    参数 states_list 为长度为steps的列表，每个元素是 states_dict（同上）。
    超界时自动使用最后一帧。
    使用：neighbor_provider=list_neighbor_observer_provider_factory(my_list)
    """
    def _provider(k, robot_id, A):
        idx = k if k < len(states_list) else len(states_list) - 1
        return states_list[idx]
    return _provider


def two_step_then_zero_provider(k, robot_id, A):
    """
    方法2：仅在前两个时间步提供手动邻居观测器数据；之后返回空（等价于0）。
    这里示例给 id=0 与 id=2 赋值；若当前 robot_id 的邻居不包含这些 id，
    则仅对实际邻居的条目生效（其余条目被忽略）。
    """
    if k == 0:
        return {
            0: {"zxeo": [0.10, -0.05], "dzxeo": [0.00, 0.00]},
            2: {"zxeo": [0.02,  0.03], "dzxeo": [0.00, 0.00]},
        }
    if k == 1:
        return {
            0: {"zxeo": [0.12, -0.04], "dzxeo": [0.00, 0.00]},
            2: {"zxeo": [0.01,  0.02], "dzxeo": [0.00, 0.00]},
        }
    return {}


def get_all_robots_observer_states_list():
    """
    指定“所有机器人”的观测器数据列表（按时间步）。
    - 返回值：长度为 K 的列表，列表每个元素是一个字典，键为 robot_id(0..4)，
      值为 {"zxeo": [x, y], "dzxeo": [dx, dy]}。
    - 你可以直接在此函数中编辑每个时间步、每个机器人的 zxeo/dzxeo 数值。
    - 若某时间步未提供某个 id，则该 id 默认保持 0。
    """
    # 示例：这里给出前两个时间步（k=0,1）为五个机器人分别指定观测器数据，后续时间步请按需扩展
    return [
        {
            0: {"zxeo": [0.00, 0.00], "dzxeo": [0.00, 0.00]},
            1: {"zxeo": [0.00,  0.00], "dzxeo": [0.00, 0.00]},
            2: {"zxeo": [0.00,  0.00], "dzxeo": [0.00, 0.00]},
            3: {"zxeo": [0.00,  0.00], "dzxeo": [0.00, 0.00]},
            4: {"zxeo": [0.00,  0.00], "dzxeo": [0.00, 0.00]},
        },
        {
            0: {"zxeo": [0.0405794844, 0.0096359015], "dzxeo": [0.4057948438, 0.0963590151]},
            1: {"zxeo": [0.00,  0.00], "dzxeo": [0.00, 0.00]},
            2: {"zxeo": [0.00,  0.00], "dzxeo": [0.00, 0.00]},
            3: {"zxeo": [0.00,  0.00], "dzxeo": [0.00, 0.00]},
            4: {"zxeo": [0.00,  0.00], "dzxeo": [0.00, 0.00]},
        },
    ]


def simulate_single_robot(
    robot_id=0,
    total_time=120.0,
    dt=0.1,
    neighbor_provider=default_neighbor_observer_provider,
):
    steps = int(total_time / dt)
    ctrl = TurtleBot3Controller(robot_id)

    # 记录数组
    t_arr = np.zeros(steps + 1)
    xc_arr = np.zeros(steps + 1)
    yc_arr = np.zeros(steps + 1)
    thetac_arr = np.zeros(steps + 1)
    xr_arr = np.zeros(steps + 1)
    yr_arr = np.zeros(steps + 1)
    vc_arr = np.zeros(steps + 1)
    wc_arr = np.zeros(steps + 1)
    ex_arr = np.zeros(steps + 1)
    ey_arr = np.zeros(steps + 1)
    etheta_arr = np.zeros(steps + 1)

    # 初值
    t2 = 0.0
    x0_0 = 0.3
    y0_0 = 0.0

    # 保存初始状态
    t_arr[0] = 0.0
    xc_arr[0] = ctrl.xc
    yc_arr[0] = ctrl.yc
    thetac_arr[0] = ctrl.thetac
    xr_arr[0] = ctrl.xr
    yr_arr[0] = ctrl.yr

    for k in range(steps):
        # 领导者参考轨迹（与纯仿真一致的简单周期参考）
        x0_curr = x0_0 + 2.5 * np.sin(t2 / 15.0)
        y0_curr = y0_0 + 2.5 * np.sin(t2 / 30.0)
        x0_next = x0_0 + 2.5 * np.sin((t2 + dt) / 15.0)
        y0_next = y0_0 + 2.5 * np.sin((t2 + dt) / 30.0)
        u0x = (x0_next - x0_curr) / dt
        u0y = (y0_next - y0_curr) / dt
        theta0 = np.arctan2(u0y, u0x) if (abs(u0x) + abs(u0y)) > 1e-9 else 0.0

        # 设置领导者状态
        ctrl.set_leader_state(t2 + dt, x0_next, y0_next, u0x, u0y, theta0)

        # 外部邻居观测器（可自定义/替换）
        all_obs = neighbor_provider(k, robot_id, ctrl.A)
        
        # 🔍 调试：打印从provider获取的原始数据
        if k <= 2:  # 只打印前3个时间步
            print(f"[DEBUG k={k}] neighbor_provider返回的机器人0数据: {all_obs.get(0, 'N/A')}")
        
        ctrl.set_all_robot_observer_states(all_obs)
        ctrl.neighbor_observer_states = ctrl.get_neighbor_observer_states()

        # 单步控制
        ctrl.control_step_once(local_time=t2 + dt)
        # 注意：control_step_once 内部已经调用了 execute_control_step，不需要重复调用
        
        # 🔍 获取控制结果（从上一次 execute_control_step 的结果）
        result = {
            "t": float(ctrl.leader_time),
            "xc": float(ctrl.xc),
            "yc": float(ctrl.yc), 
            "thetac": float(ctrl.thetac),
            "vc": float(ctrl.vc),
            "wc": float(ctrl.wc),
            "xe": float(ctrl.xc - ctrl.leader_state["x0"] - ctrl.px),
            "ye": float(ctrl.yc - ctrl.leader_state["y0"] - ctrl.py),
            "thetae": float(ctrl.angle_difference_and_velocity(ctrl.leader_state["theta0"], ctrl.thetac)),
            "xr": float(ctrl.xr),
            "yr": float(ctrl.yr),
        }

        # 用控制输入更新自身位姿（纯仿真）
        ctrl.thetac = ctrl.thetac + dt * ctrl.wc
        # wrap 到 [-pi, pi]
        if ctrl.thetac > np.pi:
            ctrl.thetac -= 2 * np.pi
        elif ctrl.thetac < -np.pi:
            ctrl.thetac += 2 * np.pi
        ctrl.xc = ctrl.xc + ctrl.vc * dt * np.cos(ctrl.thetac)
        ctrl.yc = ctrl.yc + ctrl.vc * dt * np.sin(ctrl.thetac)

        # 记录
        idx = k + 1
        t_arr[idx] = t2 + dt
        xc_arr[idx] = ctrl.xc
        yc_arr[idx] = ctrl.yc
        thetac_arr[idx] = ctrl.thetac
        xr_arr[idx] = ctrl.xr
        yr_arr[idx] = ctrl.yr
        vc_arr[idx] = ctrl.vc
        wc_arr[idx] = ctrl.wc
        ex_arr[idx] = result["xe"]
        ey_arr[idx] = result["ye"]
        etheta_arr[idx] = result["thetae"]

        t2 += dt

    # 简单可视化（轨迹、速度、误差）
    plt.figure(1)
    plt.plot(xc_arr, yc_arr, label=f"tb3_{robot_id}")
    plt.plot(xr_arr, yr_arr, '--', label="ref")
    plt.axis('equal')
    plt.xlabel('X (m)')
    plt.ylabel('Y (m)')
    plt.legend()
    plt.grid(True)

    plt.figure(2)
    plt.plot(t_arr, vc_arr, label='v')
    plt.xlabel('Time (s)')
    plt.ylabel('Linear velocity')
    plt.grid(True)

    plt.figure(3)
    plt.plot(t_arr, wc_arr, label='w')
    plt.xlabel('Time (s)')
    plt.ylabel('Angular velocity')
    plt.grid(True)

    plt.figure(4)
    plt.plot(t_arr, ex_arr, label='x error')
    plt.plot(t_arr, ey_arr, label='y error')
    plt.xlabel('Time (s)')
    plt.ylabel('Formation errors')
    plt.legend()
    plt.grid(True)

    plt.figure(5)
    plt.plot(t_arr, etheta_arr, label='theta error')
    plt.xlabel('Time (s)')
    plt.ylabel('Heading error')
    plt.grid(True)

    plt.show()


if __name__ == "__main__":
    # 可直接修改 robot_id / total_time / dt 或替换 neighbor_provider
    # 使用“所有机器人观测器数据列表”作为 provider：
    _states_list = get_all_robots_observer_states_list()
    _provider = list_neighbor_observer_provider_factory(_states_list)
    # 为保证邻居生效，在当前 A 下推荐 robot_id=1（其邻居包含0）。
    simulate_single_robot(robot_id=0, total_time=120.0, dt=0.1, neighbor_provider=_provider)
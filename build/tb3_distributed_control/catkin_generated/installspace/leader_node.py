#!/usr/bin/env python3
import rospy
import numpy as np
from std_msgs.msg import Float64MultiArray, Bool
from geometry_msgs.msg import Twist, TransformStamped
from tb3_distributed_control.msg import LeaderHistoryData  # 导入自定义消息类型
import tf2_ros

class LeaderNode:
    def __init__(self):
        rospy.init_node("leader_node")
        # 发布领导者状态（使用相对话题名，适配命名空间）
        self.leader_pub = rospy.Publisher("state", Float64MultiArray, queue_size=1)  # 🚀 优化: 最新状态实时性
        
        # 🚀 新增：ROS话题优化版本 - 发布历史数据到专用话题
        self.leader_history_pub = rospy.Publisher("/leader/history", LeaderHistoryData, queue_size=1)  # 🚀 优化: 数据新鲜度
        
        # 发布系统停止信号（保持全局话题）
        self.shutdown_pub = rospy.Publisher("/system/shutdown", Bool, queue_size=1)  # 🚀 优化: 停止信号实时性

        # 发布速度指令给真实机器人（可选功能），暂时用不到
        # self.enable_real_robot = rospy.get_param("~enable_real_robot", False)
        # if self.enable_real_robot:
        #     real_robot_name = rospy.get_param("~real_robot_name", "tb3_real")
        #     self.cmd_vel_pub = rospy.Publisher(f"/{real_robot_name}/cmd_vel", Twist, queue_size=1)  # 🚀 优化: 速度指令实时性
        #     rospy.loginfo(f"启用真实机器人控制，目标: /{real_robot_name}/cmd_vel")

        # 虚拟领导者TF发布器（用于RViz显示机器人模型）
        self.tf_broadcaster = tf2_ros.TransformBroadcaster()
        # 从launch参数获取虚拟领导者命名空间
        self.virtual_leader_ns = rospy.get_param("~virtual_leader_ns", "tb3_virtual_leader")
        rospy.loginfo(f"虚拟领导者TF发布器已启动，将发布到 {self.virtual_leader_ns}/base_footprint")

        self.T = rospy.get_param("~total_time", 30.0)  # 总运行时间，默认30秒，可通过参数配置
        self.trajectory_type = rospy.get_param("~trajectory_type", "eight")  # 轨迹类型：eight(8字形)、circle(圆形)、line(直线)
        self.t1 = 0.1  # 控制周期（作为默认时间间隔，处理异常情况）
        self.shutdown_sent = False  # 标记是否已发送停止信号
        # 添加时间基准变量（相对时间基准）
        self.start_time = None  # 节点实际启动时的ROS仿真时间
        self.current_sim_time = None  # 初始化为None，标记首次调用
        
        self.trajectory_time = 0.0  # 轨迹计算用的相对时间（从0开始）

        # 从launch参数获取虚拟领导者初始位姿
        self.leader_x0 = rospy.get_param("~leader_init_x", -0.3)  # 初始x
        self.leader_y0 = rospy.get_param("~leader_init_y", 0.0)  # 初始y
        self.leader_theta0 = rospy.get_param("~leader_init_yaw", 0.0)  # 初始航向角
        rospy.loginfo(f"虚拟领导者初始位置: x={self.leader_x0}, y={self.leader_y0}, yaw={self.leader_theta0}")

        # 初始化当前时刻的位置和航向角
        self.x0 = self.leader_x0  # 初始x
        self.y0 = self.leader_y0  # 初始y
        self.theta0 = self.leader_theta0  # 初始航向角
        self.u0x = 0.0  # 初始x方向速度
        self.u0y = 0.0  # 初始y方向速度
        self.v0 = 0.0  # 初始线速度
        self.w0 = 0.0  # 初始角速度


        # 初始化下一时刻的的位置和航向角（基于当前状态计算）
        self.x0_next = 0.0  # 初始x
        self.y0_next = 0.0  # 初始y
        self.theta0_next = 0.0  # 初始航向角
        self.u0x_next = 0.0  # 初始x方向速度
        self.u0y_next = 0.0  # 初始y方向速度
        self.v0_next = 0.0  # 初始线速度
        self.w0_next = 0.0  # 初始角速度
        
        # 定时发布（10Hz，与控制周期一致）
        self.timer = rospy.Timer(rospy.Duration(0.1), self.publish_leader_state)
        
        # 打印轨迹信息
        rospy.loginfo(f"领导者节点启动 - 轨迹类型：{self.trajectory_type}，总时长：{self.T}秒")

    def publish_leader_state(self, event):
        """发布领导者轨迹（使用相对时间计算，从0开始）"""
        self.current_sim_time = rospy.get_time()
        
        # 首次调用：记录启动时间基准（仅一次设置）
        if self.start_time is None:
                # 如果是第一次进入定时器回调，则记录当前仿真时间为轨迹的起点时间
            self.start_time = self.current_sim_time
            rospy.loginfo(f"领导者节点启动，时间基准设为: {self.start_time:.3f}s")

        # 计算轨迹用的相对时间（从0开始，随时间累积）
        self.trajectory_time = self.current_sim_time - self.start_time

        # ⏹️ 检查是否达到停止时间（在发布之前检查，避免发送t=T的数据）
        if self.trajectory_time >= self.T and not self.shutdown_sent:
            rospy.loginfo(f"达到设定总时长 {self.T}s，停止轨迹发布")
            self.shutdown_sent = True
            
            # 等待一个控制周期，确保最后数据被机器人接收
            rospy.sleep(self.t1)
            
            # 发送停止信号给所有节点
            shutdown_msg = Bool()
            shutdown_msg.data = True
            self.shutdown_pub.publish(shutdown_msg)
            
            # 给其他节点时间接收停止信号并保存数据
            rospy.loginfo("等待其他节点完成数据保存...")
            rospy.sleep(0.5)
            
            # 停止自己
            rospy.signal_shutdown(f"轨迹总时间：{self.trajectory_time:.2f}s，领导者轨迹生成任务完成，系统正常停止")
            return

        # 🚀 ROS话题优化：发布历史数据到专用话题（替代参数服务器）
        leader_history_msg = LeaderHistoryData()
        leader_history_msg.trajectory_time = float(self.trajectory_time)
        leader_history_msg.ros_timestamp = float(self.current_sim_time)
        leader_history_msg.x0 = float(self.x0)
        leader_history_msg.y0 = float(self.y0)
        leader_history_msg.theta0 = float(self.theta0)
        leader_history_msg.v0 = float(self.v0)
        leader_history_msg.w0 = float(self.w0)
        leader_history_msg.u0x = float(self.u0x)
        leader_history_msg.u0y = float(self.u0y)
        self.leader_history_pub.publish(leader_history_msg)

        t_calc = self.trajectory_time + self.t1  # 计算下一时刻即k+1时刻

        ###  编队队形选择 ###
        if self.trajectory_type == "eight_slow_slow_slow": 
            #①8字形轨迹 - 慢速版本（虚拟者线速度在0.04652——0.14947）
            self.x0_next = self.leader_x0 + 2.5 * np.sin((t_calc) / 18.7)  
            self.y0_next = self.leader_y0 + 2.5 * np.sin((t_calc) / 37.4)  

            self.u0x_next = 2.5 * np.cos(t_calc / 18.7) * (1.0 / 18.7)  # dx/dt = 0.2 * cos(t/18.7)
            self.u0y_next = 2.5 * np.cos(t_calc / 37.4) * (1.0 / 37.4)  # dy/dt = 0.1 * cos(t/37.4)

            ax_next = -2.5 * np.sin(t_calc / 18.7) * (1.0 / 18.7) * (1.0 / 18.7)  # d²x/dt² = -0.2/18.7 * sin(t/18.7)
            ay_next = -2.5 * np.sin(t_calc / 37.4) * (1.0 / 37.4) * (1.0 / 37.4)  # d²y/dt² = -0.1/37.4 * sin(t/37.4)

        elif self.trajectory_type == "eight_slow_slow":
            #①8字形轨迹 - 慢速版本（虚拟者线速度在0.057998——0.186339）
            self.x0_next = self.leader_x0 + 2.5 * np.sin((t_calc) / 15)  
            self.y0_next = self.leader_y0 + 2.5 * np.sin((t_calc) / 30)  

            self.u0x_next = 2.5 * np.cos(t_calc / 15) * (1.0 / 15)  # dx/dt = 0.2 * cos(t/15)
            self.u0y_next = 2.5 * np.cos(t_calc / 30) * (1.0 / 30)  # dy/dt = 0.1 * cos(t/30)

            ax_next = -2.5 * np.sin(t_calc / 15) * (1.0 / 15) * (1.0 / 15)  # d²x/dt² = -0.2/15 * sin(t/15)
            ay_next = -2.5 * np.sin(t_calc / 30) * (1.0 / 30) * (1.0 / 30)  # d²y/dt² = -0.1/30 * sin(t/30)


        elif self.trajectory_type == "eight_slow":
            #①8字形轨迹 - 慢速版本（虚拟者线速度在0.069597——0.223607）
            self.x0_next = self.leader_x0 + 2.5 * np.sin((t_calc) / 12.5)  
            self.y0_next = self.leader_y0 + 2.5 * np.sin((t_calc) / 25)  

            self.u0x_next = 2.5 * np.cos(t_calc / 12.5) * (1.0 / 12.5)  # dx/dt = 0.2 * cos(t/12.5)
            self.u0y_next = 2.5 * np.cos(t_calc / 25) * (1.0 / 25)  # dy/dt = 0.1 * cos(t/25)

            ax_next = -2.5 * np.sin(t_calc / 12.5) * (1.0 / 12.5) * (1.0 / 12.5)  # d²x/dt² = -0.2/12.5 * sin(t/12.5)
            ay_next = -2.5 * np.sin(t_calc / 25) * (1.0 / 25) * (1.0 / 25)  # d²y/dt² = -0.1/25 * sin(t/25)

        elif self.trajectory_type == "eight_fast":
            #①8字形轨迹 - 快速版本（虚拟者线速度在0.086996——0.279508）
            self.x0_next = self.leader_x0 + 2.5 * np.sin((t_calc) / 10)  # 使用相对时间计算轨迹
            self.y0_next = self.leader_y0 + 2.5 * np.sin((t_calc) / 20)

            self.u0x_next = 2.5 * np.cos(t_calc / 10) * (1.0 / 10)  # dx/dt = 0.25 * cos(t/10)
            self.u0y_next = 2.5 * np.cos(t_calc / 20) * (1.0 / 20)  # dy/dt = 0.125 * cos(t/20)
            
            ax_next = -2.5 * np.sin(t_calc / 10) * (1.0 / 10) * (1.0 / 10)  # d²x/dt² = -0.025 * sin(t/10)
            ay_next = -2.5 * np.sin(t_calc / 20) * (1.0 / 20) * (1.0 / 20)  # d²y/dt² = -0.00625 * sin(t/20)

        elif self.trajectory_type == "circle":
            #②圆形轨迹
            # 圆形轨迹：以leader_x0, leader_y0为圆心，半径1.2m，角速度0.15 rad/s
            radius = 0.75  # 圆形半径(m)
            angular_velocity = 0.15  # 角速度(rad/s)，线速度 = 半径 × 角速度 = 1.2 × 0.15 = 0.18 m/s

            self.x0_next = self.leader_x0 + radius * np.cos(angular_velocity * t_calc)
            self.y0_next = self.leader_y0 + radius * np.sin(angular_velocity * t_calc)
            
            # 圆形轨迹解析速度（切线方向）
            self.u0x_next = -radius * angular_velocity * np.sin(angular_velocity * t_calc)  # dx/dt
            self.u0y_next = radius * angular_velocity * np.cos(angular_velocity * t_calc)   # dy/dt
            
            # 圆形轨迹解析加速度（向心方向）
            ax_next = -radius * angular_velocity**2 * np.cos(angular_velocity * t_calc)  # d²x/dt²
            ay_next = -radius * angular_velocity**2 * np.sin(angular_velocity * t_calc)  # d²y/dt²

        elif self.trajectory_type == "line":
            #③直线轨迹
            # 直线轨迹：从起点开始沿x轴正方向运动，速度0.15 m/s
            linear_velocity = 0.15  # 直线速度(m/s)
            
            self.x0_next = self.leader_x0 + linear_velocity * t_calc  # 沿x轴匀速运动
            self.y0_next = self.leader_y0  # y坐标保持不变
            
            # 直线轨迹解析速度（恒定）
            self.u0x_next = linear_velocity  # dx/dt = 常数
            self.u0y_next = 0.0              # dy/dt = 0
            
            # 直线轨迹解析加速度（为零）
            ax_next = 0.0  # d²x/dt² = 0
            ay_next = 0.0  # d²y/dt² = 0
            
        elif self.trajectory_type == "real_experiment_trajectory":
            # ④ 实验轨迹 - 使用launch参数中的初始位置
            # 轨迹参数
            start_x = self.leader_x0   # 使用launch参数中的起点x坐标
            start_y = self.leader_y0   # 使用launch参数中的起点y坐标
            radius = 0.75   # 半圆半径0.75m
            v_avg = 0.15    # 半圆平均速度0.15 m/s
            
            # 各段距离
            dist1 = 2.55 - 0.3  # 段1：垂直上升 2.25m
            arc_length = np.pi * radius  # 半圆弧长
            dist3 = 2.55 - 1.25  # 段3：垂直下降 1.3m
            dist5 = 3.3 - 1.25   # 段5：垂直上升 2.05m
            
            # 各段时间
            t1_duration = dist1 / v_avg
            t2_duration = arc_length / v_avg
            t3_duration = dist3 / v_avg
            t4_duration = arc_length / v_avg
            t5_duration = dist5 / v_avg
            
            # 时间节点
            T1 = t1_duration
            T2 = T1 + t2_duration
            T3 = T2 + t3_duration
            T4 = T3 + t4_duration
            T5 = T4 + t5_duration
            
            if t_calc <= T1:
                # 段1：垂直上升，从(0.0, 0.3)到(0, 2.55)
                progress = t_calc / T1
                self.x0_next = start_x
                self.y0_next = start_y + dist1 * progress
                self.u0x_next = 0.0
                self.u0y_next = v_avg
                self.w0_next = 0.0
                ax_next = 0.0
                ay_next = 0.0
                
            elif t_calc <= T2:
                # 段2：顶部半圆，圆心(0.75, 2.55)，从左(π)到右(0)
                t_seg = t_calc - T1
                duration = T2 - T1
                progress = t_seg / duration
                
                # 速度变化：v = 0.15 - 0.03*sin(2πp)
                s = 0.15 * t_seg + 0.03 * duration * (np.cos(2 * np.pi * progress) - 1) / (2 * np.pi)
                angle = np.pi - s / radius
                
                self.x0_next = 0.75 + radius * np.cos(angle)
                self.y0_next = 2.55 + radius * np.sin(angle)
                
                # 速度（切向）
                v_instant = v_avg - 0.03 * np.sin(2 * np.pi * progress)
                self.u0x_next = v_instant * np.sin(angle)  # 顺时针切向
                self.u0y_next = -v_instant * np.cos(angle)
                self.w0_next = -v_instant / radius  # 顺时针为负
                
                ax_next = -radius * self.w0_next**2 * np.cos(angle)
                ay_next = -radius * self.w0_next**2 * np.sin(angle)
                
            elif t_calc <= T3:
                # 段3：垂直下降，从(1.5, 2.55)到(1.5, 1.25)
                progress = (t_calc - T2) / (T3 - T2)
                self.x0_next = 1.5
                self.y0_next = 2.55 - dist3 * progress
                self.u0x_next = 0.0
                self.u0y_next = -v_avg
                self.w0_next = 0.0
                ax_next = 0.0
                ay_next = 0.0
                
            elif t_calc <= T4:
                # 段4：底部半圆，圆心(2.25, 1.25)，从左(π)到右(2π)
                t_seg = t_calc - T3
                duration = T4 - T3
                progress = t_seg / duration
                
                # 速度变化：v = 0.15 + 0.03*sin(2πp)
                s = 0.15 * t_seg - 0.03 * duration * (np.cos(2 * np.pi * progress) - 1) / (2 * np.pi)
                angle = np.pi + s / radius
                
                self.x0_next = 2.25 + radius * np.cos(angle)
                self.y0_next = 1.25 + radius * np.sin(angle)
                
                # 速度（切向）
                v_instant = v_avg + 0.03 * np.sin(2 * np.pi * progress)
                self.u0x_next = -v_instant * np.sin(angle)  # 逆时针切向（负sin）
                self.u0y_next = v_instant * np.cos(angle)   # 逆时针切向（正cos）
                self.w0_next = v_instant / radius  # 逆时针为正
                
                ax_next = -radius * self.w0_next**2 * np.cos(angle)
                ay_next = -radius * self.w0_next**2 * np.sin(angle)
                
            else:
                # 段5：垂直上升，从(3.0, 1.25)到(3.0, 3.3)
                progress = (t_calc - T4) / (T5 - T4)
                self.x0_next = 3.0
                self.y0_next = 1.25 + dist5 * progress
                self.u0x_next = 0.0
                self.u0y_next = v_avg
                self.w0_next = 0.0
                ax_next = 0.0
                ay_next = 0.0
                
        elif self.trajectory_type == "real_experiment_trajectory_line":
            # ④ 实验轨迹_直线：从起点到(3.2, 3.5)的斜向直线
            # 起点使用launch参数，终点为(3.2, 3.5)
            start_x = self.leader_x0   # 使用launch参数中的起点x坐标
            start_y = self.leader_y0   # 使用launch参数中的起点y坐标
            end_x = 3.2
            end_y = 3.5
            
            # 计算方向向量和距离
            dx = end_x - start_x  # 3.2
            dy = end_y - start_y  # 3.2
            total_distance = np.sqrt(dx**2 + dy**2)  # ≈ 4.52
            
            # 直线速度(m/s)
            linear_velocity = 0.15
            
            # 单位方向向量
            dir_x = dx / total_distance  # ≈ 0.707
            dir_y = dy / total_distance  # ≈ 0.707
            
            # 当前运动距离
            traveled_distance = linear_velocity * t_calc
            
            # 限制在轨迹范围内
            if traveled_distance <= total_distance:
                self.x0_next = start_x + dir_x * traveled_distance
                self.y0_next = start_y + dir_y * traveled_distance
            else:
                # 到达终点后保持静止
                self.x0_next = end_x
                self.y0_next = end_y
            
            # 速度分量（恒定）
            self.u0x_next = linear_velocity * dir_x
            self.u0y_next = linear_velocity * dir_y
            
            # 加速度为零（匀速直线运动）
            ax_next = 0.0
            ay_next = 0.0

        elif self.trajectory_type == "real_experiment_trajectory_line_improve":
            # ④ 实验轨迹_直线：从起点到(3.2, 3.5)的斜向直线
            # 起点使用launch参数，终点为(3.2, 3.5)
            start_x = self.leader_x0   # 使用launch参数中的起点x坐标
            start_y = self.leader_y0   # 使用launch参数中的起点y坐标
            end_x = 4.5
            end_y = 0.0
            
            # 计算方向向量和距离
            dx = end_x - start_x  # 3.2
            dy = end_y - start_y  # 3.2
            total_distance = np.sqrt(dx**2 + dy**2)  # ≈ 4.52
            
            # 直线速度(m/s)
            linear_velocity = 0.15
            
            # 单位方向向量
            dir_x = dx / total_distance  # ≈ 0.707
            dir_y = dy / total_distance  # ≈ 0.707
            
            # 当前运动距离
            traveled_distance = linear_velocity * t_calc
            
            # 限制在轨迹范围内
            if traveled_distance <= total_distance:
                self.x0_next = start_x + dir_x * traveled_distance
                self.y0_next = start_y + dir_y * traveled_distance
            else:
                # 到达终点后保持静止
                self.x0_next = end_x
                self.y0_next = end_y
            
            # 速度分量（恒定）
            self.u0x_next = linear_velocity * dir_x
            self.u0y_next = linear_velocity * dir_y
            
            # 加速度为零（匀速直线运动）
            ax_next = 0.0
            ay_next = 0.0
            
        elif self.trajectory_type == "real_circle_s_trajectory":
            # ⑤ S形双半圆轨迹（合并自real_experiment_trajectory的两个半圆段）
            # 原轨迹时间段：顶部半圆约15-31秒，底部半圆约39-55秒
            # 起点：使用launch参数中的初始位置(self.leader_x0, self.leader_y0)
            # 轨迹描述：先顺时针走上半圆，再逆时针走下半圆，形成S形
            
            start_x = self.leader_x0   # 起点x坐标
            start_y = self.leader_y0   # 起点y坐标
            radius = 0.75              # 半圆半径0.75m
            v_avg = 0.15               # 平均速度0.15 m/s
            
            # 半圆弧长
            arc_length = np.pi * radius
            
            # 各段时间
            t1_duration = arc_length / v_avg  # 第一个半圆（上半圆）
            t2_duration = arc_length / v_avg  # 第二个半圆（下半圆）
            
            # 时间节点
            T1 = t1_duration
            T2 = T1 + t2_duration
            
            if t_calc <= T1:
                # 第一段：上半圆（顺时针）
                # 圆心：(start_x + radius, start_y)
                # 起始角度：π（左侧），结束角度：0（右侧）
                t_seg = t_calc
                duration = T1
                progress = t_seg / duration
                
                # 速度变化：v = 0.15 - 0.03*sin(2πp)（模拟原轨迹的速度波动）
                s = 0.15 * t_seg + 0.03 * duration * (np.cos(2 * np.pi * progress) - 1) / (2 * np.pi)
                angle = np.pi - s / radius
                
                center_x = start_x + radius
                center_y = start_y
                
                self.x0_next = center_x + radius * np.cos(angle)
                self.y0_next = center_y + radius * np.sin(angle)
                
                # 速度（切向，顺时针）
                v_instant = v_avg - 0.03 * np.sin(2 * np.pi * progress)
                self.u0x_next = v_instant * np.sin(angle)   # 顺时针切向
                self.u0y_next = -v_instant * np.cos(angle)
                self.w0_next = -v_instant / radius  # 顺时针为负
                
                ax_next = -radius * self.w0_next**2 * np.cos(angle)
                ay_next = -radius * self.w0_next**2 * np.sin(angle)
                
            else:
                # 第二段：下半圆（逆时针）
                # 圆心：(start_x + 3*radius, start_y)
                # 起始角度：π（左侧），结束角度：2π（右侧）
                t_seg = t_calc - T1
                duration = T2 - T1
                progress = t_seg / duration
                
                # 速度变化：v = 0.15 + 0.03*sin(2πp)（模拟原轨迹的速度波动）
                s = 0.15 * t_seg - 0.03 * duration * (np.cos(2 * np.pi * progress) - 1) / (2 * np.pi)
                angle = np.pi + s / radius
                
                center_x = start_x + 3 * radius
                center_y = start_y
                
                self.x0_next = center_x + radius * np.cos(angle)
                self.y0_next = center_y + radius * np.sin(angle)
                
                # 速度（切向，逆时针）
                v_instant = v_avg + 0.03 * np.sin(2 * np.pi * progress)
                self.u0x_next = -v_instant * np.sin(angle)  # 逆时针切向（负sin）
                self.u0y_next = v_instant * np.cos(angle)   # 逆时针切向（正cos）
                self.w0_next = v_instant / radius  # 逆时针为正
                
                ax_next = -radius * self.w0_next**2 * np.cos(angle)
                ay_next = -radius * self.w0_next**2 * np.sin(angle)
            
        else:
            # 默认使用8字形轨迹（慢速版本）
                # 如果轨迹类型参数不是预设的几种，则自动切换为默认8字形轨迹（慢速版）
            rospy.logwarn(f"未知轨迹类型：{self.trajectory_type}，使用默认8字形轨迹（慢速版本）")
            self.x0_next = self.leader_x0 + 2.5 * np.sin((t_calc) / 12.5)  
            self.y0_next = self.leader_y0 + 2.5 * np.sin((t_calc) / 25)  

            self.u0x_next = 2.5 * np.cos(t_calc / 12.5) * (1.0 / 12.5)
            self.u0y_next = 2.5 * np.cos(t_calc / 25) * (1.0 / 25)

            ax_next = -2.5 * np.sin(t_calc / 12.5) * (1.0 / 12.5) * (1.0 / 12.5)
            ay_next = -2.5 * np.sin(t_calc / 25) * (1.0 / 25) * (1.0 / 25)

        # 领导者航向角（基于解析速度计算）
        self.theta0_next = np.arctan2(self.u0y_next, self.u0x_next)  # 方向角

        # 【修复】针对不同轨迹使用不同的角速度计算方法
        if self.trajectory_type == "real_experiment_trajectory":
            # 实验轨迹：使用几何角速度（已在轨迹函数中设置）
            # 角速度已经在每个段中正确计算，无需重复计算
            pass  # w0_next在轨迹计算中已经设置
        else:
            # 其他轨迹：使用解析公式计算角速度，避免角度差分噪声
            # theta0_next的求导：ω = (vx * ay - vy * ax) / (vx² + vy²)
            v_squared = self.u0x_next**2 + self.u0y_next**2

            if v_squared > 1e-8:  # 避免除零
                # 如果速度平方很小（接近静止），则角速度直接设为0，避免除零错误
                self.w0_next = (self.u0x_next * ay_next - self.u0y_next * ax_next) / v_squared
            else:
                # 否则角速度为0
                self.w0_next = 0.0  # 静止时角速度为0
        
        # 【修复】使用解析速度计算线速度
        self.v0_next = np.sqrt(self.u0x_next**2 + self.u0y_next**2)  # 解析线速度

        # 发布状态用于通信（当前时刻：trajectory_time, 下一时刻的x0, y0, u0x, u0y, theta0）
        # 注意：u0x, u0y 用于通信发布；v0, w0 仅用于历史记录和绘图
        msg = Float64MultiArray()
        # 修改后（转换为原生类型，使用相对时间）
        msg.data = [
            self.trajectory_time,  # 发布相对时间而非ROS仿真时间
            self.x0_next.item() if isinstance(self.x0_next, np.ndarray) else float(self.x0_next),
            self.y0_next.item() if isinstance(self.y0_next, np.ndarray) else float(self.y0_next),
            self.u0x_next.item() if isinstance(self.u0x_next, np.ndarray) else float(self.u0x_next),
            self.u0y_next.item() if isinstance(self.u0y_next, np.ndarray) else float(self.u0y_next),
            self.theta0_next.item() if isinstance(self.theta0_next, np.ndarray) else float(self.theta0_next)
        ]
        
        # 📡 首次发送时记录时间（用于测量网络延迟）
        if self.trajectory_time < 0.01:  # 第一次发送（t≈0）
            rospy.loginfo(f"📤 虚拟领导者首次发送数据: ROS时间={rospy.get_time():.5f}s, 轨迹时间={self.trajectory_time:.5f}s")
        
        self.leader_pub.publish(msg)
        # rospy.loginfo(f"Leader state at 相对时间={self.trajectory_time:.5f}: 下一时刻的x={self.x0_next:.5f}, y={self.y0_next:.5f}, u0x={self.u0x_next:.5f}, u0y={self.u0y_next:.5f}, theta0={self.theta0_next:.5f}, v0={self.v0_next:.5f}, w0={self.w0_next:.5f}")

        # 发布虚拟领导者TF变换（用于RViz显示机器人模型）
        self.publish_virtual_leader_tf()
        
        # 发布速度指令给真实机器人（如果启用）
        # if self.enable_real_robot:
        #     cmd_msg = Twist()
        #     cmd_msg.linear.x = float(self.v0_next)
        #     cmd_msg.angular.z = float(self.w0_next)
        #     self.cmd_vel_pub.publish(cmd_msg)
        
        # 打印调试信息（显示相对时间）
        # debug_info = f"Leader state at 相对时间={self.trajectory_time:.5f}: 下一时刻的x={self.x0_next:.5f}, y={self.y0_next:.5f}, u0x={self.u0x_next:.5f}, u0y={self.u0y_next:.5f}, theta0={self.theta0_next:.5f}, v0={self.v0_next:.5f}, w0={self.w0_next:.5f}"
        # if self.enable_real_robot:
        #     debug_info += f", 真实机器人指令: v={self.v0_next:.3f}, w={self.w0_next:.3f}"
        # rospy.loginfo(debug_info)

        # 更新当前时刻值（用于下一次迭代计算）
        self.x0 = self.x0_next
        self.y0 = self.y0_next
        self.u0x = self.u0x_next
        self.u0y = self.u0y_next
        self.theta0 = self.theta0_next
        self.v0 = self.v0_next
        self.w0 = self.w0_next

    def publish_virtual_leader_tf(self):
        """发布虚拟领导者的TF变换，用于在RViz中显示机器人模型"""
        try:
            # 创建TF变换消息
            transform = TransformStamped()
            
            # 设置时间戳和坐标系（使用动态命名空间）
            transform.header.stamp = rospy.Time.now()
            transform.header.frame_id = f"{self.virtual_leader_ns}/odom"
            transform.child_frame_id = f"{self.virtual_leader_ns}/base_footprint"
            
            # 设置位置（使用当前领导者位置）
            transform.transform.translation.x = float(self.x0_next) if hasattr(self, 'x0_next') else 0.0
            transform.transform.translation.y = float(self.y0_next) if hasattr(self, 'y0_next') else 0.0
            transform.transform.translation.z = 0.0
            
            # 设置姿态（使用当前领导者角度）
            theta = float(self.theta0_next) if hasattr(self, 'theta0_next') else 0.0
            # 将欧拉角转换为四元数
            transform.transform.rotation.x = 0.0
            transform.transform.rotation.y = 0.0
            transform.transform.rotation.z = np.sin(theta / 2.0)
            transform.transform.rotation.w = np.cos(theta / 2.0)
            
            # 发布TF变换
            self.tf_broadcaster.sendTransform(transform)
            
        except Exception as e:
            rospy.logwarn(f"发布虚拟领导者TF变换时出错: {e}")

if __name__ == "__main__":
    try:
        leader = LeaderNode()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
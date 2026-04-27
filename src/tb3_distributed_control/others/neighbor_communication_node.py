#!/usr/bin/env python3
import rospy
import numpy as np
from std_msgs.msg import Float64MultiArray, Bool

class NeighborCommunicator:
    def __init__(self):
        rospy.init_node("neighbor_communication_node")
        
        # 邻接矩阵（适配0-4ID，与原逻辑一致但索引调整）
        # 行索引：当前机器人ID（0-4）
        # 列索引：邻居ID（0-4），1表示是邻居
        self.adj_matrix = np.array([
            [0, 0, 1, 0, 0],  # 机器人0的邻居：2
            [1, 0, 1, 0, 0],  # 机器人1的邻居：0、2
            [0, 0, 0, 1, 0],  # 机器人2的邻居：3
            [1, 0, 0, 0, 0],  # 机器人3的邻居：0
            [0, 1, 0, 0, 0]   # 机器人4的邻居：1
        ])
        
        # 存储所有机器人zx偏差（0-4）
        self.robot_states = {i: [0.0, 0.0] for i in range(5)}  # {id: [x_hat-px, y_hat-py]}
        
        # 订阅所有机器人的状态（tb3_0~4/state）
        for robot_id in range(5):
            rospy.Subscriber(f"/tb3_{robot_id}/state", Float64MultiArray,
                           self.state_callback, callback_args=robot_id)
        
        # 订阅系统停止信号
        rospy.Subscriber("/system/shutdown", Bool, self.shutdown_callback)
        
        # 发布邻居状态的Publisher（/neighbor_0/state ~ /neighbor_4/state）
        self.neighbor_pubs = {
            i: rospy.Publisher(f"/neighbor_{i}/state", Float64MultiArray, queue_size=10)
            for i in range(5)
        }
        
        # 定时转发（与控制周期一致：10Hz）
        self.timer = rospy.Timer(rospy.Duration(0.1), self.forward_neighbor_states)

    def state_callback(self, msg, robot_id):
        """更新机器人状态缓存（保存位置偏差zx）"""
        if len(msg.data) >= 2: # 确保数据长度足够
            self.robot_states[robot_id] = [msg.data[0], msg.data[1]]  # msg.data格式：[x_hat-px, y_hat-py]

    def shutdown_callback(self, msg):
        """接收系统停止信号并优雅关闭"""
        if msg.data:
            rospy.loginfo("邻居通信节点收到系统停止信号，正在关闭...")
            rospy.signal_shutdown("邻居通信节点接收到系统停止信号，正常关闭")

    def forward_neighbor_states(self, event):
        """按邻接矩阵转发邻居状态"""
        for robot_id in range(5):  # 遍历每个机器人（0-4）
            # 获取当前机器人的邻居ID（从邻接矩阵提取）
            neighbor_ids = [i for i, val in enumerate(self.adj_matrix[robot_id]) if val == 1]
            # 收集邻居状态（位置偏差zx）
            neighbor_data = []
            for n_id in neighbor_ids:
                neighbor_data.extend(self.robot_states[n_id])  # 格式：[x_hat-px_n, y_hat-py_n, x_hat-px_m, y_hat-py_m, ...]
            
            msg = Float64MultiArray()
            msg.data = neighbor_data
            self.neighbor_pubs[robot_id].publish(msg)
            # 发布给对应机器人调试信息
            # rospy.loginfo(f"Robot {robot_id} neighbors: {neighbor_ids}, data: {neighbor_data}")


if __name__ == "__main__":
    try:
        comm = NeighborCommunicator()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
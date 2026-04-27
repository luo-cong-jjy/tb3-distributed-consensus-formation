# 🚀 TurtleBot3 分布式一致性编队控制系统（方案总览）

📌 本文件是**方案一级导航页**：只保留最小必要信息。
📚 详细配置、参数、脚本说明请直接查看各功能包 README。

🔎 阅读建议：
- 🟢 先看“当前推荐路线”
- 🟢 再按“最简部署流程”执行
- 🟠 需要导航栈位姿时再看“探索方案”

## 🧭 1. 文档导航

- 📘 详细版总说明：`详细版README.md`
- 🖥️ 主机端控制包说明：`主机端功能包/src/tb3_distributed_control/README.md`
- 🤖 机器人端控制包说明：`机器人端功能包/src/tb3_distributed_control/README.md`
- 🗺️ 机器人端导航定位包说明（进阶）：`机器人端功能包/src/tb3_distributed_location/README.md`

## 🎯 2. 当前推荐路线

- 🟢 **推荐主线**：里程计位姿链路（实时性优先）
- 🟠 **可探索路线**：导航栈位姿链路（AMCL/map）

主机端对应：
- 🟢 里程计推荐：`distributed_host_side.launch`
- 🟠 导航探索：`distributed_host_side_nav_location.launch`

## ▶️ 3. 最简部署流程（里程计推荐）

1. ✅ 主机与机器人均完成编译并 `source devel/setup.bash`
2. ✅ 主机启动：

```bash
roscore
```

3. ✅ 每台机器人启动底盘（示例 `tb3_0`）：

```bash
ROS_NAMESPACE=tb3_0 roslaunch turtlebot3_bringup turtlebot3_robot.launch multi_robot_name:=tb3_0
```

4. ✅ 每台机器人启动控制（推荐脚本）：

```bash
cd ~/turtlebot3_consensus_ws/src/tb3_distributed_control/scripts
./robot_start.sh 0
```

5. ✅ 主机启动控制中心（推荐）：

```bash
roslaunch tb3_distributed_control distributed_host_side.launch
```

6. 🛑 结束时停止机器人会话（示例 `tb3_0`）：

```bash
cd ~/turtlebot3_consensus_ws/src/tb3_distributed_control/scripts
./robot_stop.sh 0
```

## 🧪 4. 导航栈位姿方案（探索）

🟠 若需要导航栈位姿，请先按定位包说明启动机器人端定位链路，再在主机端使用：

```bash
roslaunch tb3_distributed_control distributed_host_side_nav_location.launch
```

📍 定位链路细节见：`机器人端功能包/src/tb3_distributed_location/README.md`

## ✅ 5. 快速自检

```bash
rosnode list
rostopic list | grep -E "tb3_0/(odom|scan|cmd_vel)|leader/history|system/shutdown"
```

---

🟣 **维护建议**：方案一级 README 保持简洁；细节仅在各功能包 README 维护，避免重复和版本不一致。

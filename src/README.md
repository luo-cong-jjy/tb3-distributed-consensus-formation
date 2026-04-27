# TurtleBot3 分布式一致性编队控制系统（主机端完整代码说明）

## 📌 说明范围

本说明面向 `tb3_distributed_control` 的主机端完整代码入口，按当前保留文件重新核对，覆盖三条主机使用路径：

- 🟢 纯软件仿真（Python脚本级，不走Gazebo主启动）
- 🟢 Gazebo仿真（ROS + Gazebo + 多机编队）
- 🟢 实物主机端控制（主机端 + 机器人端协同）

## 📁 当前代码结构（优化版：文件名后直接说明作用）

### 1) 顶层

```text
src/
├── CMakeLists.txt                      - 工作空间顶层构建入口
├── README.md                           - 主机端完整代码说明（本文件）
└── tb3_distributed_control/            - 分布式控制主功能包
```

### 2) 启动入口（launch）

```text
tb3_distributed_control/launch/
├── distributed_host_side.launch - 实物主机端启动（里程计主线）
├── distributed_host_side_nav_location.launch - 实物主机端启动（导航定位融合）
├── distributed_robot_side.launch - 实物机器人端控制节点启动
├── multi_turtlebot3_consensus_gazebo.launch - Gazebo主仿真总入口
├── multi_turtlebot3_consensus_gazebo_one_tb3.launch - Gazebo单机器人测试入口
├── multi_turtlebot3_consensus_gazebo_real_experiment.launch - Gazebo复现实物S形轨迹实验
├── multi_turtlebot3_consensus_gazebo_real_experiment_line.launch - Gazebo复现实物直线轨迹实验
├── multi_turtlebot3_consensus_gazebo_real_experiment_line_improve.launch - Gazebo复现改进版直线轨迹实验
├── multi_turtlebot3_consensus_see_gazebo.launch - 仅场景/模型可视化入口
├── multi_turtlebot3_consensus_see_gazebo_real_experiment.launch - 实物S形场景可视化入口
└── multi_turtlebot3_consensus_see_gazebo_real_experiment_line.launch - 实物直线场景可视化入口
```

### 3) 主机端核心脚本（scripts）

```text
tb3_distributed_control/scripts/
├── leader_node.py                     - 虚拟领导者轨迹生成、状态发布、停机信号发布
├── tb3_controller_node.py             - Gazebo仿真控制器（分布式一致性+避障）
├── tb3_controller_node_real.py        - 实物控制器（实物参数与流程）
├── distributed_control_visualizer.py  - 编队过程实时可视化（轨迹/标记/连线）
├── rviz_visualizer.py                 - RViz辅助可视化
├── visualize_results.py               - 数据记录、结果绘图、性能统计
└── print_notification.py              - 启动提示与状态通知
```

### 4) 纯软件仿真脚本

```text
tb3_distributed_control/纯软件仿真代码/
├── python_consensus_tracking_avoid.py - 基础一致性跟踪仿真
├── distributed_python_consensus_tracking_avoid.py - 分布式一致性仿真
├── ob_distributed_python_consensus_tracking_avoid.py - 含障碍物分布式仿真
├── complex_obstacle_ob_distributed_python_consensus_tracking_avoid.py - 复杂障碍物分布式仿真
├── tb3_controller_node.py - 纯仿真控制器脚本版本
└── trajectory_plot.py - 轨迹结果绘图
```

### 5) 消息与资源目录

```text
tb3_distributed_control/msg/LeaderHistoryData.msg  - 领导者历史数据消息
tb3_distributed_control/msg/RobotHistoryData.msg   - 机器人历史数据消息
tb3_distributed_control/docs/                      - 设计与部署文档
tb3_distributed_control/maps/                      - 地图配置
tb3_distributed_control/rviz/                      - RViz配置文件
tb3_distributed_control/urdf/                      - 机器人模型文件
tb3_distributed_control/worlds/                    - Gazebo场景文件
```

## 🚀 路径A：纯软件仿真（无Gazebo）

使用目录：`tb3_distributed_control/纯软件仿真代码`

典型脚本：
- 基础：`python_consensus_tracking_avoid.py`
- 分布式：`distributed_python_consensus_tracking_avoid.py`
- 含障碍物：`ob_distributed_python_consensus_tracking_avoid.py`
- 复杂障碍物：`complex_obstacle_ob_distributed_python_consensus_tracking_avoid.py`
- 轨迹绘图：`trajectory_plot.py`

示例：

```bash
cd ~/turtlebot3_distributed_consensus_formation_ws/src/tb3_distributed_control/纯软件仿真代码
python3 distributed_python_consensus_tracking_avoid.py
python3 trajectory_plot.py
```

适用场景：快速验证算法逻辑，不依赖Gazebo与多节点ROS编排。

## 🚀 路径B：Gazebo仿真（主机集中启动）

### 1) 主入口

```bash
roslaunch tb3_distributed_control multi_turtlebot3_consensus_gazebo.launch
```

### 2) 变体分组（更快定位）

日常常用：
- `multi_turtlebot3_consensus_gazebo_one_tb3.launch`（单机调参/快速联调）

论文复现实验：
- `multi_turtlebot3_consensus_gazebo_real_experiment.launch`（S形轨迹复现）
- `multi_turtlebot3_consensus_gazebo_real_experiment_line.launch`（直线轨迹复现）
- `multi_turtlebot3_consensus_gazebo_real_experiment_line_improve.launch`（改进版直线复现）

可视化检查：
- `multi_turtlebot3_consensus_see_gazebo.launch`（基础场景可视化）
- `multi_turtlebot3_consensus_see_gazebo_real_experiment.launch`（S形场景可视化）
- `multi_turtlebot3_consensus_see_gazebo_real_experiment_line.launch`（直线场景可视化）

### 3) 参数覆盖示例

```bash
roslaunch tb3_distributed_control multi_turtlebot3_consensus_gazebo.launch \
  total_time:=180 trajectory_type:=eight_slow_slow open_rviz:=true
```

## 🚀 路径C：实物部署（主机端完整链路）

### 1) 主机端启动

里程计方案（主线推荐）：

```bash
roslaunch tb3_distributed_control distributed_host_side.launch
```

导航定位融合方案（可探索）：

```bash
roslaunch tb3_distributed_control distributed_host_side_nav_location.launch
```

### 2) 机器人端（每台机器人各自执行）

```bash
roslaunch tb3_distributed_control distributed_robot_side.launch robot_id:=0 lidar_type:=LDS-02
```

其余机器人改 `robot_id:=1..4`。

## 🔧 编译与环境

```bash
cd ~/turtlebot3_distributed_consensus_formation_ws
catkin_make
source devel/setup.bash
```

建议环境：
- Ubuntu 20.04
- ROS Noetic
- TurtleBot3相关依赖
- Gazebo（仅路径B必需）

## ✅ 启动后快速自检

```bash
rosnode list
rostopic list | grep -E "leader|history|cmd_vel|shutdown"
```

重点话题应包含：
- `/tb3_virtual_leader/state`
- `/leader/history`
- `/tb3_0/history` 到 `/tb3_4/history`
- `/system/shutdown`

## 📚 关联文档

- `tb3_distributed_control/docs/启动及关闭说明.md`
- `tb3_distributed_control/docs/启动与通信逻辑分析.md`
- `tb3_distributed_control/docs/方案D实施说明.md`
- `tb3_distributed_control/docs/obstacle_management_guide.md`

---

如果后续继续删改脚本或launch文件，请同步更新本README中的“入口文件列表”和“启动命令”，避免文档与代码再出现偏差。
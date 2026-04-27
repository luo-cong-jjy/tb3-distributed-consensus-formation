# 🚀 tb3_distributed_control 机器人端分布式控制功能包说明（单机或多机实物部署）

📌 **控制功能包**：用于 TurtleBot3 机器人端执行分布式一致性控制，完成邻居信息融合、控制量计算与速度指令输出。

🔴 **⚠ 重要限制**
- 本包是机器人端控制包，不包含主机端 `distributed_host_side.launch`；需与主机端控制中心配合运行。
- 默认控制脚本面向实物与 `tb3_0 ~ tb3_4` 命名空间；修改机器人数量或拓扑时需同步修改控制脚本参数。
- 若底盘话题（如 `/<ns>/odom`、`/<ns>/scan`）未就绪，控制节点无法正常闭环。

## 🎯 1. 环境要求

- ✅ 机器人型号：TurtleBot3 Burger
- ✅ 系统版本：Ubuntu 20.04
- ✅ ROS 版本：ROS Noetic
- ✅ 功能包：`tb3_distributed_control`
- ✅ 建议工具：`tmux`（用于一键启动脚本）

## 📦 2. 核心文件（关键链路）

说明：本节仅列关键入口文件；完整目录见第 3 节。

- `launch/distributed_robot_side.launch`
  - 机器人端控制启动入口，按 `robot_id` 启动控制节点。
- `scripts/tb3_controller_node_real.py`
  - 实物控制主脚本（分布式一致性 + 轨迹跟踪 + 避障融合）。
- `scripts/robot_start.sh`
  - 机器人端一键启动脚本（底盘启动、就绪检测、初始旋转、控制节点启动）。
- `scripts/robot_stop.sh`
  - 一键停止指定机器人会话。
- `msg/RobotHistoryData.msg`
  - 机器人历史数据消息定义，用于状态与性能数据传输。

## 🧭 3. 完整目录结构（机器人端版本）

```bash
tb3_distributed_control/
├── 📂 launch/                                  # 启动文件
│   └── distributed_robot_side.launch           # 机器人端控制入口
├── 📂 msg/                                     # 自定义消息
│   └── RobotHistoryData.msg                    # 机器人历史数据定义
├── 📂 scripts/                                 # 控制与运维脚本
│   ├── tb3_controller_node_real.py             # 实物控制主脚本
│   ├── robot_start.sh                          # 一键启动（tmux）
│   ├── robot_stop.sh                           # 一键停止
│   ├── robot_rotate_90.py                      # 旋转辅助脚本
│   ├── robot_return_home.py                    # 回位辅助脚本
│   └── print_notification.py                   # 启动提示输出
├── package.xml                                 # 依赖声明
├── CMakeLists.txt                              # 编译配置
└── README.md                                   # 使用说明
```

### 3.1 文件职责速览

- 🧩 `distributed_robot_side.launch`
  - 参数：`robot_id`（默认 `0`）、`lidar_type`（默认 `LDS-02`）。
  - 启动：`tb3_controller_node_real.py` + 多条启动提示节点。
- 🎮 `tb3_controller_node_real.py`
  - 核心：分布式一致性控制、邻居拓扑计算、轨迹跟踪、控制输出。
  - 输入：`/<ns>/odom`、`/<ns>/scan`、邻居/领导者相关话题。
  - 输出：`/<ns>/cmd_vel` 与历史数据话题。
- 🚀 `robot_start.sh`
  - 自动执行：环境加载 -> 底盘启动 -> 话题就绪检查 -> 初始 90° 旋转 -> 控制节点启动。
  - 使用 tmux 创建 `Robot_Base / Controller / Monitor` 三窗口。
- 🛑 `robot_stop.sh`
  - 按 `robot_id` 结束 `tb3_<id>` tmux 会话。
- 🧪 `tb3_controller_node_real_Q_R_edit.py`
  - 控制权重调参实验版，用于 Q/R 快速试验。
- 🔄 `robot_rotate_90.py`
  - 支持单机/多机旋转调姿（可自定义旋转角度）。
- 🏠 `robot_return_home.py`
  - 支持单点/多航点回位，含基础雷达避障逻辑。

## ▶️ 4. 快速启动

### 🖥️ 4.1 主机端

```bash
roscore
```

### 🤖 4.2 机器人端推荐方式（一键启动）

前置条件：
- 已配置 `ROS_MASTER_URI` 和机器人本机网络变量（`ROS_IP` 或 `ROS_HOSTNAME`）。
- 已安装 `tmux`。

```bash
cd ~/turtlebot3_consensus_ws/src/tb3_distributed_control/scripts
./robot_start.sh <robot_id>
```

示例：

```bash
./robot_start.sh 0
```

### 🛠️ 4.3 机器人端手动方式（传统）

1. 启动底盘（示例 `tb3_0`）：

```bash
ROS_NAMESPACE=tb3_0 roslaunch turtlebot3_bringup turtlebot3_robot.launch multi_robot_name:=tb3_0
```

2. 新开终端启动控制节点：

```bash
cd ~/turtlebot3_consensus_ws
source devel/setup.bash
roslaunch tb3_distributed_control distributed_robot_side.launch robot_id:=0 lidar_type:=LDS-02
```

## 🧩 5. 启动逻辑与传输关系

### 5.1 启动链路

```text
robot_start.sh（可选）
  -> 启动 turtlebot3_bringup 底盘
  -> 检查 /tb3_<id>/odom 就绪
  -> 初始旋转90度（内联Python）
  -> roslaunch distributed_robot_side.launch
      -> 启动 tb3_controller_node_real.py
```

### 5.2 控制节点参数链路

```text
roslaunch distributed_robot_side.launch robot_id:=N lidar_type:=LDS-02
  -> 参数传入 tb3_controller_node_real.py
  -> 节点命名空间按 /tb3_N 工作
```

### 5.3 关键话题关系（机器人侧）

- 输入：`/<ns>/odom`、`/<ns>/scan`
- 输出：`/<ns>/cmd_vel`
- 数据：`RobotHistoryData`（用于历史与性能分析）

## ⚙️ 6. 参数说明

- `robot_id`：机器人编号（`0~4`，默认 `0`）
- `lidar_type`：雷达型号（`LDS-01` 或 `LDS-02`，默认 `LDS-02`）

## 🔄 7. 启动后预期行为

- 🔹 启动日志提示机器人端节点已就绪。
- 🔹 控制节点持续读取里程计/雷达并发布 `cmd_vel`。
- 🔹 若使用一键脚本，可在 tmux 中分窗口查看底盘、控制与监控状态。

## ✅ 8. 联调自检命令

以 `tb3_0` 为例：

```bash
rostopic list | grep -E "tb3_0/(odom|scan|cmd_vel)"
rosnode list | grep -E "tb3_controller_0|move_base|amcl"
rostopic hz /tb3_0/odom
rostopic hz /tb3_0/cmd_vel
```

🟠 **🧪 建议**
- 先单机验证 `odom/scan/cmd_vel` 链路，再扩展到多机。
- 修改 Q/R 权重时建议先在短时低速场景回归验证。

## 🛠️ 9. 常见问题

- ❓ 控制节点启动但机器人不动：
  - 检查底盘是否已启动，`/<ns>/odom` 是否存在。
- ❓ 无法连接主机端：
  - 检查 `ROS_MASTER_URI` 与本机网络变量设置。
- ❓ 一键脚本报 tmux 错误：
  - 安装 tmux：`sudo apt-get install -y tmux`。
- ❓ 多机运行时命名空间混乱：
  - 检查 `robot_id` 与 `ROS_NAMESPACE` 是否一致映射到 `tb3_<id>`。

---

🟢 **📝 版本说明**：本说明面向机器人端控制包，强调“可执行、可排障、可扩展”的标准功能包文档风格。

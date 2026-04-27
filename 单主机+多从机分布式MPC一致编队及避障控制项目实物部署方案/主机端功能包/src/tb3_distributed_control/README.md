# 🚀 tb3_distributed_control 主机端功能包说明（单主机 + 多机器人实物部署）

📌 **主机端功能包**：用于启动虚拟领导者、分布式状态可视化与结果分析，作为多机器人编队控制系统的控制中心。

🔴 **⚠ 重要说明**
- 本包当前推荐方案为**里程计位姿链路**（实时性优先）。
- 与“导航栈位姿”方案的核心区别：
  - 里程计位姿：推荐使用 `distributed_host_side.launch`。
  - 导航栈位姿：使用 `distributed_host_side_nav_location.launch`，作为未来可探索方案。
- 主机端需与机器人端 `tb3_distributed_control` 功能包配合运行，单独启动主机端无法完成闭环控制。

## 🎯 1. 环境要求

- ✅ 操作系统：Ubuntu 20.04
- ✅ ROS 版本：ROS Noetic
- ✅ 主机网络可访问全部机器人
- ✅ 功能包：`tb3_distributed_control`（主机端 + 机器人端）

## 📦 2. 核心文件（关键链路）

说明：本节仅列关键入口文件；完整目录见第 3 节。

- `launch/distributed_host_side.launch`
  - 主机端控制入口（里程计位姿链路，当前推荐）。
- `launch/distributed_host_side_nav_location.launch`
  - 导航栈位姿显示入口（支持 `rviz_config` 与地图服务，未来可探索）。
- `scripts/leader_node.py`
  - 虚拟领导者节点，生成参考轨迹并发布领导者状态。
- `scripts/distributed_control_visualizer.py`
  - 分布式控制可视化节点（机器人轨迹、编队结构等）。
- `scripts/visualize_results.py`
  - 实验数据分析与图表输出节点。

## 🧭 3. 完整目录结构（主机端版本）

```bash
tb3_distributed_control/
├── 📂 launch/                                                # 主机端启动入口
│   ├── distributed_host_side.launch                          # 里程计位姿版入口（推荐）
│   └── distributed_host_side_nav_location.launch             # 导航栈位姿版入口（探索）
├── 📂 msg/                                                   # 自定义消息
│   ├── LeaderHistoryData.msg                                 # 领导者历史数据
│   └── RobotHistoryData.msg                                  # 机器人历史数据
├── 📂 scripts/                                               # 主机端核心脚本
│   ├── leader_node.py                                        # 虚拟领导者轨迹生成
│   ├── distributed_control_visualizer.py                     # 分布式状态可视化
│   ├── visualize_results.py                                  # 结果分析与绘图
│   ├── rviz_visualizer.py                                    # RViz轨迹可视化辅助
│   └── print_notification.py                                 # 启动提示输出
├── package.xml                                               # 依赖声明
├── CMakeLists.txt                                            # 编译配置
└── README.md                                                 # 使用说明
```

### 3.1 文件职责速览

- 🧩 `distributed_host_side.launch`
  - 参数：`total_time`、`trajectory_type`、`open_rviz`、`virtual_leader_ns` 等。
  - 启动链路：`visualize_results.py` -> `leader_node.py` -> `distributed_control_visualizer.py` ->（可选）RViz（里程计位姿链路，推荐）。
- 🗺️ `distributed_host_side_nav_location.launch`
  - 新增参数：`rviz_config`（`navigation`/`control`），可在 `navigation` 模式下启动 map_server（导航栈位姿链路，探索）。
- 👑 `leader_node.py`
  - 轨迹类型由参数控制，发布 `/leader/history` 与停止信号 `/system/shutdown`。
- 📊 `distributed_control_visualizer.py`
  - 订阅领导者状态与机器人里程计，发布轨迹与标记话题。
- 📈 `visualize_results.py`
  - 保存实验数据，生成轨迹/误差/性能图表与统计结果。
- 📨 `LeaderHistoryData.msg` / `RobotHistoryData.msg`
  - 主机端与机器人端采用的话题数据结构定义。

## ▶️ 4. 快速启动

### 🖥️ 4.1 里程计位姿版（推荐）

```bash
roslaunch tb3_distributed_control distributed_host_side.launch
```

常用参数示例：

```bash
roslaunch tb3_distributed_control distributed_host_side.launch \
  total_time:=68 \
  trajectory_type:=real_experiment_trajectory \
  open_rviz:=false
```

### 🧪 4.2 导航栈位姿版（未来可探索）

```bash
roslaunch tb3_distributed_control distributed_host_side_nav_location.launch
```

常用参数示例：

```bash
roslaunch tb3_distributed_control distributed_host_side_nav_location.launch \
  total_time:=32 \
  trajectory_type:=real_experiment_trajectory_line \
  rviz_config:=navigation \
  open_rviz:=true
```

## 🧩 5. 启动逻辑与传输关系

### 5.1 主机端启动链路

```text
distributed_host_side.launch（里程计位姿推荐链路）
  -> visualize_results.py（结果记录/绘图）
  -> leader_node.py（领导者轨迹与系统时钟）
  -> distributed_control_visualizer.py（编队可视化）
  -> RViz（可选）
```

### 5.2 关键话题链路

- `leader_node.py` 发布：
  - `/<virtual_leader_ns>/state`（领导者状态）
  - `/leader/history`（领导者历史数据）
  - `/system/shutdown`（系统停止信号）
- `distributed_control_visualizer.py` 订阅：
  - `/<virtual_leader_ns>/state`
  - `/tb3_0~4/odom`
- `visualize_results.py` 订阅：
  - `LeaderHistoryData` / `RobotHistoryData` 相关历史话题

### 5.3 里程计位姿版 vs 导航栈位姿版

- 里程计位姿版（推荐）：`distributed_host_side.launch`。
- 导航栈位姿版（未来可探索）：`distributed_host_side_nav_location.launch`。
- 两种方案都可复用领导者与结果分析节点，建议优先使用里程计版做主线实验。

### 5.4 与机器人端协同关系

- 机器人端需要提前启动底盘与控制节点，主机端仅负责领导者与可视化/分析。
- 常见协同流程：
  1. 主机端 `roscore`
  2. 机器人端底盘 + 控制节点
  3. 主机端 `distributed_host_side*.launch`

## ⚙️ 6. 参数说明（主机端常用）

- `total_time`：系统总运行时间（秒）
- `trajectory_type`：轨迹类型（如 `real_experiment_trajectory`、`real_experiment_trajectory_line`）
- `open_rviz`：是否启动 RViz
- `virtual_leader_ns`：虚拟领导者命名空间
- `rviz_config`（仅导航版 launch）：`navigation` 或 `control`（里程计版无需该参数）

## 🔄 7. 启动后预期行为

- 🔹 控制台输出主机端启动提示与轨迹类型、运行时长。
- 🔹 虚拟领导者持续发布参考轨迹与历史数据。
- 🔹 到达 `total_time` 后主机端发布 `/system/shutdown`，系统进入停止流程。
- 🔹 结果分析节点输出图表与统计文件。

## ✅ 8. 联调自检命令

```bash
rosnode list | grep -E "leader_node|distributed_control_visualizer|result_visualizer"
rostopic list | grep -E "leader/history|system/shutdown|tb3_0/odom"
rostopic echo -n 1 /leader/history
rostopic hz /tb3_0/odom
```

🟠 **🧪 建议**
- 每次改动轨迹参数后，先做短时（15~30s）回归测试。
- 主机端与机器人端使用同一版消息定义，避免字段不一致导致解析失败。

## 🛠️ 9. 常见问题

- ❓ 启动时报找不到 `rviz/urdf/maps` 资源：
  - 确认运行环境中的 `tb3_distributed_control` 包路径包含这些目录。
- ❓ 主机端已启动但无轨迹显示：
  - 检查机器人端 `odom` 是否正常发布、命名空间是否为 `tb3_0~tb3_4`。
- ❓ 导航栈位姿版显示异常：
  - 检查机器人端是否正常发布 `amcl_pose`、`map`、`tf`。
- ❓ 结果图未生成或数据为空：
  - 检查 `LeaderHistoryData` / `RobotHistoryData` 话题是否有数据流。
- ❓ 系统未按时停止：
  - 检查 `leader_node.py` 是否正常发布 `/system/shutdown`。

---

🟢 **📝 版本说明**：本说明面向主机端功能包，采用与机器人端一致的文档结构，强调“可执行、可协同、可排障”。

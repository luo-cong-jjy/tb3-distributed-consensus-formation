# 🚀 tb3_distributed_location 导航栈位姿提供功能包说明（单机或者多机实物部署）

📌 **定位功能包**：用于多 TurtleBot3 在实物环境下获取统一 map 坐标系位姿（AMCL + 导航栈）。

🔴 **⚠ 重要限制**（通常直接用odom的位姿可符合实验中对于位姿实时要求，另外该功能包目前仅在陈师兄（CCH）的强化学习单机实物避障实验中效果良好）
- 当前实测导航位姿频率约为 **3-5 Hz**，若你的控制器位姿输入要求高于该频率，请先做闭环频率与稳定性验证，再决定是否用于正式实验。

## 🎯 1. 环境要求

- ✅ 机器人型号：TurtleBot3 Burger
- ✅ 系统版本：Ubuntu 20.04
- ✅ ROS 版本：ROS Noetic
- ✅ 功能包：`tb3_distributed_location`

## 📦 2. 核心文件（关键链路）

说明：本节仅列关键入口文件；完整目录见第 3 节。

- `launch/tb3_distributed_location.launch`
  - 本包主启动入口；汇总底盘、导航、位姿初始化参数。
- `launch/multi_turtlebot3_navigation.launch`
  - 导航总装配；启动 map_server、AMCL、move_base，并向子 launch 传递坐标参数。
- `launch/multi_amcl.launch`
  - AMCL 定位配置；接收 `initial_pose_x/y/a` 并设置坐标系参数。
- `launch/multi_move_base.launch`
  - move_base 与局部规划器配置；加载 `param/` 下代价地图与 DWA 参数。
- `src/turtlebot3_initial_localization.py`
  - 监听 `/<ns>/amcl_pose`，发布 `/<ns>/initialpose`，并发送 `/<ns>/cmd_vel` 旋转校准。

## 🧭 3. 完整目录结构（实物部署版本）

```bash
tb3_distributed_location/
├── 📂 launch/                                      # 启动链路
│   ├── tb3_distributed_location.launch             # 主入口（位姿参数入口）
│   ├── multi_turtlebot3_navigation.launch          # 导航总装配
│   ├── multi_amcl.launch                           # AMCL定位配置
│   └── multi_move_base.launch                      # move_base配置
├── 📂 src/                                         # 节点脚本
│   └── turtlebot3_initial_localization.py          # 初始位姿发布+旋转校准
├── 📂 maps/                                        # 地图文件
│   ├── 419_map.yaml
│   ├── 419_map.pgm
│   ├── 419_map_line.yaml
│   └── 419_map_line.pgm
├── 📂 param/                                       # 导航参数
│   ├── costmap_common_params_burger.yaml
│   ├── costmap_common_params_waffle.yaml
│   ├── costmap_common_params_waffle_pi.yaml
│   ├── local_costmap_params.yaml
│   ├── global_costmap_params.yaml
│   ├── move_base_params.yaml
│   ├── dwa_local_planner_params_burger.yaml
│   ├── dwa_local_planner_params_waffle.yaml
│   ├── dwa_local_planner_params_waffle_pi.yaml
│   └── base_local_planner_params.yaml
├── package.xml                                     # 依赖声明
├── CMakeLists.txt                                  # 编译配置
└── README.md                                       # 使用说明
```

### 3.1 文件职责补充（地图与参数）

- 🗺️ `maps/`
  - `419_map_line.yaml/.pgm`：当前默认地图。
  - `419_map.yaml/.pgm`：备用地图。
- ⚙️ `param/`
  - `costmap_common_params_*.yaml`：不同机型通用代价地图参数。
  - `local_costmap_params.yaml`、`global_costmap_params.yaml`：局部/全局代价地图参数。
  - `move_base_params.yaml`：move_base 核心参数。
  - `dwa_local_planner_params_*.yaml`：DWA 规划器参数（按机型区分）。

## ▶️ 4. 快速启动

### 🖥️ 4.1 主机端

```bash
roscore
```

### 🤖 4.2 机器人端（按机器人分别执行）

⚠ 注意：该命令会同时启动机器人底盘与导航栈，请先确认机器人端已安装 TurtleBot3 官方相关功能包。

通用启动模板：

```bash
ROS_NAMESPACE=<robot_ns> roslaunch tb3_distributed_location tb3_distributed_location.launch \
  multi_robot_name:=<robot_ns> \
  tb3_x_pos:=<x> \
  tb3_y_pos:=<y> \
  tb3_z_pos:=<yaw>
```

建议初始化位姿（示例编队）：

| 机器人 | x (m) | y (m) | yaw (rad) |
|---|---:|---:|---:|
| tb3_0 | 0.0 | 0.4 | 0.0 |
| tb3_1 | -0.346 | 0.2 | 0.0 |
| tb3_2 | -0.346 | -0.2 | 0.0 |
| tb3_3 | 0.346 | 0.2 | 0.0 |
| tb3_4 | 0.346 | -0.2 | 0.0 |

按 `tb3_0` 启动示例：

```bash
ROS_NAMESPACE=tb3_0 roslaunch tb3_distributed_location tb3_distributed_location.launch \
  multi_robot_name:=tb3_0 \
  tb3_x_pos:=0.0 \
  tb3_y_pos:=0.4 \
  tb3_z_pos:=0.0
```

## 🧩 5. 位姿设置逻辑与传输关系

### 5.1 默认值逻辑

- `tb3_distributed_location.launch` 是本包位姿设置主 launch。
- 若命令中不写 `tb3_x_pos/tb3_y_pos/tb3_z_pos`，默认值均为 `0.0`。
- 即默认按 `(x=0.0, y=0.0, yaw=0.0)` 初始化。
- `multi_robot_name` 在 launch 中虽有默认空值，但实物多机必须显式设置（例如 `tb3_0`）。

### 5.2 参数链路（launch 到脚本）

```text
roslaunch 命令参数
  -> tb3_distributed_location.launch
     -> include multi_turtlebot3_navigation.launch（继续传递 x/y/yaw）
     -> 启动 turtlebot3_initial_localization.py（args: <namespace> <x> <y> <yaw>）
```

### 5.3 脚本话题传输关系

- 订阅：`/<namespace>/amcl_pose`
  - 收到首帧后触发初始化。
- 发布：`/<namespace>/initialpose`
  - 将传入的 `x/y/yaw` 转为 `PoseWithCovarianceStamped` 并发布。
- 发布：`/<namespace>/cmd_vel`
  - 发送角速度指令，执行约 360° 原地旋转辅助 AMCL 收敛。

## ⚙️ 6. 参数说明

- `multi_robot_name`：机器人命名空间（必填，如 `tb3_0`）
- `tb3_x_pos`：初始 x 坐标（map 坐标系，单位 m，默认 `0.0`）
- `tb3_y_pos`：初始 y 坐标（map 坐标系，单位 m，默认 `0.0`）
- `tb3_z_pos`：初始朝向 yaw（单位 rad，默认 `0.0`）

## 🔄 7. 启动后预期行为

- 🔹 AMCL 采用设定位姿初始化。
- 🔹 延迟约 1 秒后，机器人自动原地旋转一周进行定位校准。
- 🔹 粒子云逐步收敛，位姿估计稳定输出。

## ✅ 8. 联调自检命令

```bash
rostopic list | grep -E "tb3_0/(initialpose|amcl_pose|odom|scan|cmd_vel)"
rostopic echo -n 1 /tb3_0/initialpose
rostopic hz /tb3_0/amcl_pose
```

🟠 **🧪 建议**
- 先在单机验证定位稳定性与频率，再扩展到多机编队控制。
- 多机实验前统一时间、地图版本与初始摆位，避免收敛偏差。

## 🛠️ 9. 常见问题

- ❓ `amcl_pose` 不更新：
  - 检查地图路径、激光雷达话题映射、TF 是否完整。
- ❓ `initialpose` 没生效：
  - 检查 `multi_robot_name` 是否与命名空间一致（如 `tb3_0`）。
- ❓ 位姿跳变明显：
  - 检查初始位姿是否接近真实值，确保旋转校准过程未被中断。
- ❓ 控制不稳定：
  - 优先确认定位频率是否满足控制周期要求（重点关注 3-5 Hz 限制）。

---

🟢 **📝 版本说明**：本说明面向实物部署，保持“可执行、可验证、可排障”的标准功能包文档风格。

# TurtleBot3 分布式一致性编队控制系统

## 📋 项目简介

本项目实现了基于TurtleBot3的多机器人分布式一致性编队控制系统，采用模型预测控制(MPC)和原始对偶神经网络(PDNN)算法，实现多机器人协同轨迹跟踪和编队控制。

### 核心特性

- 🤖 **多机器人编队**: 支持5个TurtleBot3机器人的分布式控制
- 🎯 **轨迹跟踪**: 虚拟领导者生成参考轨迹，跟随者实现一致性跟踪
- 🔄 **分布式通信**: 基于邻接矩阵的机器人间信息交换
- 📊 **实时可视化**: RViz实时显示编队状态和轨迹
- 🚀 **性能优化**: 基于ROS话题的高效数据传输架构
- ⏰ **自动管理**: 支持自动启动、运行和停止

## 🏗️ 系统架构

### 硬件架构
```
虚拟领导者 (tb3_virtual_leader)
    ↓ 参考轨迹
┌─────────────────────────────────────┐
│  TurtleBot3 编队 (5个机器人)          │
│  ┌─────┐  ┌─────┐  ┌─────┐           │
│  │ tb3_0├──┤ tb3_1├──┤ tb3_2│           │
│  └─────┘  └─────┘  └─┬───┘           │
│                      │               │
│  ┌─────┐            ┌┴───┐           │
│  │ tb3_3│            │tb3_4│           │
│  └─────┘            └─────┘           │
└─────────────────────────────────────┘
```

### 软件架构
```
┌─── 控制层 ───┐  ┌─── 通信层 ───┐  ┌─── 可视化层 ───┐
│ leader_node  │  │ ROS Topics  │  │ RViz Visualizer│
│ controller   │◄─┤ Message     ├─►│ Result Plots   │
│ GPNN/MPC     │  │ History     │  │ Data Analysis  │
└──────────────┘  └─────────────┘  └────────────────┘
```

### 核心脚本详解

#### 🎯 控制层脚本
- **`leader_node.py`** (虚拟领导者节点)
  - 功能：生成参考轨迹，协调系统时间基准
  - 特性：支持多种轨迹模式（8字形、圆形、直线）
  - 发布：领导者状态、轨迹数据、TF变换
  - 关键算法：相对时间管理、轨迹插值计算

- **`tb3_controller_node.py`** (分布式控制器)
  - 功能：实现单机器人的分布式一致性控制
  - 特性：GPNN+MPC混合优化、时间戳验证机制
  - 算法：梯度投影神经网络、模型预测控制
  - 通信：邻居状态交换、观测器数据发布

#### 📊 可视化层脚本
- **`rviz_visualizer.py`** (RViz实时可视化)
  - 功能：实时显示机器人状态、轨迹和编队形状
  - 特性：动态标记更新、路径轨迹显示
  - 输出：RViz可视化标记、路径话题

- **`distributed_control_visualizer.py`** (分布式控制状态可视化)
  - 功能：专门的编队状态可视化
  - 特性：五边形连线、实时位置标记
  - 输出：机器人标记数组、编队多边形

- **`visualize_results.py`** (结果分析绘图)
  - 功能：离线数据分析和图表生成
  - 特性：7种分析图表、性能统计报告、30秒后6时间节点连线
  - 输出：轨迹图、误差分析图、时间性能图、计算统计报告

#### 🔧 辅助脚本
- **`print_notification.py`** (系统通知)
  - 功能：系统状态通知和用户提示
  - 特性：启动完成提示、运行状态监控

### 启动配置文件
- **`multi_turtlebot3_consensus.launch`** (主启动文件)
  - 功能：协调整个系统的启动和关闭
  - 特性：时序控制、参数配置、自动化管理
  - 参数：运行时间、轨迹类型、编队配置

## 🚀 快速开始

### 环境要求

- **操作系统**: Ubuntu 20.04
- **ROS版本**: ROS Noetic


### 安装步骤

1. **创建工作空间**
```bash
mkdir -p ~/turtlebot3_consensus_ws/src
cd ~/turtlebot3_consensus_ws/src
```

2. **克隆项目**
```bash
git clone <项目地址>
```

3. **编译项目**
```bash
catkin_make
source devel/setup.bash
```

### 基本使用--完整系统启动
①gazebo仿真
```bash
# 启动完整分布式控制系统（默认120秒运行）
roslaunch tb3_distributed_control multi_turtlebot3_consensus.launch

# 自定义运行时间（30秒）
roslaunch tb3_distributed_control multi_turtlebot3_consensus.launch total_time:=30.0

# 选择不同轨迹类型
roslaunch tb3_distributed_control multi_turtlebot3_consensus.launch trajectory_type:=circle total_time:=60.0
```


②实物部署步骤
# 🚀 分布式一致性编队控制

## 📖 功能包简介

**ROS1功能包名称：** `tb3_distributed_control`

## 📁 期望文件结构

```bash
tb3_distributed_control/
├── 📂 launch/                    # 启动文件
│   ├── distributed_host_side.launch     # 🖥️ 主机端启动文件
│   └── distributed_robot_side.launch    # 🤖 机器人端启动文件
├── 📂 scripts/                   # 核心脚本
│   ├── leader_node.py                    # 👑 虚拟领导者节点
│   ├── tb3_controller_node.py            # 🎮 机器人控制节点
│   ├── distributed_control_visualizer.py # 📊 分布式控制可视化
│   ├── rviz_visualizer.py               # 👁️ RViz实时可视化
│   ├── visualize_results.py             # 📈 结果数据分析
│   └── print_notification.py            # 📢 系统通知
├── 📂 msg/                       # 自定义消息
│   ├── LeaderHistoryData.msg            # 领导者历史数据
│   └── RobotHistoryData.msg             # 机器人历史数据
├── 📂 rviz/                      # RViz配置
│   └── tb3_distributed_control.rviz     # 可视化配置文件
├── 📂 urdf/                      # 机器人模型
│   ├── turtlebot3_burger.gazebo.xacro
│   └── turtlebot3_burger.urdf.xacro
├── 📂 data_collect/              # 📊 实验数据存储
│   └── YYYY-MM-DD-HH-MM-SS-结果/        # 时间戳命名的结果文件夹
├── CMakeLists.txt
├── package.xml
└── README.md
```

## 🎯 分布式部署架构

### 🖥️ 主机端（Host PC）
```
📦 主机端功能包
├── 🚀 启动文件
│   └── distributed_host_side.launch    # 主机端控制中心
├── 👑 核心节点
│   ├── leader_node.py                  # 虚拟领导者（轨迹生成、时钟同步）
│   ├── distributed_control_visualizer.py  # 分布式控制可视化
│   ├── rviz_visualizer.py             # RViz实时轨迹显示
│   └── visualize_results.py           # 📈 数据分析与图表生成
├── 📨 消息定义
│   └── LeaderHistoryData.msg          # 领导者历史数据
└── 🎨 可视化配置
    ├── tb3_distributed_control.rviz   # RViz配置文件
    └── urdf/                          # 机器人3D模型
```

### 🤖 机器人端（Robot Side）
```
📦 机器人端功能包  
├── 🚀 启动文件
│   └── distributed_robot_side.launch  # 机器人端控制节点
├── 🎮 核心控制
│   └── tb3_controller_node.py         # 分布式一致性算法核心
└── 📨 消息定义
    └── RobotHistoryData.msg           # 机器人数据发布
```

## ✨ 主要功能特性

- 🎯 **多机器人编队控制**：支持5台TurtleBot3机器人分布式一致性编队
- 🔧 **灵活部署配置**：主机与机器人端分离，支持远程分布式部署
- 📊 **实时可视化**：RViz实时显示机器人轨迹、编队形状、质心等
- 📈 **数据分析**：自动生成轨迹图表、误差分析、性能统计报告
- 🔗 **自定义通信**：基于ROS消息的高效数据传输与同步

---

# 🛠️ 分布式一致性编队控制部署指南

## 🎯 环境准备

**系统要求：** TurtleBot3 Burger + Ubuntu 20.04 + ROS Noetic

## 🔧 部署步骤

### 📶 1. 网络配置
设置主机与所有机器人的主从机模式

### 🎬 2. 启动ROS Master
**主机端执行：**
```bash
roscore
```

传入整个功能包
编译
source
chmod +x 所有代码文件
修改launch的雷达参数

### 📍 3. 位姿获取方式选择

#### 🔄 方式1：里程计获取（推荐）

**步骤：**
1. **📍 精确摆放**：将机器人按代码初始位姿要求摆放在精准位置
2. **🚀 启动底盘**：在各机器人端执行
   ```bash
   # 机器人端分别执行：
   ROS_NAMESPACE=tb3_0 roslaunch turtlebot3_bringup turtlebot3_robot.launch multi_robot_name:=tb3_0
   ROS_NAMESPACE=tb3_1 roslaunch turtlebot3_bringup turtlebot3_robot.launch multi_robot_name:=tb3_1
   ROS_NAMESPACE=tb3_2 roslaunch turtlebot3_bringup turtlebot3_robot.launch multi_robot_name:=tb3_2
   ROS_NAMESPACE=tb3_3 roslaunch turtlebot3_bringup turtlebot3_robot.launch multi_robot_name:=tb3_3
   ROS_NAMESPACE=tb3_4 roslaunch turtlebot3_bringup turtlebot3_robot.launch multi_robot_name:=tb3_4
   ```
3. **⚖️ 坐标对齐(版本：坐标系相连）**：在控制脚本中进行里程计到全局坐标的偏移处理
   ```bash
   # 机器人端分别执行：
   ROS_NAMESPACE=tb3_0 roslaunch turtlebot3_bringup turtlebot3_robot.launch multi_robot_name:=tb3_0 set_lidar_frame_id:=tb3_0/base_scan
   
   ROS_NAMESPACE=tb3_1 roslaunch turtlebot3_bringup turtlebot3_robot.launch multi_robot_name:=tb3_1 set_lidar_frame_id:=tb3_1/base_scan

   ROS_NAMESPACE=tb3_2 roslaunch turtlebot3_bringup turtlebot3_robot.launch multi_robot_name:=tb3_2 set_lidar_frame_id:=tb3_2/base_scan

   ROS_NAMESPACE=tb3_3 roslaunch turtlebot3_bringup turtlebot3_robot.launch multi_robot_name:=tb3_3 set_lidar_frame_id:=tb3_3/base_scan

   ROS_NAMESPACE=tb3_4 roslaunch turtlebot3_bringup turtlebot3_robot.launch multi_robot_name:=tb3_4 set_lidar_frame_id:=tb3_4/base_scan


#### 🗺️ 方式2：导航栈位姿（需要地图）

需要额外的 `tb3_distributed_location` 功能包支持：

**步骤：**
1. **📍 精确摆放**：将机器人摆放在精准位置
2. **🚀 启动导航栈**：在各机器人端执行
   ```bash
   # 机器人端分别执行：
   ROS_NAMESPACE=tb3_0 roslaunch tb3_distributed_location tb3_distributed_location.launch multi_robot_name:="tb3_0"
   ROS_NAMESPACE=tb3_1 roslaunch tb3_distributed_location tb3_distributed_location.launch multi_robot_name:="tb3_1"
   ROS_NAMESPACE=tb3_2 roslaunch tb3_distributed_location tb3_distributed_location.launch multi_robot_name:="tb3_2"
   ROS_NAMESPACE=tb3_3 roslaunch tb3_distributed_location tb3_distributed_location.launch multi_robot_name:="tb3_3"
   ROS_NAMESPACE=tb3_4 roslaunch tb3_distributed_location tb3_distributed_location.launch multi_robot_name:="tb3_4"
   ```
3. **🔄 等待校准**：等待机器人旋转一周完成位姿校准

### 🎮 4. 启动分布式控制系统

#### 📋 准备工作
- ✅ 主机端已编译 `tb3_distributed_control` 功能包并 source 环境变量
- ✅ 机器人端已编译 `tb3_distributed_control` 功能包并 source 环境变量
- ✅ 机器人端已安装 `tmux`（推荐方案需要）

#### ⚠️ 注意事项

**控制节点配置：**
- 等待机制：实物机器人可选择性启用同步等待机制
- 里程计回调：需配置初始坐标偏移以对齐全局坐标系

**启动文件配置：**
- 机器人端需根据实际硬件修改雷达类型参数：
  - tb3_0: LDS-02
  - tb3_1: LDS-02
  - tb3_2: LDS-02
  - tb3_3: LDS-02
  - tb3_4: LDS-02

---

#### 🤖 启动机器人端控制节点

##### 🚀 **方案1：一键启动脚本（强烈推荐）**

使用自动化脚本，一条命令完成所有启动步骤：

**前置要求：**
- ✅ 主机端已启动 `roscore`
- ✅ 机器人端已配置 `ROS_MASTER_URI` 和 `ROS_IP` 环境变量
- ✅ 机器人端已安装 `tmux`

**配置环境变量（在机器人端 ~/.bashrc 中添加）：**
```bash
export ROS_MASTER_URI=http://<主机IP>:11311
export ROS_IP=<本机IP>
```

**启动命令：**
```bash
# 在各机器人端分别执行（以ID为0的机器人为例）：
cd ~/turtlebot3_consensus_ws
./src/tb3_distributed_control/scripts/robot_start.sh 0
或者：
cd ~/turtlebot3_consensus_ws/src/tb3_distributed_control/scripts
./robot_start.sh 0



# 其他机器人同理：
./robot_start.sh 1  # TB3_1
./robot_start.sh 2  # TB3_2
./robot_start.sh 3  # TB3_3
./robot_start.sh 4  # TB3_4
```

**脚本功能：**
- ✅ 自动检查 `ROS_MASTER_URI` 是否配置
- ✅ 自动加载所有ROS环境（通过 ~/.bashrc）
- ✅ 使用tmux创建3窗口会话（后台运行）
- ✅ 自动启动机器人底盘并等待话题就绪（最多等待30秒）
- ✅ 自动启动分布式控制节点
- ✅ 提供监控窗口方便调试和停止

**tmux窗口说明：**
| 窗口 | 名称 | 功能 |
|------|------|------|
| 0 | Robot_Base | 机器人底盘 (turtlebot3_bringup) |
| 1 | Controller | 分布式控制节点 |
| 2 | Monitor | 监控与操作窗口（可运行任意ROS命令） |

**tmux常用操作：**
```bash
# 查看所有会话
tmux ls

# 进入会话（查看运行状态）
tmux attach -t tb3_0

# 会话内快捷键：
#   Ctrl+B 然后按 0/1/2  - 切换窗口
#   Ctrl+B 然后按 d      - 退出会话（后台继续运行）
#   Ctrl+B 然后按 [      - 滚动查看历史（按q退出）

# 停止机器人（在监控窗口输入）
tmux kill-session -t tb3_0

# 或使用停止脚本
./robot_stop.sh 0
```

##### 📝 **方案2：手动启动（传统方式）**

如果不使用自动化脚本，需要手动执行以下步骤：

**步骤1：启动机器人底盘**
```bash
# TB3_0 机器人端
ROS_NAMESPACE=tb3_0 roslaunch turtlebot3_bringup turtlebot3_robot.launch multi_robot_name:=tb3_0

# TB3_1 机器人端  
ROS_NAMESPACE=tb3_1 roslaunch turtlebot3_bringup turtlebot3_robot.launch multi_robot_name:=tb3_1

# TB3_2 机器人端
ROS_NAMESPACE=tb3_2 roslaunch turtlebot3_bringup turtlebot3_robot.launch multi_robot_name:=tb3_2

# TB3_3 机器人端
ROS_NAMESPACE=tb3_3 roslaunch turtlebot3_bringup turtlebot3_robot.launch multi_robot_name:=tb3_3

# TB3_4 机器人端
ROS_NAMESPACE=tb3_4 roslaunch turtlebot3_bringup turtlebot3_robot.launch multi_robot_name:=tb3_4
```

**步骤2：新开终端，启动控制节点**
```bash
# 在每个机器人上新开终端执行：
cd ~/turtlebot3_consensus_ws
source devel/setup.bash

# TB3_0 机器人端
roslaunch tb3_distributed_control distributed_robot_side.launch robot_id:=0

# TB3_1 机器人端  
roslaunch tb3_distributed_control distributed_robot_side.launch robot_id:=1

# TB3_2 机器人端
roslaunch tb3_distributed_control distributed_robot_side.launch robot_id:=2

# TB3_3 机器人端
roslaunch tb3_distributed_control distributed_robot_side.launch robot_id:=3

# TB3_4 机器人端
roslaunch tb3_distributed_control distributed_robot_side.launch robot_id:=4
```

#### 🖥️ 启动主机端系统
**主机端执行：**
```bash
roslaunch tb3_distributed_control distributed_host_side.launch
```

## 📊 实验结果

- 🎯 **自动运行**：系统将按设定时间自动运行并关闭
- 📈 **数据保存**：实验数据自动保存到 `data_collect/YYYY-MM-DD-HH-MM-SS-结果/` 目录
- 📊 **结果分析**：自动生成轨迹图表、误差分析和性能统计报告

---

## ⚠️ 注意事项

1. **🔌 网络连接**：确保主机与所有机器人网络连通正常
2. **⏰ 时间同步**：建议各设备时间同步，避免数据时间戳问题
3. **🔋 电量充足**：确保机器人电量充足，避免实验中途断电
4. **📏 位置精度**：初始位置摆放精度直接影响控制效果
5. **🛠️ 编译检查**：如编译出错，检查 CMakeLists.txt 适配性

## 🔧 故障排除

- **网络通信问题**：检查 ROS_MASTER_URI 和 ROS_IP 设置
- **节点启动失败**：检查功能包路径和权限设置
- **数据不同步**：检查时钟同步和网络延迟
- **控制效果不佳**：检查初始位置和参数设置



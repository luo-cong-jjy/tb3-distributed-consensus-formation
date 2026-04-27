# 强化学习实物部署计划

## 核心代码迁移

## Turtlebot3环境准备

Turtlebot3环境配置：Turtlebot3 burger + Ubuntu 20.04 + ROS Noetic

ROS1功能包名称：```turtlebot3_rl_real```
主要文件： 

- ```turtlebot3_rl_real/launch/turtlebot3_rl_real.launch```和
- ```turtlebot3_rl_real/src/turtlebot3_initial_localization.py```

```turtlebot3_rl_real.launch```功能：

- 接收启动时的```robot_name:=tb1```参数，定义当前机器人名称
- 启动turtlebot3的启动文件```turtlebot3_robot.launch```
- 启动turtlebot3Navigation的启动文件```turtlebot3_navigation.launch```（需配置实际地图）
- 接受（或者通过话题映射）```“robot_name”/cmd_vel```话题
- 发布（或者通过话题映射）```“robot_name”/scan```话题、```“robot_name”/odom```话题和```/amcl_pose```话题
- 启动```turtlebot3_initial_localization.py```脚本

```turtlebot3_initial_localization.py```功能：

- 通过代码实现：向```/amcl_pose```话题发布初始坐标和朝向，用于粗略初始化navigation栈的坐标和朝向
- 控制机器人原地旋转360度或向前移动固定距离后向后退回原点，用于校准navigation栈提供的坐标和朝向

```turtlebot3_rl_real```包期望文件结构：

```bash
turtlebot3_rl_real
├── launch
│   └── turtlebot3_rl_real.launch
├── src
│   └── turtlebot3_initial_localization.py
├── maps
│   └── map.yaml
│   └── map.pgm
└── 其它必要的包配置文件
```

使用方法。
1.主机启动roscore

2.在小车终端： 
    ROS_NAMESPACE=tb3_0 roslaunch turtlebot3_rl_real turtlebot3_rl_real.launch multi_robot_name:="tb3_0" 
    ROS_NAMESPACE=tb3_1 roslaunch turtlebot3_rl_real turtlebot3_rl_real.launch multi_robot_name:="tb3_1"
    ROS_NAMESPACE=tb3_2 roslaunch turtlebot3_rl_real turtlebot3_rl_real.launch multi_robot_name:="tb3_2"
    ......

3.

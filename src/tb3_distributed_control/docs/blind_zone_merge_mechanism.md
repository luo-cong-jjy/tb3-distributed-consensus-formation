# 近距离盲区合并机制说明

## 🎯 问题描述

### 原始问题
当机器人靠近障碍物时，由于激光雷达的**最小检测距离限制**（默认0.18m），会出现以下问题：

```
障碍物示意图：
    ████████████████████
    ██              ██
    ██    盲区      ██  <-- 机器人靠太近，中间部分检测不到
    ██   (0.18m)    ██
    ██              ██
        \        /
         \      /
          \    /
           \  /
            \/
          机器人
```

**危险场景**：
- 原本是**一个完整的障碍物**
- 被分割成**两个独立的分区**
- 中间的盲区被误判为**安全通道**
- 机器人可能尝试从中间穿过，导致碰撞

## ✅ 解决方案

### 新增功能：`merge_close_adjacent_clusters()`

在聚类分析流程中添加**近距离相邻分区合并**步骤：

```python
# 处理流程
clusters = self.cluster_by_continuity(laser_data)        # 1. 基于连续性分区
clusters = self.merge_wraparound_clusters(clusters)      # 2. 处理360°跨越
clusters = self.merge_close_adjacent_clusters(clusters)  # 3. 🔥 合并近距离分区（新增）
filtered_clusters = [c for c in clusters if len(c) >= 3] # 4. 过滤噪声
```

### 合并条件

同时满足以下**三个条件**才会合并相邻分区：

1. **空间距离小** (`spatial_gap < 0.25m`)
   - 相邻分区的端点在物理空间上距离小于25cm
   
2. **角度差小** (`angle_gap < 0.3 rad ≈ 17°`)
   - 扫描角度连续，不是跳跃很远的两个位置
   
3. **至少一侧在盲区附近** (`range < 0.30m`)
   - 说明可能是由于靠太近导致的分离

### 合并逻辑示意

```
合并前：
分区A: [点1, 点2, 点3]          分区B: [点7, 点8, 点9]
                    ↑            ↑
                 点3(0.20m)   点7(0.22m)
                    └─────────┘
                   间隙 0.18m < 0.25m ✓
                   角度差 12° < 17° ✓
                   至少一侧 < 0.30m ✓
                   
合并后：
分区A+B: [点1, 点2, 点3, 点7, 点8, 点9]
         └─────────────────────────┘
         识别为同一个障碍物
```

## 📊 参数配置

可调整的阈值参数（在代码第679-681行）：

```python
merge_spatial_threshold = 0.25   # 空间距离阈值 (m)
merge_angle_threshold = 0.3      # 角度阈值 (rad)
blind_zone_threshold = 0.30      # 盲区判断阈值 (m)
```

### 参数调整建议

| 参数 | 增大效果 | 减小效果 | 建议值 |
|------|---------|---------|--------|
| `merge_spatial_threshold` | 更激进合并，可能误合并 | 更保守合并，可能漏掉 | 0.20-0.30m |
| `merge_angle_threshold` | 允许更大角度跨度 | 只合并角度很近的 | 0.2-0.4 rad |
| `blind_zone_threshold` | 更宽松的盲区判断 | 更严格的盲区判断 | 0.25-0.35m |

## 🧪 测试方法

### 场景1：正常避障
```bash
# 启动仿真
roslaunch tb3_distributed_control multi_turtlebot3_consensus_gazebo.launch

# 观察机器人远距离避障，不应触发合并
```

### 场景2：近距离接近障碍物
```bash
# 1. 启动仿真
roslaunch tb3_distributed_control multi_turtlebot3_consensus_gazebo.launch

# 2. 手动控制机器人靠近墙壁
roslaunch turtlebot3_teleop turtlebot3_teleop_key.launch

# 3. 观察日志输出
# 当距离 < 0.30m 时，应该看到：
# 🔗 [tb3_X] 近距离分区合并: 间隙=0.18m, 角度差=12.5°
```

### 场景3：使用聚类分析工具测试
```bash
# 启动聚类分析测试（带详细日志）
roslaunch tb3_distributed_control test_clustering_analysis.launch \
  robot_id:=4 verbose:=true visualize:=true

# 在RViz中观察聚类结果
# 手动驱动机器人靠近障碍物，观察分区是否正确合并
```

## 📈 性能影响

- **计算复杂度**：O(n) - 线性扫描所有分区
- **额外耗时**：< 0.1ms（相比总聚类时间可忽略）
- **内存开销**：无显著增加

## ⚠️ 注意事项

### 可能的副作用
1. **过度合并**：如果阈值设置过大，可能将实际分离的障碍物合并
2. **计算开销**：每次扫描都要检查所有相邻分区对

### 不适用场景
- 如果障碍物间隙确实存在且 > 25cm，不应合并
- 如果机器人不会靠近障碍物（< 0.30m），此功能不会触发

## 🔍 调试信息

前3次扫描会输出合并信息（可在代码第695行调整）：
```
🔗 [tb3_4] 近距离分区合并: 间隙=0.182m, 角度差=15.3°
```

如需持续输出，修改条件：
```python
# 修改前
if self.scan_count <= 3:

# 修改后（持续输出）
if True:
```

## 📝 代码位置

- **主函数**：`tb3_controller_node.py` 第649-706行
- **调用位置**：`laser_callback()` 第495行
- **参数定义**：第679-681行

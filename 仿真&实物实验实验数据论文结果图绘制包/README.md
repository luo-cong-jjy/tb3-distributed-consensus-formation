# 论文结果图绘制与视频截图工具

本目录用于将实验 `pkl` 数据与实验视频快速转换为论文图、截图序列和里程计 CSV。

## 🎯 一句话说明

- 🟢 `paper_graph_plot.py`：主绘图脚本（论文图主入口）
- 🟢 `parse_robot_odometry.py`：解析 `pkl` 并导出 `csv`
- 🟢 `paper_vedio_plot.py`：视频截图 / 鬼影图生成

## 📁 目录与文件职责

- `paper_graph_plot.py`：生成轨迹、误差、速度、观测器、触发事件、DoS 时序等图
- `parse_robot_odometry.py`：读取 `pkl`，打印统计，并输出 `output_odometry/*.csv`
- `paper_vedio_plot.py`：按时间采样视频，输出截图或鬼影融合图
- `8字形一致性编队及避障实验数据（实物：直线+S形）/`：实物实验 `pkl` 数据
- `实验视频/`：仿真/实物视频源
- `output_redraw_results/praph/`：论文图输出目录（按脚本当前配置）
- `output_redraw_results/vedio/screenshots/`：视频截图输出目录
- `output_odometry/`：里程计与 leader 导出 CSV

## 🚀 快速开始（推荐顺序）

### 1) 安装依赖

```bash
cd /home/gdut/24_LC/turtlebot3_distributed_consensus_formation_ws/仿真&实物实验实验数据论文结果图绘制包
pip3 install numpy matplotlib opencv-python
```

### 2) 生成论文图

编辑 `paper_graph_plot.py` 中配置：

```python
PKL_FILE_PATH = "./8字形一致性编队及避障实验数据（实物：直线+S形）/S/xxx.pkl"
OBSTACLE_MODE = 'experiment_s'  # none/simple/experiment/experiment_line/experiment_s
OUTPUT_DIR = "./output_redraw_results/praph"
```

运行：

```bash
python3 paper_graph_plot.py
```

### 3) 导出里程计 CSV（可选）

编辑 `parse_robot_odometry.py` 的 `PKL_FILE_PATH` 后运行：

```bash
python3 parse_robot_odometry.py
```

输出：

- `output_odometry/leader_data.csv`
- `output_odometry/robot_0_odometry.csv` 到 `robot_4_odometry.csv`

### 4) 生成视频截图/鬼影图（可选）

编辑 `paper_vedio_plot.py`：

```python
VIDEO_PATH = ".../实验视频/.../xxx.mp4"
SAMPLE_TIMES = [0.0, 10.0, 30.0]
MODE = 'screenshot'  # screenshot / ghost / darker / lighter
```

运行：

```bash
python3 paper_vedio_plot.py
```

## 📊 `paper_graph_plot.py` 实际输出图（当前版本）

输出目录：`output_redraw_results/praph/`

- `trajectory.png`：编队轨迹与障碍物
- `x_error.png`：X 方向误差
- `y_error.png`：Y 方向误差
- `cpl_control_input_x.png`：CPL 控制输入（x）
- `cpl_control_input_y.png`：CPL 控制输入（y）
- `heading_error.png`：航向误差
- `heading_angle.png`：航向角
- `linear_velocity.png`：线速度
- `angular_velocity.png`：角速度
- `obstacle_distance.png`：最近障碍物距离
- `avoidance_forces.png`：避障力
- `computation_time.png`：单步计算时间
- `observer_estimation.png`：观测器估计值
- `observer_estimation_error_x.png`：观测器估计误差（x）
- `observer_estimation_error_y.png`：观测器估计误差（y）
- `trigger_events.png`：事件触发时刻
- `dos_topology.png`：DoS 攻击时序拓扑

## ⚙️ 常用配置建议

- 🟢 论文投稿：`dpi = 600`
- 🟢 日常调试：可临时降到 `dpi = 150~300`
- 🟢 LaTeX 兼容优先：`use_latex = False`
- 🟠 若路径含 `~`：脚本会自动展开为家目录
- 🟠 相对路径基准：均以“脚本所在目录”为基准解析

## 🧪 常见问题

### 1) 报错 `PKL文件不存在`

检查 `PKL_FILE_PATH` 是否指向真实 `.pkl` 文件（不是 `.kpl`）。

### 2) 图中没有障碍物或障碍物位置不对

优先检查数据内是否自带 `obstacles`；若无则使用 `OBSTACLE_MODE` 的内置配置。

### 3) 视频打不开

先确认 `VIDEO_PATH` 存在；若编码特殊，建议先用 `ffmpeg` 转为标准 `mp4(H.264)` 后再处理。

### 4) 生成目录和预期不一致

当前主绘图输出目录变量是 `output_redraw_results/praph`（按脚本现状保留）。如需改名，可直接修改 `OUTPUT_DIR`。

## ✅ 最小检查清单

- 已设置正确 `PKL_FILE_PATH`
- 已设置正确 `VIDEO_PATH`（如需视频处理）
- 在本目录下执行脚本
- 输出目录出现 png/csv 文件

---

如需进一步精简为“论文附录版 README（超短版）”，可以在此基础上再压缩到 1 页以内。

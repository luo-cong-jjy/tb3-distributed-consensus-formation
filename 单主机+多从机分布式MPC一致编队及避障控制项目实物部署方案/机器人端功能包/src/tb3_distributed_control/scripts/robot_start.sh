#!/bin/bash
# TurtleBot3 分布式控制 - 机器人端一键启动脚本
# 使用方法: ./robot_start.sh <robot_id>
# 示例: ./robot_start.sh 0

# 检查参数
if [ $# -ne 1 ]; then
    echo "❌ 错误: 缺少机器人ID参数"
    echo "使用方法: $0 <robot_id>"
    echo "示例: $0 0"
    exit 1
fi

ROBOT_ID=$1
ROBOT_NAME="tb3_${ROBOT_ID}"
WORKSPACE_DIR="$HOME/turtlebot3_consensus_ws"

# 检查ROS_MASTER_URI是否设置（最优先，底盘启动需要）
if [ -z "$ROS_MASTER_URI" ]; then
    echo "❌ 错误: ROS_MASTER_URI 未设置"
    echo "请先在主机端启动 roscore，并在机器人端设置环境变量："
    echo "  export ROS_MASTER_URI=http://<主机IP>:11311"
    echo "  export ROS_IP=<本机IP>"
    exit 1
fi

echo "=========================================="
echo "🤖 启动机器人: ${ROBOT_NAME}"
echo "📡 ROS_MASTER_URI: $ROS_MASTER_URI"
echo "=========================================="

# 检查工作空间是否存在
if [ ! -d "$WORKSPACE_DIR" ]; then
    echo "❌ 错误: 工作空间不存在: $WORKSPACE_DIR"
    exit 1
fi

# Source用户环境（包含所有已配置的ROS环境）
source ~/.bashrc

# Source 分布式控制工作空间
if [ -d "$WORKSPACE_DIR/devel" ]; then
    source $WORKSPACE_DIR/devel/setup.bash
    echo "✅ 已加载工作空间环境"
else
    echo "❌ 错误: 未找到分布式控制工作空间: $WORKSPACE_DIR"
    exit 1
fi

# 使用tmux创建多窗口会话
SESSION_NAME="tb3_${ROBOT_ID}"

# 检查tmux是否安装
if ! command -v tmux &> /dev/null; then
    echo "❌ 错误: tmux 未安装"
    echo "请运行: sudo apt-get install tmux"
    exit 1
fi

# 如果会话已存在，先关闭
tmux has-session -t $SESSION_NAME 2>/dev/null
if [ $? -eq 0 ]; then
    echo "🔄 关闭现有会话: $SESSION_NAME"
    tmux kill-session -t $SESSION_NAME
fi

# 创建新的tmux会话
echo "🚀 创建tmux会话: $SESSION_NAME"
tmux new-session -d -s $SESSION_NAME

# 窗口1: 启动机器人底盘
tmux rename-window -t $SESSION_NAME:0 'Robot_Base'
tmux send-keys -t $SESSION_NAME:0 "source ~/.bashrc" C-m
tmux send-keys -t $SESSION_NAME:0 "echo '🤖 启动机器人底盘...'" C-m
tmux send-keys -t $SESSION_NAME:0 "ROS_NAMESPACE=${ROBOT_NAME} roslaunch turtlebot3_bringup turtlebot3_robot.launch multi_robot_name:=${ROBOT_NAME}" C-m

# 等待底盘完全启动并检查关键话题是否就绪
echo "⏳ 等待机器人底盘启动并检查话题就绪状态..."
sleep 5

# 检查odom话题是否就绪
TIMEOUT=30
ELAPSED=0
while [ $ELAPSED -lt $TIMEOUT ]; do
    rostopic list 2>/dev/null | grep -q "/${ROBOT_NAME}/odom"
    if [ $? -eq 0 ]; then
        echo "✅ 底盘已就绪: /${ROBOT_NAME}/odom 话题检测到"
        break
    fi
    echo "⏳ 等待 /${ROBOT_NAME}/odom 话题... ($ELAPSED/$TIMEOUT 秒)"
    sleep 2
    ELAPSED=$((ELAPSED + 2))
done

if [ $ELAPSED -ge $TIMEOUT ]; then
    echo "⚠️  警告: 超时未检测到 /${ROBOT_NAME}/odom 话题，但继续启动控制节点"
fi

# 额外等待2秒确保传感器数据稳定
sleep 2

# 🔄 执行初始旋转90度（使用内联Python脚本）
echo "🔄 开始执行初始旋转（逆时针90度）..."
python3 - <<EOF_ROTATE
#!/usr/bin/env python3
import rospy
import math
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion

class QuickRotate:
    def __init__(self, namespace):
        self.namespace = namespace
        self.rotation_angle = math.pi / 2  # 90度
        self.current_theta = None
        self.initial_theta = None
        self.target_theta = None
        
        # PID参数
        self.angular_kp = 1.5
        self.angular_ki = 0.02
        self.angular_kd = 0.2
        self.angular_error_integral = 0.0
        self.angular_last_error = 0.0
        self.angular_integral_limit = 0.5
        self.max_angular_vel = 0.8
        self.angle_threshold = 0.05  # 约3度
        self.last_time = None
        
        cmd_topic = f"/{namespace}/cmd_vel"
        odom_topic = f"/{namespace}/odom"
        
        rospy.init_node(f'quick_rotate_{namespace}', anonymous=True)
        self.cmd_pub = rospy.Publisher(cmd_topic, Twist, queue_size=10)
        self.odom_sub = rospy.Subscriber(odom_topic, Odometry, self.odom_callback)
        
    def odom_callback(self, msg):
        orientation = msg.pose.pose.orientation
        _, _, yaw = euler_from_quaternion([orientation.x, orientation.y, orientation.z, orientation.w])
        self.current_theta = yaw
        if self.initial_theta is None:
            self.initial_theta = yaw
            self.target_theta = self.normalize_angle(yaw + self.rotation_angle)
    
    def normalize_angle(self, angle):
        while angle > math.pi:
            angle -= 2.0 * math.pi
        while angle < -math.pi:
            angle += 2.0 * math.pi
        return angle
    
    def run(self):
        rate = rospy.Rate(20)
        print("⏳ 等待里程计数据...")
        while not rospy.is_shutdown() and (self.current_theta is None or self.target_theta is None):
            rate.sleep()
        
        print(f"🔄 开始旋转：{math.degrees(self.initial_theta):.1f}° → {math.degrees(self.target_theta):.1f}°")
        start_time = rospy.Time.now()
        
        while not rospy.is_shutdown():
            if (rospy.Time.now() - start_time).to_sec() > 30.0:
                print("⚠️  旋转超时")
                break
            
            # 计算控制
            current_time = rospy.Time.now()
            if self.last_time is None:
                dt = 0.05
            else:
                dt = (current_time - self.last_time).to_sec()
                if dt <= 0:
                    dt = 0.05
            self.last_time = current_time
            
            angle_error = self.normalize_angle(self.target_theta - self.current_theta)
            
            if abs(angle_error) > self.angle_threshold:
                # PID控制
                self.angular_error_integral += angle_error * dt
                self.angular_error_integral = max(min(self.angular_error_integral, 
                                                      self.angular_integral_limit), 
                                                  -self.angular_integral_limit)
                angular_derivative = (angle_error - self.angular_last_error) / dt
                self.angular_last_error = angle_error
                
                cmd = Twist()
                cmd.angular.z = (self.angular_kp * angle_error + 
                               self.angular_ki * self.angular_error_integral + 
                               self.angular_kd * angular_derivative)
                cmd.angular.z = max(min(cmd.angular.z, self.max_angular_vel), -self.max_angular_vel)
                self.cmd_pub.publish(cmd)
            else:
                # 完成旋转
                stop_cmd = Twist()
                self.cmd_pub.publish(stop_cmd)
                print(f"✅ 旋转完成！最终角度: {math.degrees(self.current_theta):.1f}°")
                break
            
            rate.sleep()
        
        # 确保停止
        stop_cmd = Twist()
        self.cmd_pub.publish(stop_cmd)

if __name__ == '__main__':
    try:
        rotator = QuickRotate('${ROBOT_NAME}')
        rotator.run()
    except Exception as e:
        print(f"❌ 旋转出错: {e}")
EOF_ROTATE

if [ $? -eq 0 ]; then
    echo "✅ 初始旋转完成"
else
    echo "⚠️  初始旋转失败，但继续启动控制节点"
fi

sleep 1

# 窗口2: 启动分布式控制节点
tmux new-window -t $SESSION_NAME:1 -n 'Controller'
tmux send-keys -t $SESSION_NAME:1 "cd $WORKSPACE_DIR" C-m
tmux send-keys -t $SESSION_NAME:1 "source devel/setup.bash" C-m
tmux send-keys -t $SESSION_NAME:1 "echo '🎮 启动分布式控制节点...'" C-m
tmux send-keys -t $SESSION_NAME:1 "roslaunch tb3_distributed_control distributed_robot_side.launch robot_id:=${ROBOT_ID}" C-m

# 窗口3: 监控与操作窗口
tmux new-window -t $SESSION_NAME:2 -n 'Monitor'
tmux send-keys -t $SESSION_NAME:2 "source ~/.bashrc" C-m
tmux send-keys -t $SESSION_NAME:2 "clear" C-m
# 🎯 优化：使用单个命令输出所有提示信息（避免污染命令历史）
tmux send-keys -t $SESSION_NAME:2 "cat << 'HELP_EOF'
📊 监控与操作窗口 - ${ROBOT_NAME}
==========================================
💡 常用命令：
  rostopic list                          # 查看所有话题
  rosnode list                           # 查看所有节点
  rostopic echo /${ROBOT_NAME}/cmd_vel   # 监控速度
  rostopic echo /${ROBOT_NAME}/odom      # 监控位置
  tmux kill-session -t ${SESSION_NAME}   # 🛑 停止机器人
  ./robot_stop.sh <robot_id>             # 🛑 停止机器人（推荐）
  只关闭控制节点：
        # 按 Ctrl+B 然后按 1，切换到Controller窗口
        # 按 Ctrl+C 停止控制节点
HELP_EOF" C-m

# 切换到第一个窗口
tmux select-window -t $SESSION_NAME:0

echo ""
echo "✅ 启动完成！"
echo ""
echo "📺 tmux会话: $SESSION_NAME"
echo ""
echo "🎹 窗口说明:"
echo "   窗口0 (Robot_Base)  - 机器人底盘 (turtlebot3_bringup)"
echo "   窗口1 (Controller)  - 分布式控制节点"
echo "   窗口2 (Monitor)     - 监控与操作窗口 (可运行任意ROS命令)"
echo ""
echo "🎹 快捷键:"
echo "   Ctrl+B 然后按 0/1/2  - 切换窗口"
echo "   Ctrl+B 然后按 d      - 退出会话（后台继续运行）"
echo "   Ctrl+B 然后按 [      - 滚动查看历史（按q退出）"
echo ""
echo "🛑 停止: 切换到窗口2，输入 tmux kill-session -t $SESSION_NAME"
echo "=========================================="

# 自动进入tmux会话
tmux attach -t $SESSION_NAME

#!/bin/bash
# TurtleBot3 分布式控制 - 机器人端停止脚本
# 使用方法: ./robot_stop.sh <robot_id>

if [ $# -ne 1 ]; then
    echo "使用方法: $0 <robot_id>"
    exit 1
fi

ROBOT_ID=$1
SESSION_NAME="tb3_${ROBOT_ID}"

echo "🛑 停止机器人 tb3_${ROBOT_ID}..."
tmux kill-session -t $SESSION_NAME 2>/dev/null

if [ $? -eq 0 ]; then
    echo "✅ 机器人 tb3_${ROBOT_ID} 已停止"
else
    echo "⚠️  会话 $SESSION_NAME 不存在或已停止"
fi

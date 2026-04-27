#!/usr/bin/env python3
import rospy
import sys

def main():
    # 初始化节点（匿名模式，避免节点名冲突）
    rospy.init_node("print_notification", anonymous=True)
    # 从参数服务器获取提示文本（launch文件中传递）
    if rospy.has_param("~text"):
        text = rospy.get_param("~text")
        # 打印提示（带分隔符，更清晰）
        print("="*50)
        print(f"[Launch Notification] {text}")
        print("="*50)
    else:
        rospy.logwarn("未设置提示文本参数 '~text'")
    # 节点立即退出（仅打印一次）
    rospy.signal_shutdown("提示打印完成")

if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        pass
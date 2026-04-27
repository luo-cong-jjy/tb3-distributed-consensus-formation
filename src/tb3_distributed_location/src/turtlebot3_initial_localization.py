#!/usr/bin/env python3
import rospy
import sys
import time
import math
from geometry_msgs.msg import PoseWithCovarianceStamped, Twist
from tf.transformations import quaternion_from_euler

# 用于标记是否收到 amcl_pose 消息
amcl_pose_received = False
# 存储命名空间
namespace = None


def amcl_pose_callback(msg):
    global amcl_pose_received
    if not amcl_pose_received:
        amcl_pose_received = True
        set_initial_pose()
        


def set_initial_pose():
    global namespace
    # 预设的机器人起点（使用存储的命名空间）
    pose = {"ns": namespace, "x": 0, "y": 0, "yaw": 0}

    # 发布初始位姿的发布者
    initial_pose_pub = rospy.Publisher(f'/{pose["ns"]}/initialpose', PoseWithCovarianceStamped, queue_size=10)
    rospy.sleep(0.5)  # 等待发布者注册

    # 创建初始位姿消息
    initial_pose_msg = PoseWithCovarianceStamped()
    initial_pose_msg.header.frame_id = "map"
    initial_pose_msg.pose.pose.position.x = pose["x"]
    initial_pose_msg.pose.pose.position.y = pose["y"]
    q = quaternion_from_euler(0, 0, pose["yaw"])
    initial_pose_msg.pose.pose.orientation.x = q[0]
    initial_pose_msg.pose.pose.orientation.y = q[1]
    initial_pose_msg.pose.pose.orientation.z = q[2]
    initial_pose_msg.pose.pose.orientation.w = q[3]

    # 发布初始位姿消息
    initial_pose_pub.publish(initial_pose_msg)
    rospy.loginfo(f"Set initial pose for {pose['ns']}: ({pose['x']}, {pose['y']}, {pose['yaw']})")

    # 控制机器人原地旋转 360 度
    rotate_360(pose["ns"])


def rotate_360(namespace):
    # 创建一个发布者，发布速度指令到 cmd_vel 话题
    cmd_vel_pub = rospy.Publisher(f'/{namespace}/cmd_vel', Twist, queue_size=10)
    rospy.sleep(0.5)  # 等待发布者注册

    # 创建一个 Twist 消息对象
    twist_msg = Twist()
    # 设置角速度（单位：弧度/秒），正值表示逆时针旋转
    angular_speed = 0.5
    twist_msg.angular.z = angular_speed

    # 计算旋转 360 度所需的时间
    # 使用 math.pi 提高精度
    angle_to_rotate = 2 * math.pi
    time_to_rotate = angle_to_rotate / angular_speed

    # 记录开始时间
    start_time = time.time()

    # 发布速度指令，开始旋转
    while (time.time() - start_time) < time_to_rotate:
        cmd_vel_pub.publish(twist_msg)
        rospy.sleep(0.1)

    # 停止旋转
    twist_msg.angular.z = 0
    cmd_vel_pub.publish(twist_msg)
    rospy.loginfo(f"Robot {namespace} has rotated 360 degrees.")


if __name__ == '__main__':
    try:
        if len(sys.argv) > 1:
            namespace = sys.argv[1]
        else:
            rospy.logerr("Please provide the multi_robot_name as an argument.")
            sys.exit(1)

        rospy.init_node('wait_for_amcl_pose', anonymous=True)
        # 订阅带命名空间的 amcl_pose 话题
        rospy.Subscriber(f'/{namespace}/amcl_pose', PoseWithCovarianceStamped, amcl_pose_callback)
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
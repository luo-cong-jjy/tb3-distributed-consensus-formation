;; Auto-generated. Do not edit!


(when (boundp 'tb3_distributed_control::LeaderHistoryData)
  (if (not (find-package "TB3_DISTRIBUTED_CONTROL"))
    (make-package "TB3_DISTRIBUTED_CONTROL"))
  (shadow 'LeaderHistoryData (find-package "TB3_DISTRIBUTED_CONTROL")))
(unless (find-package "TB3_DISTRIBUTED_CONTROL::LEADERHISTORYDATA")
  (make-package "TB3_DISTRIBUTED_CONTROL::LEADERHISTORYDATA"))

(in-package "ROS")
;;//! \htmlinclude LeaderHistoryData.msg.html


(defclass tb3_distributed_control::LeaderHistoryData
  :super ros::object
  :slots (_trajectory_time _ros_timestamp _x0 _y0 _theta0 _v0 _w0 _u0x _u0y ))

(defmethod tb3_distributed_control::LeaderHistoryData
  (:init
   (&key
    ((:trajectory_time __trajectory_time) 0.0)
    ((:ros_timestamp __ros_timestamp) 0.0)
    ((:x0 __x0) 0.0)
    ((:y0 __y0) 0.0)
    ((:theta0 __theta0) 0.0)
    ((:v0 __v0) 0.0)
    ((:w0 __w0) 0.0)
    ((:u0x __u0x) 0.0)
    ((:u0y __u0y) 0.0)
    )
   (send-super :init)
   (setq _trajectory_time (float __trajectory_time))
   (setq _ros_timestamp (float __ros_timestamp))
   (setq _x0 (float __x0))
   (setq _y0 (float __y0))
   (setq _theta0 (float __theta0))
   (setq _v0 (float __v0))
   (setq _w0 (float __w0))
   (setq _u0x (float __u0x))
   (setq _u0y (float __u0y))
   self)
  (:trajectory_time
   (&optional __trajectory_time)
   (if __trajectory_time (setq _trajectory_time __trajectory_time)) _trajectory_time)
  (:ros_timestamp
   (&optional __ros_timestamp)
   (if __ros_timestamp (setq _ros_timestamp __ros_timestamp)) _ros_timestamp)
  (:x0
   (&optional __x0)
   (if __x0 (setq _x0 __x0)) _x0)
  (:y0
   (&optional __y0)
   (if __y0 (setq _y0 __y0)) _y0)
  (:theta0
   (&optional __theta0)
   (if __theta0 (setq _theta0 __theta0)) _theta0)
  (:v0
   (&optional __v0)
   (if __v0 (setq _v0 __v0)) _v0)
  (:w0
   (&optional __w0)
   (if __w0 (setq _w0 __w0)) _w0)
  (:u0x
   (&optional __u0x)
   (if __u0x (setq _u0x __u0x)) _u0x)
  (:u0y
   (&optional __u0y)
   (if __u0y (setq _u0y __u0y)) _u0y)
  (:serialization-length
   ()
   (+
    ;; float64 _trajectory_time
    8
    ;; float64 _ros_timestamp
    8
    ;; float64 _x0
    8
    ;; float64 _y0
    8
    ;; float64 _theta0
    8
    ;; float64 _v0
    8
    ;; float64 _w0
    8
    ;; float64 _u0x
    8
    ;; float64 _u0y
    8
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float64 _trajectory_time
       (sys::poke _trajectory_time (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _ros_timestamp
       (sys::poke _ros_timestamp (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _x0
       (sys::poke _x0 (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _y0
       (sys::poke _y0 (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _theta0
       (sys::poke _theta0 (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _v0
       (sys::poke _v0 (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _w0
       (sys::poke _w0 (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _u0x
       (sys::poke _u0x (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _u0y
       (sys::poke _u0y (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float64 _trajectory_time
     (setq _trajectory_time (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _ros_timestamp
     (setq _ros_timestamp (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _x0
     (setq _x0 (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _y0
     (setq _y0 (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _theta0
     (setq _theta0 (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _v0
     (setq _v0 (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _w0
     (setq _w0 (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _u0x
     (setq _u0x (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _u0y
     (setq _u0y (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;;
   self)
  )

(setf (get tb3_distributed_control::LeaderHistoryData :md5sum-) "e13ef0559dc1ccb0a5a11bd1a53b8ab3")
(setf (get tb3_distributed_control::LeaderHistoryData :datatype-) "tb3_distributed_control/LeaderHistoryData")
(setf (get tb3_distributed_control::LeaderHistoryData :definition-)
      "# ROS话题优化版本：领导者历史数据消息类型

# 时间戳信息
float64 trajectory_time    # 轨迹相对时间（从0开始）
float64 ros_timestamp     # ROS时间戳

# 位置和姿态数据  
float64 x0               # 领导者x坐标
float64 y0               # 领导者y坐标
float64 theta0           # 领导者航向角

# 速度数据
float64 v0               # 线速度
float64 w0               # 角速度
float64 u0x              # x方向速度分量
float64 u0y              # y方向速度分量
")



(provide :tb3_distributed_control/LeaderHistoryData "e13ef0559dc1ccb0a5a11bd1a53b8ab3")



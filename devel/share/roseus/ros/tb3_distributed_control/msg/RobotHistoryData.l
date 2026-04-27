;; Auto-generated. Do not edit!


(when (boundp 'tb3_distributed_control::RobotHistoryData)
  (if (not (find-package "TB3_DISTRIBUTED_CONTROL"))
    (make-package "TB3_DISTRIBUTED_CONTROL"))
  (shadow 'RobotHistoryData (find-package "TB3_DISTRIBUTED_CONTROL")))
(unless (find-package "TB3_DISTRIBUTED_CONTROL::ROBOTHISTORYDATA")
  (make-package "TB3_DISTRIBUTED_CONTROL::ROBOTHISTORYDATA"))

(in-package "ROS")
;;//! \htmlinclude RobotHistoryData.msg.html


(defclass tb3_distributed_control::RobotHistoryData
  :super ros::object
  :slots (_robot_id _trajectory_time _ros_timestamp _xc _yc _thetac _vc _wc _xe _ye _thetae _xr _yr _zxeo_x _zxeo_y _raw_min_obstacle_distance _closest_obstacle_distance _total_clusters_count _avoidance_force_magnitude _computation_time _full_cycle_time ))

(defmethod tb3_distributed_control::RobotHistoryData
  (:init
   (&key
    ((:robot_id __robot_id) 0)
    ((:trajectory_time __trajectory_time) 0.0)
    ((:ros_timestamp __ros_timestamp) 0.0)
    ((:xc __xc) 0.0)
    ((:yc __yc) 0.0)
    ((:thetac __thetac) 0.0)
    ((:vc __vc) 0.0)
    ((:wc __wc) 0.0)
    ((:xe __xe) 0.0)
    ((:ye __ye) 0.0)
    ((:thetae __thetae) 0.0)
    ((:xr __xr) 0.0)
    ((:yr __yr) 0.0)
    ((:zxeo_x __zxeo_x) 0.0)
    ((:zxeo_y __zxeo_y) 0.0)
    ((:raw_min_obstacle_distance __raw_min_obstacle_distance) 0.0)
    ((:closest_obstacle_distance __closest_obstacle_distance) 0.0)
    ((:total_clusters_count __total_clusters_count) 0)
    ((:avoidance_force_magnitude __avoidance_force_magnitude) 0.0)
    ((:computation_time __computation_time) 0.0)
    ((:full_cycle_time __full_cycle_time) 0.0)
    )
   (send-super :init)
   (setq _robot_id (round __robot_id))
   (setq _trajectory_time (float __trajectory_time))
   (setq _ros_timestamp (float __ros_timestamp))
   (setq _xc (float __xc))
   (setq _yc (float __yc))
   (setq _thetac (float __thetac))
   (setq _vc (float __vc))
   (setq _wc (float __wc))
   (setq _xe (float __xe))
   (setq _ye (float __ye))
   (setq _thetae (float __thetae))
   (setq _xr (float __xr))
   (setq _yr (float __yr))
   (setq _zxeo_x (float __zxeo_x))
   (setq _zxeo_y (float __zxeo_y))
   (setq _raw_min_obstacle_distance (float __raw_min_obstacle_distance))
   (setq _closest_obstacle_distance (float __closest_obstacle_distance))
   (setq _total_clusters_count (round __total_clusters_count))
   (setq _avoidance_force_magnitude (float __avoidance_force_magnitude))
   (setq _computation_time (float __computation_time))
   (setq _full_cycle_time (float __full_cycle_time))
   self)
  (:robot_id
   (&optional __robot_id)
   (if __robot_id (setq _robot_id __robot_id)) _robot_id)
  (:trajectory_time
   (&optional __trajectory_time)
   (if __trajectory_time (setq _trajectory_time __trajectory_time)) _trajectory_time)
  (:ros_timestamp
   (&optional __ros_timestamp)
   (if __ros_timestamp (setq _ros_timestamp __ros_timestamp)) _ros_timestamp)
  (:xc
   (&optional __xc)
   (if __xc (setq _xc __xc)) _xc)
  (:yc
   (&optional __yc)
   (if __yc (setq _yc __yc)) _yc)
  (:thetac
   (&optional __thetac)
   (if __thetac (setq _thetac __thetac)) _thetac)
  (:vc
   (&optional __vc)
   (if __vc (setq _vc __vc)) _vc)
  (:wc
   (&optional __wc)
   (if __wc (setq _wc __wc)) _wc)
  (:xe
   (&optional __xe)
   (if __xe (setq _xe __xe)) _xe)
  (:ye
   (&optional __ye)
   (if __ye (setq _ye __ye)) _ye)
  (:thetae
   (&optional __thetae)
   (if __thetae (setq _thetae __thetae)) _thetae)
  (:xr
   (&optional __xr)
   (if __xr (setq _xr __xr)) _xr)
  (:yr
   (&optional __yr)
   (if __yr (setq _yr __yr)) _yr)
  (:zxeo_x
   (&optional __zxeo_x)
   (if __zxeo_x (setq _zxeo_x __zxeo_x)) _zxeo_x)
  (:zxeo_y
   (&optional __zxeo_y)
   (if __zxeo_y (setq _zxeo_y __zxeo_y)) _zxeo_y)
  (:raw_min_obstacle_distance
   (&optional __raw_min_obstacle_distance)
   (if __raw_min_obstacle_distance (setq _raw_min_obstacle_distance __raw_min_obstacle_distance)) _raw_min_obstacle_distance)
  (:closest_obstacle_distance
   (&optional __closest_obstacle_distance)
   (if __closest_obstacle_distance (setq _closest_obstacle_distance __closest_obstacle_distance)) _closest_obstacle_distance)
  (:total_clusters_count
   (&optional __total_clusters_count)
   (if __total_clusters_count (setq _total_clusters_count __total_clusters_count)) _total_clusters_count)
  (:avoidance_force_magnitude
   (&optional __avoidance_force_magnitude)
   (if __avoidance_force_magnitude (setq _avoidance_force_magnitude __avoidance_force_magnitude)) _avoidance_force_magnitude)
  (:computation_time
   (&optional __computation_time)
   (if __computation_time (setq _computation_time __computation_time)) _computation_time)
  (:full_cycle_time
   (&optional __full_cycle_time)
   (if __full_cycle_time (setq _full_cycle_time __full_cycle_time)) _full_cycle_time)
  (:serialization-length
   ()
   (+
    ;; int32 _robot_id
    4
    ;; float64 _trajectory_time
    8
    ;; float64 _ros_timestamp
    8
    ;; float64 _xc
    8
    ;; float64 _yc
    8
    ;; float64 _thetac
    8
    ;; float64 _vc
    8
    ;; float64 _wc
    8
    ;; float64 _xe
    8
    ;; float64 _ye
    8
    ;; float64 _thetae
    8
    ;; float64 _xr
    8
    ;; float64 _yr
    8
    ;; float64 _zxeo_x
    8
    ;; float64 _zxeo_y
    8
    ;; float64 _raw_min_obstacle_distance
    8
    ;; float64 _closest_obstacle_distance
    8
    ;; int32 _total_clusters_count
    4
    ;; float64 _avoidance_force_magnitude
    8
    ;; float64 _computation_time
    8
    ;; float64 _full_cycle_time
    8
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; int32 _robot_id
       (write-long _robot_id s)
     ;; float64 _trajectory_time
       (sys::poke _trajectory_time (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _ros_timestamp
       (sys::poke _ros_timestamp (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _xc
       (sys::poke _xc (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _yc
       (sys::poke _yc (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _thetac
       (sys::poke _thetac (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _vc
       (sys::poke _vc (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _wc
       (sys::poke _wc (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _xe
       (sys::poke _xe (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _ye
       (sys::poke _ye (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _thetae
       (sys::poke _thetae (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _xr
       (sys::poke _xr (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _yr
       (sys::poke _yr (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _zxeo_x
       (sys::poke _zxeo_x (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _zxeo_y
       (sys::poke _zxeo_y (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _raw_min_obstacle_distance
       (sys::poke _raw_min_obstacle_distance (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _closest_obstacle_distance
       (sys::poke _closest_obstacle_distance (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; int32 _total_clusters_count
       (write-long _total_clusters_count s)
     ;; float64 _avoidance_force_magnitude
       (sys::poke _avoidance_force_magnitude (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _computation_time
       (sys::poke _computation_time (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _full_cycle_time
       (sys::poke _full_cycle_time (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; int32 _robot_id
     (setq _robot_id (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; float64 _trajectory_time
     (setq _trajectory_time (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _ros_timestamp
     (setq _ros_timestamp (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _xc
     (setq _xc (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _yc
     (setq _yc (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _thetac
     (setq _thetac (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _vc
     (setq _vc (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _wc
     (setq _wc (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _xe
     (setq _xe (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _ye
     (setq _ye (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _thetae
     (setq _thetae (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _xr
     (setq _xr (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _yr
     (setq _yr (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _zxeo_x
     (setq _zxeo_x (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _zxeo_y
     (setq _zxeo_y (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _raw_min_obstacle_distance
     (setq _raw_min_obstacle_distance (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _closest_obstacle_distance
     (setq _closest_obstacle_distance (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; int32 _total_clusters_count
     (setq _total_clusters_count (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; float64 _avoidance_force_magnitude
     (setq _avoidance_force_magnitude (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _computation_time
     (setq _computation_time (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _full_cycle_time
     (setq _full_cycle_time (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;;
   self)
  )

(setf (get tb3_distributed_control::RobotHistoryData :md5sum-) "23ba331a962f095047cf39372dc8fff3")
(setf (get tb3_distributed_control::RobotHistoryData :datatype-) "tb3_distributed_control/RobotHistoryData")
(setf (get tb3_distributed_control::RobotHistoryData :definition-)
      "# ROS话题优化版本：机器人历史数据消息类型
# 设计目标：减少网络传输，提高实时性，降低roscore负载

# 机器人标识
int32 robot_id

# 时间戳信息
float64 trajectory_time    # 轨迹相对时间（从0开始）
float64 ros_timestamp     # ROS时间戳（用于数据时效性检查）

# 位置和姿态数据
float64 xc               # 当前x坐标
float64 yc               # 当前y坐标  
float64 thetac           # 当前航向角

# 控制输入数据
float64 vc               # 线速度
float64 wc               # 角速度

# 跟踪误差数据
float64 xe               # x方向误差
float64 ye               # y方向误差
float64 thetae           # 航向角误差

# 参考轨迹数据
float64 xr               # 参考x坐标
float64 yr               # 参考y坐标

# 观测器估计数据（对领导者位置的估计）
float64 zxeo_x           # 观测器估计的领导者X坐标
float64 zxeo_y           # 观测器估计的领导者Y坐标

# 避障相关数据（统一处理所有障碍物）
float64 raw_min_obstacle_distance   # 雷达原始数据的最小距离（直接从range获取）
float64 closest_obstacle_distance   # 最近障碍物点到参考点的距离（基于聚类分析）
int32 total_clusters_count          # 检测到的障碍物聚类总数
float64 avoidance_force_magnitude   # 避障力大小

# 性能分析数据
float64 computation_time  # 算法计算时间（秒）
float64 full_cycle_time  # 完整周期时间（秒）
")



(provide :tb3_distributed_control/RobotHistoryData "23ba331a962f095047cf39372dc8fff3")



; Auto-generated. Do not edit!


(cl:in-package tb3_distributed_control-msg)


;//! \htmlinclude RobotHistoryData.msg.html

(cl:defclass <RobotHistoryData> (roslisp-msg-protocol:ros-message)
  ((robot_id
    :reader robot_id
    :initarg :robot_id
    :type cl:integer
    :initform 0)
   (trajectory_time
    :reader trajectory_time
    :initarg :trajectory_time
    :type cl:float
    :initform 0.0)
   (ros_timestamp
    :reader ros_timestamp
    :initarg :ros_timestamp
    :type cl:float
    :initform 0.0)
   (xc
    :reader xc
    :initarg :xc
    :type cl:float
    :initform 0.0)
   (yc
    :reader yc
    :initarg :yc
    :type cl:float
    :initform 0.0)
   (thetac
    :reader thetac
    :initarg :thetac
    :type cl:float
    :initform 0.0)
   (vc
    :reader vc
    :initarg :vc
    :type cl:float
    :initform 0.0)
   (wc
    :reader wc
    :initarg :wc
    :type cl:float
    :initform 0.0)
   (xe
    :reader xe
    :initarg :xe
    :type cl:float
    :initform 0.0)
   (ye
    :reader ye
    :initarg :ye
    :type cl:float
    :initform 0.0)
   (thetae
    :reader thetae
    :initarg :thetae
    :type cl:float
    :initform 0.0)
   (xr
    :reader xr
    :initarg :xr
    :type cl:float
    :initform 0.0)
   (yr
    :reader yr
    :initarg :yr
    :type cl:float
    :initform 0.0)
   (zxeo_x
    :reader zxeo_x
    :initarg :zxeo_x
    :type cl:float
    :initform 0.0)
   (zxeo_y
    :reader zxeo_y
    :initarg :zxeo_y
    :type cl:float
    :initform 0.0)
   (raw_min_obstacle_distance
    :reader raw_min_obstacle_distance
    :initarg :raw_min_obstacle_distance
    :type cl:float
    :initform 0.0)
   (closest_obstacle_distance
    :reader closest_obstacle_distance
    :initarg :closest_obstacle_distance
    :type cl:float
    :initform 0.0)
   (total_clusters_count
    :reader total_clusters_count
    :initarg :total_clusters_count
    :type cl:integer
    :initform 0)
   (avoidance_force_magnitude
    :reader avoidance_force_magnitude
    :initarg :avoidance_force_magnitude
    :type cl:float
    :initform 0.0)
   (computation_time
    :reader computation_time
    :initarg :computation_time
    :type cl:float
    :initform 0.0)
   (full_cycle_time
    :reader full_cycle_time
    :initarg :full_cycle_time
    :type cl:float
    :initform 0.0))
)

(cl:defclass RobotHistoryData (<RobotHistoryData>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <RobotHistoryData>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'RobotHistoryData)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name tb3_distributed_control-msg:<RobotHistoryData> is deprecated: use tb3_distributed_control-msg:RobotHistoryData instead.")))

(cl:ensure-generic-function 'robot_id-val :lambda-list '(m))
(cl:defmethod robot_id-val ((m <RobotHistoryData>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader tb3_distributed_control-msg:robot_id-val is deprecated.  Use tb3_distributed_control-msg:robot_id instead.")
  (robot_id m))

(cl:ensure-generic-function 'trajectory_time-val :lambda-list '(m))
(cl:defmethod trajectory_time-val ((m <RobotHistoryData>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader tb3_distributed_control-msg:trajectory_time-val is deprecated.  Use tb3_distributed_control-msg:trajectory_time instead.")
  (trajectory_time m))

(cl:ensure-generic-function 'ros_timestamp-val :lambda-list '(m))
(cl:defmethod ros_timestamp-val ((m <RobotHistoryData>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader tb3_distributed_control-msg:ros_timestamp-val is deprecated.  Use tb3_distributed_control-msg:ros_timestamp instead.")
  (ros_timestamp m))

(cl:ensure-generic-function 'xc-val :lambda-list '(m))
(cl:defmethod xc-val ((m <RobotHistoryData>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader tb3_distributed_control-msg:xc-val is deprecated.  Use tb3_distributed_control-msg:xc instead.")
  (xc m))

(cl:ensure-generic-function 'yc-val :lambda-list '(m))
(cl:defmethod yc-val ((m <RobotHistoryData>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader tb3_distributed_control-msg:yc-val is deprecated.  Use tb3_distributed_control-msg:yc instead.")
  (yc m))

(cl:ensure-generic-function 'thetac-val :lambda-list '(m))
(cl:defmethod thetac-val ((m <RobotHistoryData>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader tb3_distributed_control-msg:thetac-val is deprecated.  Use tb3_distributed_control-msg:thetac instead.")
  (thetac m))

(cl:ensure-generic-function 'vc-val :lambda-list '(m))
(cl:defmethod vc-val ((m <RobotHistoryData>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader tb3_distributed_control-msg:vc-val is deprecated.  Use tb3_distributed_control-msg:vc instead.")
  (vc m))

(cl:ensure-generic-function 'wc-val :lambda-list '(m))
(cl:defmethod wc-val ((m <RobotHistoryData>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader tb3_distributed_control-msg:wc-val is deprecated.  Use tb3_distributed_control-msg:wc instead.")
  (wc m))

(cl:ensure-generic-function 'xe-val :lambda-list '(m))
(cl:defmethod xe-val ((m <RobotHistoryData>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader tb3_distributed_control-msg:xe-val is deprecated.  Use tb3_distributed_control-msg:xe instead.")
  (xe m))

(cl:ensure-generic-function 'ye-val :lambda-list '(m))
(cl:defmethod ye-val ((m <RobotHistoryData>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader tb3_distributed_control-msg:ye-val is deprecated.  Use tb3_distributed_control-msg:ye instead.")
  (ye m))

(cl:ensure-generic-function 'thetae-val :lambda-list '(m))
(cl:defmethod thetae-val ((m <RobotHistoryData>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader tb3_distributed_control-msg:thetae-val is deprecated.  Use tb3_distributed_control-msg:thetae instead.")
  (thetae m))

(cl:ensure-generic-function 'xr-val :lambda-list '(m))
(cl:defmethod xr-val ((m <RobotHistoryData>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader tb3_distributed_control-msg:xr-val is deprecated.  Use tb3_distributed_control-msg:xr instead.")
  (xr m))

(cl:ensure-generic-function 'yr-val :lambda-list '(m))
(cl:defmethod yr-val ((m <RobotHistoryData>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader tb3_distributed_control-msg:yr-val is deprecated.  Use tb3_distributed_control-msg:yr instead.")
  (yr m))

(cl:ensure-generic-function 'zxeo_x-val :lambda-list '(m))
(cl:defmethod zxeo_x-val ((m <RobotHistoryData>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader tb3_distributed_control-msg:zxeo_x-val is deprecated.  Use tb3_distributed_control-msg:zxeo_x instead.")
  (zxeo_x m))

(cl:ensure-generic-function 'zxeo_y-val :lambda-list '(m))
(cl:defmethod zxeo_y-val ((m <RobotHistoryData>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader tb3_distributed_control-msg:zxeo_y-val is deprecated.  Use tb3_distributed_control-msg:zxeo_y instead.")
  (zxeo_y m))

(cl:ensure-generic-function 'raw_min_obstacle_distance-val :lambda-list '(m))
(cl:defmethod raw_min_obstacle_distance-val ((m <RobotHistoryData>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader tb3_distributed_control-msg:raw_min_obstacle_distance-val is deprecated.  Use tb3_distributed_control-msg:raw_min_obstacle_distance instead.")
  (raw_min_obstacle_distance m))

(cl:ensure-generic-function 'closest_obstacle_distance-val :lambda-list '(m))
(cl:defmethod closest_obstacle_distance-val ((m <RobotHistoryData>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader tb3_distributed_control-msg:closest_obstacle_distance-val is deprecated.  Use tb3_distributed_control-msg:closest_obstacle_distance instead.")
  (closest_obstacle_distance m))

(cl:ensure-generic-function 'total_clusters_count-val :lambda-list '(m))
(cl:defmethod total_clusters_count-val ((m <RobotHistoryData>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader tb3_distributed_control-msg:total_clusters_count-val is deprecated.  Use tb3_distributed_control-msg:total_clusters_count instead.")
  (total_clusters_count m))

(cl:ensure-generic-function 'avoidance_force_magnitude-val :lambda-list '(m))
(cl:defmethod avoidance_force_magnitude-val ((m <RobotHistoryData>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader tb3_distributed_control-msg:avoidance_force_magnitude-val is deprecated.  Use tb3_distributed_control-msg:avoidance_force_magnitude instead.")
  (avoidance_force_magnitude m))

(cl:ensure-generic-function 'computation_time-val :lambda-list '(m))
(cl:defmethod computation_time-val ((m <RobotHistoryData>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader tb3_distributed_control-msg:computation_time-val is deprecated.  Use tb3_distributed_control-msg:computation_time instead.")
  (computation_time m))

(cl:ensure-generic-function 'full_cycle_time-val :lambda-list '(m))
(cl:defmethod full_cycle_time-val ((m <RobotHistoryData>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader tb3_distributed_control-msg:full_cycle_time-val is deprecated.  Use tb3_distributed_control-msg:full_cycle_time instead.")
  (full_cycle_time m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <RobotHistoryData>) ostream)
  "Serializes a message object of type '<RobotHistoryData>"
  (cl:let* ((signed (cl:slot-value msg 'robot_id)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'trajectory_time))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'ros_timestamp))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'xc))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'yc))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'thetac))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'vc))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'wc))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'xe))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'ye))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'thetae))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'xr))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'yr))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'zxeo_x))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'zxeo_y))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'raw_min_obstacle_distance))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'closest_obstacle_distance))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:let* ((signed (cl:slot-value msg 'total_clusters_count)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'avoidance_force_magnitude))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'computation_time))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'full_cycle_time))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <RobotHistoryData>) istream)
  "Deserializes a message object of type '<RobotHistoryData>"
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'robot_id) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'trajectory_time) (roslisp-utils:decode-double-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'ros_timestamp) (roslisp-utils:decode-double-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'xc) (roslisp-utils:decode-double-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'yc) (roslisp-utils:decode-double-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'thetac) (roslisp-utils:decode-double-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'vc) (roslisp-utils:decode-double-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'wc) (roslisp-utils:decode-double-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'xe) (roslisp-utils:decode-double-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'ye) (roslisp-utils:decode-double-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'thetae) (roslisp-utils:decode-double-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'xr) (roslisp-utils:decode-double-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'yr) (roslisp-utils:decode-double-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'zxeo_x) (roslisp-utils:decode-double-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'zxeo_y) (roslisp-utils:decode-double-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'raw_min_obstacle_distance) (roslisp-utils:decode-double-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'closest_obstacle_distance) (roslisp-utils:decode-double-float-bits bits)))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'total_clusters_count) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'avoidance_force_magnitude) (roslisp-utils:decode-double-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'computation_time) (roslisp-utils:decode-double-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'full_cycle_time) (roslisp-utils:decode-double-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<RobotHistoryData>)))
  "Returns string type for a message object of type '<RobotHistoryData>"
  "tb3_distributed_control/RobotHistoryData")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'RobotHistoryData)))
  "Returns string type for a message object of type 'RobotHistoryData"
  "tb3_distributed_control/RobotHistoryData")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<RobotHistoryData>)))
  "Returns md5sum for a message object of type '<RobotHistoryData>"
  "23ba331a962f095047cf39372dc8fff3")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'RobotHistoryData)))
  "Returns md5sum for a message object of type 'RobotHistoryData"
  "23ba331a962f095047cf39372dc8fff3")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<RobotHistoryData>)))
  "Returns full string definition for message of type '<RobotHistoryData>"
  (cl:format cl:nil "# ROS话题优化版本：机器人历史数据消息类型~%# 设计目标：减少网络传输，提高实时性，降低roscore负载~%~%# 机器人标识~%int32 robot_id~%~%# 时间戳信息~%float64 trajectory_time    # 轨迹相对时间（从0开始）~%float64 ros_timestamp     # ROS时间戳（用于数据时效性检查）~%~%# 位置和姿态数据~%float64 xc               # 当前x坐标~%float64 yc               # 当前y坐标  ~%float64 thetac           # 当前航向角~%~%# 控制输入数据~%float64 vc               # 线速度~%float64 wc               # 角速度~%~%# 跟踪误差数据~%float64 xe               # x方向误差~%float64 ye               # y方向误差~%float64 thetae           # 航向角误差~%~%# 参考轨迹数据~%float64 xr               # 参考x坐标~%float64 yr               # 参考y坐标~%~%# 观测器估计数据（对领导者位置的估计）~%float64 zxeo_x           # 观测器估计的领导者X坐标~%float64 zxeo_y           # 观测器估计的领导者Y坐标~%~%# 避障相关数据（统一处理所有障碍物）~%float64 raw_min_obstacle_distance   # 雷达原始数据的最小距离（直接从range获取）~%float64 closest_obstacle_distance   # 最近障碍物点到参考点的距离（基于聚类分析）~%int32 total_clusters_count          # 检测到的障碍物聚类总数~%float64 avoidance_force_magnitude   # 避障力大小~%~%# 性能分析数据~%float64 computation_time  # 算法计算时间（秒）~%float64 full_cycle_time  # 完整周期时间（秒）~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'RobotHistoryData)))
  "Returns full string definition for message of type 'RobotHistoryData"
  (cl:format cl:nil "# ROS话题优化版本：机器人历史数据消息类型~%# 设计目标：减少网络传输，提高实时性，降低roscore负载~%~%# 机器人标识~%int32 robot_id~%~%# 时间戳信息~%float64 trajectory_time    # 轨迹相对时间（从0开始）~%float64 ros_timestamp     # ROS时间戳（用于数据时效性检查）~%~%# 位置和姿态数据~%float64 xc               # 当前x坐标~%float64 yc               # 当前y坐标  ~%float64 thetac           # 当前航向角~%~%# 控制输入数据~%float64 vc               # 线速度~%float64 wc               # 角速度~%~%# 跟踪误差数据~%float64 xe               # x方向误差~%float64 ye               # y方向误差~%float64 thetae           # 航向角误差~%~%# 参考轨迹数据~%float64 xr               # 参考x坐标~%float64 yr               # 参考y坐标~%~%# 观测器估计数据（对领导者位置的估计）~%float64 zxeo_x           # 观测器估计的领导者X坐标~%float64 zxeo_y           # 观测器估计的领导者Y坐标~%~%# 避障相关数据（统一处理所有障碍物）~%float64 raw_min_obstacle_distance   # 雷达原始数据的最小距离（直接从range获取）~%float64 closest_obstacle_distance   # 最近障碍物点到参考点的距离（基于聚类分析）~%int32 total_clusters_count          # 检测到的障碍物聚类总数~%float64 avoidance_force_magnitude   # 避障力大小~%~%# 性能分析数据~%float64 computation_time  # 算法计算时间（秒）~%float64 full_cycle_time  # 完整周期时间（秒）~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <RobotHistoryData>))
  (cl:+ 0
     4
     8
     8
     8
     8
     8
     8
     8
     8
     8
     8
     8
     8
     8
     8
     8
     8
     4
     8
     8
     8
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <RobotHistoryData>))
  "Converts a ROS message object to a list"
  (cl:list 'RobotHistoryData
    (cl:cons ':robot_id (robot_id msg))
    (cl:cons ':trajectory_time (trajectory_time msg))
    (cl:cons ':ros_timestamp (ros_timestamp msg))
    (cl:cons ':xc (xc msg))
    (cl:cons ':yc (yc msg))
    (cl:cons ':thetac (thetac msg))
    (cl:cons ':vc (vc msg))
    (cl:cons ':wc (wc msg))
    (cl:cons ':xe (xe msg))
    (cl:cons ':ye (ye msg))
    (cl:cons ':thetae (thetae msg))
    (cl:cons ':xr (xr msg))
    (cl:cons ':yr (yr msg))
    (cl:cons ':zxeo_x (zxeo_x msg))
    (cl:cons ':zxeo_y (zxeo_y msg))
    (cl:cons ':raw_min_obstacle_distance (raw_min_obstacle_distance msg))
    (cl:cons ':closest_obstacle_distance (closest_obstacle_distance msg))
    (cl:cons ':total_clusters_count (total_clusters_count msg))
    (cl:cons ':avoidance_force_magnitude (avoidance_force_magnitude msg))
    (cl:cons ':computation_time (computation_time msg))
    (cl:cons ':full_cycle_time (full_cycle_time msg))
))

; Auto-generated. Do not edit!


(cl:in-package tb3_distributed_control-msg)


;//! \htmlinclude LeaderHistoryData.msg.html

(cl:defclass <LeaderHistoryData> (roslisp-msg-protocol:ros-message)
  ((trajectory_time
    :reader trajectory_time
    :initarg :trajectory_time
    :type cl:float
    :initform 0.0)
   (ros_timestamp
    :reader ros_timestamp
    :initarg :ros_timestamp
    :type cl:float
    :initform 0.0)
   (x0
    :reader x0
    :initarg :x0
    :type cl:float
    :initform 0.0)
   (y0
    :reader y0
    :initarg :y0
    :type cl:float
    :initform 0.0)
   (theta0
    :reader theta0
    :initarg :theta0
    :type cl:float
    :initform 0.0)
   (v0
    :reader v0
    :initarg :v0
    :type cl:float
    :initform 0.0)
   (w0
    :reader w0
    :initarg :w0
    :type cl:float
    :initform 0.0)
   (u0x
    :reader u0x
    :initarg :u0x
    :type cl:float
    :initform 0.0)
   (u0y
    :reader u0y
    :initarg :u0y
    :type cl:float
    :initform 0.0))
)

(cl:defclass LeaderHistoryData (<LeaderHistoryData>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <LeaderHistoryData>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'LeaderHistoryData)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name tb3_distributed_control-msg:<LeaderHistoryData> is deprecated: use tb3_distributed_control-msg:LeaderHistoryData instead.")))

(cl:ensure-generic-function 'trajectory_time-val :lambda-list '(m))
(cl:defmethod trajectory_time-val ((m <LeaderHistoryData>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader tb3_distributed_control-msg:trajectory_time-val is deprecated.  Use tb3_distributed_control-msg:trajectory_time instead.")
  (trajectory_time m))

(cl:ensure-generic-function 'ros_timestamp-val :lambda-list '(m))
(cl:defmethod ros_timestamp-val ((m <LeaderHistoryData>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader tb3_distributed_control-msg:ros_timestamp-val is deprecated.  Use tb3_distributed_control-msg:ros_timestamp instead.")
  (ros_timestamp m))

(cl:ensure-generic-function 'x0-val :lambda-list '(m))
(cl:defmethod x0-val ((m <LeaderHistoryData>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader tb3_distributed_control-msg:x0-val is deprecated.  Use tb3_distributed_control-msg:x0 instead.")
  (x0 m))

(cl:ensure-generic-function 'y0-val :lambda-list '(m))
(cl:defmethod y0-val ((m <LeaderHistoryData>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader tb3_distributed_control-msg:y0-val is deprecated.  Use tb3_distributed_control-msg:y0 instead.")
  (y0 m))

(cl:ensure-generic-function 'theta0-val :lambda-list '(m))
(cl:defmethod theta0-val ((m <LeaderHistoryData>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader tb3_distributed_control-msg:theta0-val is deprecated.  Use tb3_distributed_control-msg:theta0 instead.")
  (theta0 m))

(cl:ensure-generic-function 'v0-val :lambda-list '(m))
(cl:defmethod v0-val ((m <LeaderHistoryData>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader tb3_distributed_control-msg:v0-val is deprecated.  Use tb3_distributed_control-msg:v0 instead.")
  (v0 m))

(cl:ensure-generic-function 'w0-val :lambda-list '(m))
(cl:defmethod w0-val ((m <LeaderHistoryData>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader tb3_distributed_control-msg:w0-val is deprecated.  Use tb3_distributed_control-msg:w0 instead.")
  (w0 m))

(cl:ensure-generic-function 'u0x-val :lambda-list '(m))
(cl:defmethod u0x-val ((m <LeaderHistoryData>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader tb3_distributed_control-msg:u0x-val is deprecated.  Use tb3_distributed_control-msg:u0x instead.")
  (u0x m))

(cl:ensure-generic-function 'u0y-val :lambda-list '(m))
(cl:defmethod u0y-val ((m <LeaderHistoryData>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader tb3_distributed_control-msg:u0y-val is deprecated.  Use tb3_distributed_control-msg:u0y instead.")
  (u0y m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <LeaderHistoryData>) ostream)
  "Serializes a message object of type '<LeaderHistoryData>"
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
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'x0))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'y0))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'theta0))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'v0))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'w0))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'u0x))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'u0y))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <LeaderHistoryData>) istream)
  "Deserializes a message object of type '<LeaderHistoryData>"
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
    (cl:setf (cl:slot-value msg 'x0) (roslisp-utils:decode-double-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'y0) (roslisp-utils:decode-double-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'theta0) (roslisp-utils:decode-double-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'v0) (roslisp-utils:decode-double-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'w0) (roslisp-utils:decode-double-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'u0x) (roslisp-utils:decode-double-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'u0y) (roslisp-utils:decode-double-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<LeaderHistoryData>)))
  "Returns string type for a message object of type '<LeaderHistoryData>"
  "tb3_distributed_control/LeaderHistoryData")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'LeaderHistoryData)))
  "Returns string type for a message object of type 'LeaderHistoryData"
  "tb3_distributed_control/LeaderHistoryData")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<LeaderHistoryData>)))
  "Returns md5sum for a message object of type '<LeaderHistoryData>"
  "e13ef0559dc1ccb0a5a11bd1a53b8ab3")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'LeaderHistoryData)))
  "Returns md5sum for a message object of type 'LeaderHistoryData"
  "e13ef0559dc1ccb0a5a11bd1a53b8ab3")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<LeaderHistoryData>)))
  "Returns full string definition for message of type '<LeaderHistoryData>"
  (cl:format cl:nil "# ROS话题优化版本：领导者历史数据消息类型~%~%# 时间戳信息~%float64 trajectory_time    # 轨迹相对时间（从0开始）~%float64 ros_timestamp     # ROS时间戳~%~%# 位置和姿态数据  ~%float64 x0               # 领导者x坐标~%float64 y0               # 领导者y坐标~%float64 theta0           # 领导者航向角~%~%# 速度数据~%float64 v0               # 线速度~%float64 w0               # 角速度~%float64 u0x              # x方向速度分量~%float64 u0y              # y方向速度分量~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'LeaderHistoryData)))
  "Returns full string definition for message of type 'LeaderHistoryData"
  (cl:format cl:nil "# ROS话题优化版本：领导者历史数据消息类型~%~%# 时间戳信息~%float64 trajectory_time    # 轨迹相对时间（从0开始）~%float64 ros_timestamp     # ROS时间戳~%~%# 位置和姿态数据  ~%float64 x0               # 领导者x坐标~%float64 y0               # 领导者y坐标~%float64 theta0           # 领导者航向角~%~%# 速度数据~%float64 v0               # 线速度~%float64 w0               # 角速度~%float64 u0x              # x方向速度分量~%float64 u0y              # y方向速度分量~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <LeaderHistoryData>))
  (cl:+ 0
     8
     8
     8
     8
     8
     8
     8
     8
     8
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <LeaderHistoryData>))
  "Converts a ROS message object to a list"
  (cl:list 'LeaderHistoryData
    (cl:cons ':trajectory_time (trajectory_time msg))
    (cl:cons ':ros_timestamp (ros_timestamp msg))
    (cl:cons ':x0 (x0 msg))
    (cl:cons ':y0 (y0 msg))
    (cl:cons ':theta0 (theta0 msg))
    (cl:cons ':v0 (v0 msg))
    (cl:cons ':w0 (w0 msg))
    (cl:cons ':u0x (u0x msg))
    (cl:cons ':u0y (u0y msg))
))

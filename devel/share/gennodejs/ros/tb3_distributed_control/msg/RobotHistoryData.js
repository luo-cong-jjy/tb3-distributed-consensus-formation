// Auto-generated. Do not edit!

// (in-package tb3_distributed_control.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class RobotHistoryData {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.robot_id = null;
      this.trajectory_time = null;
      this.ros_timestamp = null;
      this.xc = null;
      this.yc = null;
      this.thetac = null;
      this.vc = null;
      this.wc = null;
      this.xe = null;
      this.ye = null;
      this.thetae = null;
      this.xr = null;
      this.yr = null;
      this.zxeo_x = null;
      this.zxeo_y = null;
      this.raw_min_obstacle_distance = null;
      this.closest_obstacle_distance = null;
      this.total_clusters_count = null;
      this.avoidance_force_magnitude = null;
      this.computation_time = null;
      this.full_cycle_time = null;
    }
    else {
      if (initObj.hasOwnProperty('robot_id')) {
        this.robot_id = initObj.robot_id
      }
      else {
        this.robot_id = 0;
      }
      if (initObj.hasOwnProperty('trajectory_time')) {
        this.trajectory_time = initObj.trajectory_time
      }
      else {
        this.trajectory_time = 0.0;
      }
      if (initObj.hasOwnProperty('ros_timestamp')) {
        this.ros_timestamp = initObj.ros_timestamp
      }
      else {
        this.ros_timestamp = 0.0;
      }
      if (initObj.hasOwnProperty('xc')) {
        this.xc = initObj.xc
      }
      else {
        this.xc = 0.0;
      }
      if (initObj.hasOwnProperty('yc')) {
        this.yc = initObj.yc
      }
      else {
        this.yc = 0.0;
      }
      if (initObj.hasOwnProperty('thetac')) {
        this.thetac = initObj.thetac
      }
      else {
        this.thetac = 0.0;
      }
      if (initObj.hasOwnProperty('vc')) {
        this.vc = initObj.vc
      }
      else {
        this.vc = 0.0;
      }
      if (initObj.hasOwnProperty('wc')) {
        this.wc = initObj.wc
      }
      else {
        this.wc = 0.0;
      }
      if (initObj.hasOwnProperty('xe')) {
        this.xe = initObj.xe
      }
      else {
        this.xe = 0.0;
      }
      if (initObj.hasOwnProperty('ye')) {
        this.ye = initObj.ye
      }
      else {
        this.ye = 0.0;
      }
      if (initObj.hasOwnProperty('thetae')) {
        this.thetae = initObj.thetae
      }
      else {
        this.thetae = 0.0;
      }
      if (initObj.hasOwnProperty('xr')) {
        this.xr = initObj.xr
      }
      else {
        this.xr = 0.0;
      }
      if (initObj.hasOwnProperty('yr')) {
        this.yr = initObj.yr
      }
      else {
        this.yr = 0.0;
      }
      if (initObj.hasOwnProperty('zxeo_x')) {
        this.zxeo_x = initObj.zxeo_x
      }
      else {
        this.zxeo_x = 0.0;
      }
      if (initObj.hasOwnProperty('zxeo_y')) {
        this.zxeo_y = initObj.zxeo_y
      }
      else {
        this.zxeo_y = 0.0;
      }
      if (initObj.hasOwnProperty('raw_min_obstacle_distance')) {
        this.raw_min_obstacle_distance = initObj.raw_min_obstacle_distance
      }
      else {
        this.raw_min_obstacle_distance = 0.0;
      }
      if (initObj.hasOwnProperty('closest_obstacle_distance')) {
        this.closest_obstacle_distance = initObj.closest_obstacle_distance
      }
      else {
        this.closest_obstacle_distance = 0.0;
      }
      if (initObj.hasOwnProperty('total_clusters_count')) {
        this.total_clusters_count = initObj.total_clusters_count
      }
      else {
        this.total_clusters_count = 0;
      }
      if (initObj.hasOwnProperty('avoidance_force_magnitude')) {
        this.avoidance_force_magnitude = initObj.avoidance_force_magnitude
      }
      else {
        this.avoidance_force_magnitude = 0.0;
      }
      if (initObj.hasOwnProperty('computation_time')) {
        this.computation_time = initObj.computation_time
      }
      else {
        this.computation_time = 0.0;
      }
      if (initObj.hasOwnProperty('full_cycle_time')) {
        this.full_cycle_time = initObj.full_cycle_time
      }
      else {
        this.full_cycle_time = 0.0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type RobotHistoryData
    // Serialize message field [robot_id]
    bufferOffset = _serializer.int32(obj.robot_id, buffer, bufferOffset);
    // Serialize message field [trajectory_time]
    bufferOffset = _serializer.float64(obj.trajectory_time, buffer, bufferOffset);
    // Serialize message field [ros_timestamp]
    bufferOffset = _serializer.float64(obj.ros_timestamp, buffer, bufferOffset);
    // Serialize message field [xc]
    bufferOffset = _serializer.float64(obj.xc, buffer, bufferOffset);
    // Serialize message field [yc]
    bufferOffset = _serializer.float64(obj.yc, buffer, bufferOffset);
    // Serialize message field [thetac]
    bufferOffset = _serializer.float64(obj.thetac, buffer, bufferOffset);
    // Serialize message field [vc]
    bufferOffset = _serializer.float64(obj.vc, buffer, bufferOffset);
    // Serialize message field [wc]
    bufferOffset = _serializer.float64(obj.wc, buffer, bufferOffset);
    // Serialize message field [xe]
    bufferOffset = _serializer.float64(obj.xe, buffer, bufferOffset);
    // Serialize message field [ye]
    bufferOffset = _serializer.float64(obj.ye, buffer, bufferOffset);
    // Serialize message field [thetae]
    bufferOffset = _serializer.float64(obj.thetae, buffer, bufferOffset);
    // Serialize message field [xr]
    bufferOffset = _serializer.float64(obj.xr, buffer, bufferOffset);
    // Serialize message field [yr]
    bufferOffset = _serializer.float64(obj.yr, buffer, bufferOffset);
    // Serialize message field [zxeo_x]
    bufferOffset = _serializer.float64(obj.zxeo_x, buffer, bufferOffset);
    // Serialize message field [zxeo_y]
    bufferOffset = _serializer.float64(obj.zxeo_y, buffer, bufferOffset);
    // Serialize message field [raw_min_obstacle_distance]
    bufferOffset = _serializer.float64(obj.raw_min_obstacle_distance, buffer, bufferOffset);
    // Serialize message field [closest_obstacle_distance]
    bufferOffset = _serializer.float64(obj.closest_obstacle_distance, buffer, bufferOffset);
    // Serialize message field [total_clusters_count]
    bufferOffset = _serializer.int32(obj.total_clusters_count, buffer, bufferOffset);
    // Serialize message field [avoidance_force_magnitude]
    bufferOffset = _serializer.float64(obj.avoidance_force_magnitude, buffer, bufferOffset);
    // Serialize message field [computation_time]
    bufferOffset = _serializer.float64(obj.computation_time, buffer, bufferOffset);
    // Serialize message field [full_cycle_time]
    bufferOffset = _serializer.float64(obj.full_cycle_time, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type RobotHistoryData
    let len;
    let data = new RobotHistoryData(null);
    // Deserialize message field [robot_id]
    data.robot_id = _deserializer.int32(buffer, bufferOffset);
    // Deserialize message field [trajectory_time]
    data.trajectory_time = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [ros_timestamp]
    data.ros_timestamp = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [xc]
    data.xc = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [yc]
    data.yc = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [thetac]
    data.thetac = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [vc]
    data.vc = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [wc]
    data.wc = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [xe]
    data.xe = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [ye]
    data.ye = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [thetae]
    data.thetae = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [xr]
    data.xr = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [yr]
    data.yr = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [zxeo_x]
    data.zxeo_x = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [zxeo_y]
    data.zxeo_y = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [raw_min_obstacle_distance]
    data.raw_min_obstacle_distance = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [closest_obstacle_distance]
    data.closest_obstacle_distance = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [total_clusters_count]
    data.total_clusters_count = _deserializer.int32(buffer, bufferOffset);
    // Deserialize message field [avoidance_force_magnitude]
    data.avoidance_force_magnitude = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [computation_time]
    data.computation_time = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [full_cycle_time]
    data.full_cycle_time = _deserializer.float64(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 160;
  }

  static datatype() {
    // Returns string type for a message object
    return 'tb3_distributed_control/RobotHistoryData';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '23ba331a962f095047cf39372dc8fff3';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    # ROS话题优化版本：机器人历史数据消息类型
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
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new RobotHistoryData(null);
    if (msg.robot_id !== undefined) {
      resolved.robot_id = msg.robot_id;
    }
    else {
      resolved.robot_id = 0
    }

    if (msg.trajectory_time !== undefined) {
      resolved.trajectory_time = msg.trajectory_time;
    }
    else {
      resolved.trajectory_time = 0.0
    }

    if (msg.ros_timestamp !== undefined) {
      resolved.ros_timestamp = msg.ros_timestamp;
    }
    else {
      resolved.ros_timestamp = 0.0
    }

    if (msg.xc !== undefined) {
      resolved.xc = msg.xc;
    }
    else {
      resolved.xc = 0.0
    }

    if (msg.yc !== undefined) {
      resolved.yc = msg.yc;
    }
    else {
      resolved.yc = 0.0
    }

    if (msg.thetac !== undefined) {
      resolved.thetac = msg.thetac;
    }
    else {
      resolved.thetac = 0.0
    }

    if (msg.vc !== undefined) {
      resolved.vc = msg.vc;
    }
    else {
      resolved.vc = 0.0
    }

    if (msg.wc !== undefined) {
      resolved.wc = msg.wc;
    }
    else {
      resolved.wc = 0.0
    }

    if (msg.xe !== undefined) {
      resolved.xe = msg.xe;
    }
    else {
      resolved.xe = 0.0
    }

    if (msg.ye !== undefined) {
      resolved.ye = msg.ye;
    }
    else {
      resolved.ye = 0.0
    }

    if (msg.thetae !== undefined) {
      resolved.thetae = msg.thetae;
    }
    else {
      resolved.thetae = 0.0
    }

    if (msg.xr !== undefined) {
      resolved.xr = msg.xr;
    }
    else {
      resolved.xr = 0.0
    }

    if (msg.yr !== undefined) {
      resolved.yr = msg.yr;
    }
    else {
      resolved.yr = 0.0
    }

    if (msg.zxeo_x !== undefined) {
      resolved.zxeo_x = msg.zxeo_x;
    }
    else {
      resolved.zxeo_x = 0.0
    }

    if (msg.zxeo_y !== undefined) {
      resolved.zxeo_y = msg.zxeo_y;
    }
    else {
      resolved.zxeo_y = 0.0
    }

    if (msg.raw_min_obstacle_distance !== undefined) {
      resolved.raw_min_obstacle_distance = msg.raw_min_obstacle_distance;
    }
    else {
      resolved.raw_min_obstacle_distance = 0.0
    }

    if (msg.closest_obstacle_distance !== undefined) {
      resolved.closest_obstacle_distance = msg.closest_obstacle_distance;
    }
    else {
      resolved.closest_obstacle_distance = 0.0
    }

    if (msg.total_clusters_count !== undefined) {
      resolved.total_clusters_count = msg.total_clusters_count;
    }
    else {
      resolved.total_clusters_count = 0
    }

    if (msg.avoidance_force_magnitude !== undefined) {
      resolved.avoidance_force_magnitude = msg.avoidance_force_magnitude;
    }
    else {
      resolved.avoidance_force_magnitude = 0.0
    }

    if (msg.computation_time !== undefined) {
      resolved.computation_time = msg.computation_time;
    }
    else {
      resolved.computation_time = 0.0
    }

    if (msg.full_cycle_time !== undefined) {
      resolved.full_cycle_time = msg.full_cycle_time;
    }
    else {
      resolved.full_cycle_time = 0.0
    }

    return resolved;
    }
};

module.exports = RobotHistoryData;

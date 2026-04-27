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

class LeaderHistoryData {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.trajectory_time = null;
      this.ros_timestamp = null;
      this.x0 = null;
      this.y0 = null;
      this.theta0 = null;
      this.v0 = null;
      this.w0 = null;
      this.u0x = null;
      this.u0y = null;
    }
    else {
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
      if (initObj.hasOwnProperty('x0')) {
        this.x0 = initObj.x0
      }
      else {
        this.x0 = 0.0;
      }
      if (initObj.hasOwnProperty('y0')) {
        this.y0 = initObj.y0
      }
      else {
        this.y0 = 0.0;
      }
      if (initObj.hasOwnProperty('theta0')) {
        this.theta0 = initObj.theta0
      }
      else {
        this.theta0 = 0.0;
      }
      if (initObj.hasOwnProperty('v0')) {
        this.v0 = initObj.v0
      }
      else {
        this.v0 = 0.0;
      }
      if (initObj.hasOwnProperty('w0')) {
        this.w0 = initObj.w0
      }
      else {
        this.w0 = 0.0;
      }
      if (initObj.hasOwnProperty('u0x')) {
        this.u0x = initObj.u0x
      }
      else {
        this.u0x = 0.0;
      }
      if (initObj.hasOwnProperty('u0y')) {
        this.u0y = initObj.u0y
      }
      else {
        this.u0y = 0.0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type LeaderHistoryData
    // Serialize message field [trajectory_time]
    bufferOffset = _serializer.float64(obj.trajectory_time, buffer, bufferOffset);
    // Serialize message field [ros_timestamp]
    bufferOffset = _serializer.float64(obj.ros_timestamp, buffer, bufferOffset);
    // Serialize message field [x0]
    bufferOffset = _serializer.float64(obj.x0, buffer, bufferOffset);
    // Serialize message field [y0]
    bufferOffset = _serializer.float64(obj.y0, buffer, bufferOffset);
    // Serialize message field [theta0]
    bufferOffset = _serializer.float64(obj.theta0, buffer, bufferOffset);
    // Serialize message field [v0]
    bufferOffset = _serializer.float64(obj.v0, buffer, bufferOffset);
    // Serialize message field [w0]
    bufferOffset = _serializer.float64(obj.w0, buffer, bufferOffset);
    // Serialize message field [u0x]
    bufferOffset = _serializer.float64(obj.u0x, buffer, bufferOffset);
    // Serialize message field [u0y]
    bufferOffset = _serializer.float64(obj.u0y, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type LeaderHistoryData
    let len;
    let data = new LeaderHistoryData(null);
    // Deserialize message field [trajectory_time]
    data.trajectory_time = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [ros_timestamp]
    data.ros_timestamp = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [x0]
    data.x0 = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [y0]
    data.y0 = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [theta0]
    data.theta0 = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [v0]
    data.v0 = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [w0]
    data.w0 = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [u0x]
    data.u0x = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [u0y]
    data.u0y = _deserializer.float64(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 72;
  }

  static datatype() {
    // Returns string type for a message object
    return 'tb3_distributed_control/LeaderHistoryData';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'e13ef0559dc1ccb0a5a11bd1a53b8ab3';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    # ROS话题优化版本：领导者历史数据消息类型
    
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
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new LeaderHistoryData(null);
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

    if (msg.x0 !== undefined) {
      resolved.x0 = msg.x0;
    }
    else {
      resolved.x0 = 0.0
    }

    if (msg.y0 !== undefined) {
      resolved.y0 = msg.y0;
    }
    else {
      resolved.y0 = 0.0
    }

    if (msg.theta0 !== undefined) {
      resolved.theta0 = msg.theta0;
    }
    else {
      resolved.theta0 = 0.0
    }

    if (msg.v0 !== undefined) {
      resolved.v0 = msg.v0;
    }
    else {
      resolved.v0 = 0.0
    }

    if (msg.w0 !== undefined) {
      resolved.w0 = msg.w0;
    }
    else {
      resolved.w0 = 0.0
    }

    if (msg.u0x !== undefined) {
      resolved.u0x = msg.u0x;
    }
    else {
      resolved.u0x = 0.0
    }

    if (msg.u0y !== undefined) {
      resolved.u0y = msg.u0y;
    }
    else {
      resolved.u0y = 0.0
    }

    return resolved;
    }
};

module.exports = LeaderHistoryData;

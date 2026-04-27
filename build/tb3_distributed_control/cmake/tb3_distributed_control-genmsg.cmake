# generated from genmsg/cmake/pkg-genmsg.cmake.em

message(STATUS "tb3_distributed_control: 2 messages, 0 services")

set(MSG_I_FLAGS "-Itb3_distributed_control:/home/gdut/24_LC/turtlebot3_distributed_consensus_formation_ws/src/tb3_distributed_control/msg;-Istd_msgs:/opt/ros/noetic/share/std_msgs/cmake/../msg;-Igeometry_msgs:/opt/ros/noetic/share/geometry_msgs/cmake/../msg;-Inav_msgs:/opt/ros/noetic/share/nav_msgs/cmake/../msg;-Isensor_msgs:/opt/ros/noetic/share/sensor_msgs/cmake/../msg;-Iactionlib_msgs:/opt/ros/noetic/share/actionlib_msgs/cmake/../msg")

# Find all generators
find_package(gencpp REQUIRED)
find_package(geneus REQUIRED)
find_package(genlisp REQUIRED)
find_package(gennodejs REQUIRED)
find_package(genpy REQUIRED)

add_custom_target(tb3_distributed_control_generate_messages ALL)

# verify that message/service dependencies have not changed since configure



get_filename_component(_filename "/home/gdut/24_LC/turtlebot3_distributed_consensus_formation_ws/src/tb3_distributed_control/msg/LeaderHistoryData.msg" NAME_WE)
add_custom_target(_tb3_distributed_control_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "tb3_distributed_control" "/home/gdut/24_LC/turtlebot3_distributed_consensus_formation_ws/src/tb3_distributed_control/msg/LeaderHistoryData.msg" ""
)

get_filename_component(_filename "/home/gdut/24_LC/turtlebot3_distributed_consensus_formation_ws/src/tb3_distributed_control/msg/RobotHistoryData.msg" NAME_WE)
add_custom_target(_tb3_distributed_control_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "tb3_distributed_control" "/home/gdut/24_LC/turtlebot3_distributed_consensus_formation_ws/src/tb3_distributed_control/msg/RobotHistoryData.msg" ""
)

#
#  langs = gencpp;geneus;genlisp;gennodejs;genpy
#

### Section generating for lang: gencpp
### Generating Messages
_generate_msg_cpp(tb3_distributed_control
  "/home/gdut/24_LC/turtlebot3_distributed_consensus_formation_ws/src/tb3_distributed_control/msg/LeaderHistoryData.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/tb3_distributed_control
)
_generate_msg_cpp(tb3_distributed_control
  "/home/gdut/24_LC/turtlebot3_distributed_consensus_formation_ws/src/tb3_distributed_control/msg/RobotHistoryData.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/tb3_distributed_control
)

### Generating Services

### Generating Module File
_generate_module_cpp(tb3_distributed_control
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/tb3_distributed_control
  "${ALL_GEN_OUTPUT_FILES_cpp}"
)

add_custom_target(tb3_distributed_control_generate_messages_cpp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_cpp}
)
add_dependencies(tb3_distributed_control_generate_messages tb3_distributed_control_generate_messages_cpp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/gdut/24_LC/turtlebot3_distributed_consensus_formation_ws/src/tb3_distributed_control/msg/LeaderHistoryData.msg" NAME_WE)
add_dependencies(tb3_distributed_control_generate_messages_cpp _tb3_distributed_control_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/gdut/24_LC/turtlebot3_distributed_consensus_formation_ws/src/tb3_distributed_control/msg/RobotHistoryData.msg" NAME_WE)
add_dependencies(tb3_distributed_control_generate_messages_cpp _tb3_distributed_control_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(tb3_distributed_control_gencpp)
add_dependencies(tb3_distributed_control_gencpp tb3_distributed_control_generate_messages_cpp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS tb3_distributed_control_generate_messages_cpp)

### Section generating for lang: geneus
### Generating Messages
_generate_msg_eus(tb3_distributed_control
  "/home/gdut/24_LC/turtlebot3_distributed_consensus_formation_ws/src/tb3_distributed_control/msg/LeaderHistoryData.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/tb3_distributed_control
)
_generate_msg_eus(tb3_distributed_control
  "/home/gdut/24_LC/turtlebot3_distributed_consensus_formation_ws/src/tb3_distributed_control/msg/RobotHistoryData.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/tb3_distributed_control
)

### Generating Services

### Generating Module File
_generate_module_eus(tb3_distributed_control
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/tb3_distributed_control
  "${ALL_GEN_OUTPUT_FILES_eus}"
)

add_custom_target(tb3_distributed_control_generate_messages_eus
  DEPENDS ${ALL_GEN_OUTPUT_FILES_eus}
)
add_dependencies(tb3_distributed_control_generate_messages tb3_distributed_control_generate_messages_eus)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/gdut/24_LC/turtlebot3_distributed_consensus_formation_ws/src/tb3_distributed_control/msg/LeaderHistoryData.msg" NAME_WE)
add_dependencies(tb3_distributed_control_generate_messages_eus _tb3_distributed_control_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/gdut/24_LC/turtlebot3_distributed_consensus_formation_ws/src/tb3_distributed_control/msg/RobotHistoryData.msg" NAME_WE)
add_dependencies(tb3_distributed_control_generate_messages_eus _tb3_distributed_control_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(tb3_distributed_control_geneus)
add_dependencies(tb3_distributed_control_geneus tb3_distributed_control_generate_messages_eus)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS tb3_distributed_control_generate_messages_eus)

### Section generating for lang: genlisp
### Generating Messages
_generate_msg_lisp(tb3_distributed_control
  "/home/gdut/24_LC/turtlebot3_distributed_consensus_formation_ws/src/tb3_distributed_control/msg/LeaderHistoryData.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/tb3_distributed_control
)
_generate_msg_lisp(tb3_distributed_control
  "/home/gdut/24_LC/turtlebot3_distributed_consensus_formation_ws/src/tb3_distributed_control/msg/RobotHistoryData.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/tb3_distributed_control
)

### Generating Services

### Generating Module File
_generate_module_lisp(tb3_distributed_control
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/tb3_distributed_control
  "${ALL_GEN_OUTPUT_FILES_lisp}"
)

add_custom_target(tb3_distributed_control_generate_messages_lisp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_lisp}
)
add_dependencies(tb3_distributed_control_generate_messages tb3_distributed_control_generate_messages_lisp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/gdut/24_LC/turtlebot3_distributed_consensus_formation_ws/src/tb3_distributed_control/msg/LeaderHistoryData.msg" NAME_WE)
add_dependencies(tb3_distributed_control_generate_messages_lisp _tb3_distributed_control_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/gdut/24_LC/turtlebot3_distributed_consensus_formation_ws/src/tb3_distributed_control/msg/RobotHistoryData.msg" NAME_WE)
add_dependencies(tb3_distributed_control_generate_messages_lisp _tb3_distributed_control_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(tb3_distributed_control_genlisp)
add_dependencies(tb3_distributed_control_genlisp tb3_distributed_control_generate_messages_lisp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS tb3_distributed_control_generate_messages_lisp)

### Section generating for lang: gennodejs
### Generating Messages
_generate_msg_nodejs(tb3_distributed_control
  "/home/gdut/24_LC/turtlebot3_distributed_consensus_formation_ws/src/tb3_distributed_control/msg/LeaderHistoryData.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/tb3_distributed_control
)
_generate_msg_nodejs(tb3_distributed_control
  "/home/gdut/24_LC/turtlebot3_distributed_consensus_formation_ws/src/tb3_distributed_control/msg/RobotHistoryData.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/tb3_distributed_control
)

### Generating Services

### Generating Module File
_generate_module_nodejs(tb3_distributed_control
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/tb3_distributed_control
  "${ALL_GEN_OUTPUT_FILES_nodejs}"
)

add_custom_target(tb3_distributed_control_generate_messages_nodejs
  DEPENDS ${ALL_GEN_OUTPUT_FILES_nodejs}
)
add_dependencies(tb3_distributed_control_generate_messages tb3_distributed_control_generate_messages_nodejs)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/gdut/24_LC/turtlebot3_distributed_consensus_formation_ws/src/tb3_distributed_control/msg/LeaderHistoryData.msg" NAME_WE)
add_dependencies(tb3_distributed_control_generate_messages_nodejs _tb3_distributed_control_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/gdut/24_LC/turtlebot3_distributed_consensus_formation_ws/src/tb3_distributed_control/msg/RobotHistoryData.msg" NAME_WE)
add_dependencies(tb3_distributed_control_generate_messages_nodejs _tb3_distributed_control_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(tb3_distributed_control_gennodejs)
add_dependencies(tb3_distributed_control_gennodejs tb3_distributed_control_generate_messages_nodejs)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS tb3_distributed_control_generate_messages_nodejs)

### Section generating for lang: genpy
### Generating Messages
_generate_msg_py(tb3_distributed_control
  "/home/gdut/24_LC/turtlebot3_distributed_consensus_formation_ws/src/tb3_distributed_control/msg/LeaderHistoryData.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/tb3_distributed_control
)
_generate_msg_py(tb3_distributed_control
  "/home/gdut/24_LC/turtlebot3_distributed_consensus_formation_ws/src/tb3_distributed_control/msg/RobotHistoryData.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/tb3_distributed_control
)

### Generating Services

### Generating Module File
_generate_module_py(tb3_distributed_control
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/tb3_distributed_control
  "${ALL_GEN_OUTPUT_FILES_py}"
)

add_custom_target(tb3_distributed_control_generate_messages_py
  DEPENDS ${ALL_GEN_OUTPUT_FILES_py}
)
add_dependencies(tb3_distributed_control_generate_messages tb3_distributed_control_generate_messages_py)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/gdut/24_LC/turtlebot3_distributed_consensus_formation_ws/src/tb3_distributed_control/msg/LeaderHistoryData.msg" NAME_WE)
add_dependencies(tb3_distributed_control_generate_messages_py _tb3_distributed_control_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/gdut/24_LC/turtlebot3_distributed_consensus_formation_ws/src/tb3_distributed_control/msg/RobotHistoryData.msg" NAME_WE)
add_dependencies(tb3_distributed_control_generate_messages_py _tb3_distributed_control_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(tb3_distributed_control_genpy)
add_dependencies(tb3_distributed_control_genpy tb3_distributed_control_generate_messages_py)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS tb3_distributed_control_generate_messages_py)



if(gencpp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/tb3_distributed_control)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/tb3_distributed_control
    DESTINATION ${gencpp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_cpp)
  add_dependencies(tb3_distributed_control_generate_messages_cpp std_msgs_generate_messages_cpp)
endif()
if(TARGET geometry_msgs_generate_messages_cpp)
  add_dependencies(tb3_distributed_control_generate_messages_cpp geometry_msgs_generate_messages_cpp)
endif()
if(TARGET nav_msgs_generate_messages_cpp)
  add_dependencies(tb3_distributed_control_generate_messages_cpp nav_msgs_generate_messages_cpp)
endif()
if(TARGET sensor_msgs_generate_messages_cpp)
  add_dependencies(tb3_distributed_control_generate_messages_cpp sensor_msgs_generate_messages_cpp)
endif()

if(geneus_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/tb3_distributed_control)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/tb3_distributed_control
    DESTINATION ${geneus_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_eus)
  add_dependencies(tb3_distributed_control_generate_messages_eus std_msgs_generate_messages_eus)
endif()
if(TARGET geometry_msgs_generate_messages_eus)
  add_dependencies(tb3_distributed_control_generate_messages_eus geometry_msgs_generate_messages_eus)
endif()
if(TARGET nav_msgs_generate_messages_eus)
  add_dependencies(tb3_distributed_control_generate_messages_eus nav_msgs_generate_messages_eus)
endif()
if(TARGET sensor_msgs_generate_messages_eus)
  add_dependencies(tb3_distributed_control_generate_messages_eus sensor_msgs_generate_messages_eus)
endif()

if(genlisp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/tb3_distributed_control)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/tb3_distributed_control
    DESTINATION ${genlisp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_lisp)
  add_dependencies(tb3_distributed_control_generate_messages_lisp std_msgs_generate_messages_lisp)
endif()
if(TARGET geometry_msgs_generate_messages_lisp)
  add_dependencies(tb3_distributed_control_generate_messages_lisp geometry_msgs_generate_messages_lisp)
endif()
if(TARGET nav_msgs_generate_messages_lisp)
  add_dependencies(tb3_distributed_control_generate_messages_lisp nav_msgs_generate_messages_lisp)
endif()
if(TARGET sensor_msgs_generate_messages_lisp)
  add_dependencies(tb3_distributed_control_generate_messages_lisp sensor_msgs_generate_messages_lisp)
endif()

if(gennodejs_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/tb3_distributed_control)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/tb3_distributed_control
    DESTINATION ${gennodejs_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_nodejs)
  add_dependencies(tb3_distributed_control_generate_messages_nodejs std_msgs_generate_messages_nodejs)
endif()
if(TARGET geometry_msgs_generate_messages_nodejs)
  add_dependencies(tb3_distributed_control_generate_messages_nodejs geometry_msgs_generate_messages_nodejs)
endif()
if(TARGET nav_msgs_generate_messages_nodejs)
  add_dependencies(tb3_distributed_control_generate_messages_nodejs nav_msgs_generate_messages_nodejs)
endif()
if(TARGET sensor_msgs_generate_messages_nodejs)
  add_dependencies(tb3_distributed_control_generate_messages_nodejs sensor_msgs_generate_messages_nodejs)
endif()

if(genpy_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/tb3_distributed_control)
  install(CODE "execute_process(COMMAND \"/usr/bin/python3\" -m compileall \"${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/tb3_distributed_control\")")
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/tb3_distributed_control
    DESTINATION ${genpy_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_py)
  add_dependencies(tb3_distributed_control_generate_messages_py std_msgs_generate_messages_py)
endif()
if(TARGET geometry_msgs_generate_messages_py)
  add_dependencies(tb3_distributed_control_generate_messages_py geometry_msgs_generate_messages_py)
endif()
if(TARGET nav_msgs_generate_messages_py)
  add_dependencies(tb3_distributed_control_generate_messages_py nav_msgs_generate_messages_py)
endif()
if(TARGET sensor_msgs_generate_messages_py)
  add_dependencies(tb3_distributed_control_generate_messages_py sensor_msgs_generate_messages_py)
endif()

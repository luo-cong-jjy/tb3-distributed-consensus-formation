# Install script for directory: /home/gdut/24_LC/turtlebot3_distributed_consensus_formation_ws/src/tb3_distributed_control

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/gdut/24_LC/turtlebot3_distributed_consensus_formation_ws/install")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/tb3_distributed_control/msg" TYPE FILE FILES
    "/home/gdut/24_LC/turtlebot3_distributed_consensus_formation_ws/src/tb3_distributed_control/msg/LeaderHistoryData.msg"
    "/home/gdut/24_LC/turtlebot3_distributed_consensus_formation_ws/src/tb3_distributed_control/msg/RobotHistoryData.msg"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/tb3_distributed_control/cmake" TYPE FILE FILES "/home/gdut/24_LC/turtlebot3_distributed_consensus_formation_ws/build/tb3_distributed_control/catkin_generated/installspace/tb3_distributed_control-msg-paths.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include" TYPE DIRECTORY FILES "/home/gdut/24_LC/turtlebot3_distributed_consensus_formation_ws/devel/include/tb3_distributed_control")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/roseus/ros" TYPE DIRECTORY FILES "/home/gdut/24_LC/turtlebot3_distributed_consensus_formation_ws/devel/share/roseus/ros/tb3_distributed_control")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/common-lisp/ros" TYPE DIRECTORY FILES "/home/gdut/24_LC/turtlebot3_distributed_consensus_formation_ws/devel/share/common-lisp/ros/tb3_distributed_control")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/gennodejs/ros" TYPE DIRECTORY FILES "/home/gdut/24_LC/turtlebot3_distributed_consensus_formation_ws/devel/share/gennodejs/ros/tb3_distributed_control")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  execute_process(COMMAND "/usr/bin/python3" -m compileall "/home/gdut/24_LC/turtlebot3_distributed_consensus_formation_ws/devel/lib/python3/dist-packages/tb3_distributed_control")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python3/dist-packages" TYPE DIRECTORY FILES "/home/gdut/24_LC/turtlebot3_distributed_consensus_formation_ws/devel/lib/python3/dist-packages/tb3_distributed_control")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/home/gdut/24_LC/turtlebot3_distributed_consensus_formation_ws/build/tb3_distributed_control/catkin_generated/installspace/tb3_distributed_control.pc")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/tb3_distributed_control/cmake" TYPE FILE FILES "/home/gdut/24_LC/turtlebot3_distributed_consensus_formation_ws/build/tb3_distributed_control/catkin_generated/installspace/tb3_distributed_control-msg-extras.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/tb3_distributed_control/cmake" TYPE FILE FILES
    "/home/gdut/24_LC/turtlebot3_distributed_consensus_formation_ws/build/tb3_distributed_control/catkin_generated/installspace/tb3_distributed_controlConfig.cmake"
    "/home/gdut/24_LC/turtlebot3_distributed_consensus_formation_ws/build/tb3_distributed_control/catkin_generated/installspace/tb3_distributed_controlConfig-version.cmake"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/tb3_distributed_control" TYPE FILE FILES "/home/gdut/24_LC/turtlebot3_distributed_consensus_formation_ws/src/tb3_distributed_control/package.xml")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/tb3_distributed_control" TYPE PROGRAM FILES "/home/gdut/24_LC/turtlebot3_distributed_consensus_formation_ws/build/tb3_distributed_control/catkin_generated/installspace/leader_node.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/tb3_distributed_control" TYPE PROGRAM FILES "/home/gdut/24_LC/turtlebot3_distributed_consensus_formation_ws/build/tb3_distributed_control/catkin_generated/installspace/print_notification.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/tb3_distributed_control" TYPE PROGRAM FILES "/home/gdut/24_LC/turtlebot3_distributed_consensus_formation_ws/build/tb3_distributed_control/catkin_generated/installspace/rviz_visualizer.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/tb3_distributed_control" TYPE PROGRAM FILES "/home/gdut/24_LC/turtlebot3_distributed_consensus_formation_ws/build/tb3_distributed_control/catkin_generated/installspace/tb3_controller_node.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/tb3_distributed_control/launch" TYPE DIRECTORY FILES "/home/gdut/24_LC/turtlebot3_distributed_consensus_formation_ws/src/tb3_distributed_control/launch/" FILES_MATCHING REGEX "/[^/]*\\.launch$")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/tb3_distributed_control/rviz" TYPE DIRECTORY FILES "/home/gdut/24_LC/turtlebot3_distributed_consensus_formation_ws/src/tb3_distributed_control/rviz/" FILES_MATCHING REGEX "/[^/]*\\.rviz$")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/tb3_distributed_control/urdf" TYPE DIRECTORY FILES "/home/gdut/24_LC/turtlebot3_distributed_consensus_formation_ws/src/tb3_distributed_control/urdf/" FILES_MATCHING REGEX "/[^/]*\\.xacro$" REGEX "/[^/]*\\.urdf$")
endif()


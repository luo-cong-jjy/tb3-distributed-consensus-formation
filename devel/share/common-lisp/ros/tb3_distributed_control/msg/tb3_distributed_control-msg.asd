
(cl:in-package :asdf)

(defsystem "tb3_distributed_control-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "LeaderHistoryData" :depends-on ("_package_LeaderHistoryData"))
    (:file "_package_LeaderHistoryData" :depends-on ("_package"))
    (:file "RobotHistoryData" :depends-on ("_package_RobotHistoryData"))
    (:file "_package_RobotHistoryData" :depends-on ("_package"))
  ))
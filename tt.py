# 获取机器人状态
suc , result , id = sendCMD(sock , "getRobotState")
if (result == 4):
    # 清除报警
    suc , result , id = sendCMD(sock , "clearAlarm", {"force": 0})
    time.sleep (0.5)
# 获取同步状态
suc , result , id = sendCMD(sock , "getMotorStatus")
if (result == 0):
    # 同步伺服编码器数据
    suc , result , id = sendCMD(sock , "syncMotorStatus")
    time.sleep (0.5)
# 获取机械臂伺服状态
suc , result , id = sendCMD(sock , "getServoStatus")
if (result == 0):
    # 设置机械臂伺服状态ON
    suc , result , id = sendCMD(sock , "set_servo_status", {"status": 1})
    time.sleep (1)
# 获取当前机器人是否处于透传状态
suc , result , id = sendCMD(sock , "get_transparent_transmission_state ")
if (result == 1):
    # 清空透传缓存
    suc , result , id = sendCMD(sock , "tt_clear_servo_joint_buf",{"clear": 0})
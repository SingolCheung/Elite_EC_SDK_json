# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication, QRadioButton, QLabel, QLineEdit, QDialog, QFormLayout, QVBoxLayout
# from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread, pyqtSignal, QDateTime
from PyQt5.QtGui import *
from threading import Thread
import time
from ctypes import *
import ctypes
import socket
import collections
import struct
import math
#python3用pip3 install pywin32
import win32con
from win32process import SuspendThread, ResumeThread
import json
import pygame

####Python端代码#####
class elt_error(Structure):
    _field_ = [
        ('code', c_int),
        ('err_msg', c_char * 256)
    ]

#region 动态链接库Dll的所有函数接口--API
#动态链接库的路径
dllpath = "D:\\Informations\\VScode\\GUI_json\\eltrobot.dll"
#链接动态库
Elite_dll = cdll.LoadLibrary(dllpath)          
#001
#*************************************************************************
#在c/c++中的原函数
# ELT_SDK_PUBLIC(ELT_CTX) elt_create_ctx(const char* addr, int port); 
#原elt_create_ctx有两个输入参数，类型const char* 用c_char_p，int换c_int
Elite_dll.elt_create_ctx.argtypes = (c_char_p,c_int)
#原elt_create_ctx有一个返回参数，类型为c_void_p
Elite_dll.elt_create_ctx.restype = (c_void_p)
robot_IP = bytes("192.168.1.200","ascii")
robot_SDK_port = c_int(8055)
#转换后在Python中的函数
#elt_ctx = Elite_dll.elt_create_ctx(robot_IP, robot_SDK_port)
#--------------------------------------------------------------------------------------------
#*************************************************************************
#在c/c++中的原函数
# ELT_SDK_PUBLIC(int) elt_login(ELT_CTX ctx);
Elite_dll.elt_login.restype = (c_void_p)
#转换后在Python中的函数
#传入参数需要在elt_ctx外加c_void_p()，否则该代码只能在linux下运行；加了才能在window下运行；
# ret = Elite_dll.elt_login(c_void_p(elt_ctx))
#--------------------------------------------------------------------------------------------
#*************************************************************************
#在c/c++中的原函数
# ELT_SDK_PUBLIC(int) elt_logout(ELT_CTX ctx);
Elite_dll.elt_logout.argtypes = [c_void_p]
Elite_dll.elt_logout.restype = c_int
#转换后在Python中的函数
# ret = Elite_dll.elt_logout(c_void_p(elt_ctx))
#--------------------------------------------------------------------------------------------
#*************************************************************************
#在c/c++中的原函数
# ELT_SDK_PUBLIC(int) elt_destroy_ctx(ELT_CTX ctx);
Elite_dll.elt_destroy_ctx.argtypes = [c_void_p]
Elite_dll.elt_destroy_ctx.restype = c_int
#转换后在Python中的函数
# ret = Elite_dll.elt_destroy_ctx(c_void_p(elt_ctx))
#-------------------------------------------------------------------------------------------- 
'''
#009 获取虚拟输出IO状态
*************************************************************************
* 获取虚拟输出IO状态
* @ctx 登陆上下文
* @addr 虚拟IO地址，范围[400~1536]
* @status 存储获取的输出IO状态<EltIOStatus>
* @err 错误信息 * @return 成功或者失败
- 在c/c++中的原函数
int elt_get_virtual_output(ELT_CTX ctx, int addr, int *status, elt_error *err)
'''
Elite_dll.elt_get_virtual_output.argtypes = [c_void_p, c_int, POINTER(c_int), POINTER(elt_error)]
Elite_dll.elt_get_virtual_output.restype = c_int
#Address_M = c_int(528)
#status = c_int(0)
error_message = elt_error()
#转换后在Python中的函数
# ret = Elite_dll.elt_get_virtual_output(c_void_p(elt_ctx), Address_M, byref(status), byref(error_message))
#-------------------------------------------------------------------------------------------- 
'''
*************************************************************************
* 设置虚拟输出IO状态 
* @ctx 登陆上下文 
* @addr 输出IO地址，范围[400~799] 
* @status IO状态<EltIOStatus> 
* @err 错误信息 
* @return 成功或者失败
- 在c/c++中的原函数
int elt_set_virtual_output(ELT_CTX ctx, int addr, int status, elt_error *err);
'''
Elite_dll.elt_set_virtual_output.argtypes = [c_void_p, c_int, c_int, POINTER(elt_error)]
Elite_dll.elt_set_virtual_output.restype = c_int
#Address_M = c_int(528)
#status = c_int(0)
error_message = elt_error()
#转换后在Python中的函数
#ret = Elite_dll.elt_set_virtual_output(c_void_p(elt_ctx), Address_M, status, byref(elt_error))
#-------------------------------------------------------------------------------------------- 
'''
设置为同步状态
*************************************************************************
* 设置为同步状态 
* @param ctx 登陆上下文 
* @param err 错误信息 
* @return 成功或者失败
在c/c++中的原函数
ELT_SDK_PUBLIC(int) elt_sync_on(ELT_CTX ctx, elt_error *err);
'''
Elite_dll.elt_sync_on.argtypes = [c_void_p, POINTER(elt_error)]
Elite_dll.elt_sync_on.restype = c_int
error_message = elt_error()
#转换后在Python中的函数
#ret = Elite_dll.elt_sync_on(c_void_p(elt_ctx), byref(error_message))
#-------------------------------------------------------------------------------------------- 
'''
设置为未同步状态
*************************************************************************
* 设置为未同步状态 
* @param ctx 登陆上下文 
* @param err 错误信息 
* @return 成功或者失败 
在c/c++中的原函数
ELT_SDK_PUBLIC(int) elt_sync_off(ELT_CTX ctx, elt_error * err);
'''
Elite_dll.elt_sync_off.argtypes = [c_void_p, POINTER(elt_error)]
Elite_dll.elt_sync_off.restype = c_int
error_message = elt_error()
#转换后在Python中的函数
#ret = Elite_dll.elt_sync_off(c_void_p(elt_ctx), byref(error_message))
#-------------------------------------------------------------------------------------------- 
'''
清除报警 
*************************************************************************
* 清除报警 
* @ctx 登陆上下文 
* @force 普通清除0,强制清除1 
* @err 错误信息 
* @return 成功或者失败
在c/c++中的原函数 
ELT_SDK_PUBLIC(int) elt_clear_alarm(ELT_CTX ctx, int force, elt_error * err);
'''
Elite_dll.elt_clear_alarm.argtypes = [c_void_p, c_int, POINTER(elt_error)]
Elite_dll.elt_clear_alarm.restype = c_int
force = c_int(0)
#转换后在Python中的函数
# ret = Elite_dll.elt_clear_alarm(c_void_p(elt_ctx),force, byref(error_message))
#-------------------------------------------------------------------------------------------- 
'''
获取机械臂伺服状态
*************************************************************************
获取机械臂伺服状态 
* @ctx 登陆上下文 
* @status 存储获取的机器人状态 ELT_TRUE 启用 ELT_FALSE 未启用 
* @err 错误信息 
* @return 成功或者失败
在c/c++中的原函数 
int elt_get_servo_status(ELT_CTX ctx, int *status, elt_error *err);
'''
Elite_dll.elt_get_servo_status.argtypes = [c_void_p, POINTER(c_long), POINTER(elt_error)]
Elite_dll.elt_get_servo_status.restype = c_int
#在python中原来C的int *status都对应为POINTER(c_long),从这一个API开始，之前的后续再改;
status = c_long(0)
error_message = elt_error()
#转换后在Python中的函数
# ret = Elite_dll.elt_get_servo_status(c_void_p(elt_ctx), byref(status), byref(error_message))
#-------------------------------------------------------------------------------------------- 
'''

*************************************************************************
* 设置伺服使能状态 
* @ctx 登陆上下文 
* @status 1 on 0 off 
* @err 错误信息 
* @return 成功或者失败 
在c/c++中的原函数 
int elt_set_servo_status(ELT_CTX ctx, int status, elt_error *err);
'''
#在python中原来C的int status都对应为c_long,从这一个API开始，之前的后续再改;
Elite_dll.elt_set_servo_status.argtypes = [c_void_p, c_long, POINTER(elt_error)]
Elite_dll.elt_set_servo_status.restype = c_int
v_status = 0
#转换后在Python中的函数
# ret = Elite_dll.elt_set_servo_status(c_void_p(elt_ctx), status, byref(error_message))
#--------------------------------------------------------------------------------------------
'''
*************************************************************************
* 获取机器人状态 
* @ctx 登陆上下文 
* @state 存储获取的机器人状态 <EltRobotState> 
* @err 错误信息 
* @return 成功或者失败
#在c/c++中的原函数
# ELT_SDK_PUBLIC(int) elt_get_robot_state(ELT_CTX ctx, int *state, elt_error *err);
'''
Elite_dll.elt_get_robot_state.argtypes = [c_void_p, POINTER(c_int), POINTER(elt_error)]
Elite_dll.elt_get_robot_state.restype = c_int
state = c_int(0)
error_message = elt_error()
#转换后在Python中的函数
# ret = Elite_dll.elt_get_robot_state(c_void_p(elt_ctx), byref(state), byref(error_message))
#--------------------------------------------------------------------------------------------

'''
设置伺服使能状态 
*************************************************************************
* 设置伺服使能状态 
* @ctx 登陆上下文 
* @status 1 on 0 off 
* @err 错误信息 
* @return 成功或者失败 
在c/c++中的原函数 
int elt_set_servo_status(ELT_CTX ctx, int status, elt_error *err);
'''
#在python中原来C的int status都对应为c_long,从这一个API开始，之前的后续再改;
Elite_dll.elt_set_servo_status.argtypes = [c_void_p, c_long, POINTER(elt_error)]
Elite_dll.elt_set_servo_status.restype = c_int
v_status = 0
#转换后在Python中的函数
# ret = Elite_dll.elt_set_servo_status(c_void_p(elt_ctx), status, byref(error_message))
#--------------------------------------------------------------------------------------------
'''
机器人自动运行
*************************************************************************
* 机器人自动运行 
* @ctx 登陆上下文 
* @err 错误信息 
* @return 成功或者失败 
在c/c++中的原函数 
int elt_run(ELT_CTX ctx, elt_error *err);
'''
Elite_dll.elt_run.argtypes = [c_void_p, POINTER(elt_error)]
Elite_dll.elt_run.restype = c_int
#转换后在Python中的函数
# ret = Elite_dll.elt_run(c_void_p(elt_ctx), byref(error_message))
#--------------------------------------------------------------------------------------------
'''
停止机器人运行 
*************************************************************************
* 停止机器人运行 
* @ctx 登陆上下文 
* @err 错误信息 
* @return 成功或者失败
在c/c++中的原函数 
int elt_stop(ELT_CTX ctx, elt_error *err);
'''
Elite_dll.elt_stop.argtypes = [c_void_p, POINTER(elt_error)]
Elite_dll.elt_stop.restype = c_int
#转换后在Python中的函数
# ret = Elite_dll.elt_stop(c_void_p(elt_ctx), byref(error_message))
#--------------------------------------------------------------------------------------------
'''
*************************************************************************
* 机器人暂停 
* @ctx 登陆上下文 
* @err 错误信息 
* @return 成功或者失败
在c/c++中的原函数 
int elt_pause(ELT_CTX ctx, elt_error *err);
'''
Elite_dll.elt_pause.argtypes = [c_void_p, POINTER(elt_error)]
Elite_dll.elt_pause.restype = c_int
#转换后在Python中的函数
# ret = Elite_dll.elt_pause(c_void_p(elt_ctx), byref(error_message))
#--------------------------------------------------------------------------------------------

'''
*************************************************************************
在c/c++中的原函数 
ret = elt_jog(ELT_CTX ctx, int index, elt_error *err);
'''
Elite_dll.elt_jog.argtypes = [c_void_p, c_long, POINTER(elt_error)]
Elite_dll.elt_jog.restype = c_int
index = c_long(0)
#转换后在Python中的函数
# ret = Elite_dll.elt_jog(c_void_p(elt_ctx), index, byref(error_message))
#--------------------------------------------------------------------------------------------
'''
*************************************************************************
* 清除路点信息 
* @ctx 登陆上下文 
* @err 错误信息 
* @return 成功或者失败
在c/c++中的原函数
ret = elt_clear_waypoint(ELT_CTX ctx, elt_error *err);
'''
Elite_dll.elt_clear_waypoint.argtypes = [c_void_p, POINTER(elt_error)]
Elite_dll.elt_clear_waypoint.restype = c_int
#转换后在Python中的函数
# ret = Elite_dll.elt_clear_waypoint(c_void_p(elt_ctx), byref(error_message))
#--------------------------------------------------------------------------------------------

'''
*************************************************************************
* 设置路点运动时最大关节速度 
* @ctx 登陆上下文 
* @speed 关节速度，范围:[1~100], 单位：百分比 
* @err 错误信息 
* @return 成功或者失败
在c/c++中的原函数
ret = elt_set_waypoint_max_joint_speed(ELT_CTX ctx, double speed, elt_error *err);
'''
Elite_dll.elt_set_waypoint_max_joint_speed.argtypes = [c_void_p, c_double, POINTER(elt_error)]
Elite_dll.elt_set_waypoint_max_joint_speed.restype = c_int
# speed = c_double(50)
error_message = elt_error()
#转换后在Python中的函数
# ret = Elite_dll.elt_set_waypoint_max_joint_speed(c_void_p(elt_ctx), speed, byref(error_message))
#--------------------------------------------------------------------------------------------
'''
*************************************************************************
* 添加路点信息 
* @ctx 登陆上下文 
* @waypoint_array 目标位置（关节角） 
* @err 错误信息 
* @return 成功或者失败
在c/c++中的原函数
ret = elt_add_waypoint(ELT_CTX ctx, elt_robot_pos waypoint_array, elt_error *err);
'''
Elite_dll.elt_add_waypoint.argtypes = [c_void_p, POINTER(c_double), POINTER(elt_error)]
Elite_dll.elt_add_waypoint.restype = c_int
waypoint_array = (c_double*8)()
error_message = elt_error()
#转换后在Python中的函数
# ret = Elite_dll.elt_add_waypoint(c_void_p(elt_ctx), waypoint_array, byref(error_message))
#--------------------------------------------------------------------------------------------
'''
*************************************************************************
* 轨迹运动 
* @ctx 登陆上下文 
* @move_type 运动类型,<EltMoveType> 
* @pl 平滑度等级，范围[0~7] 
* @return 成功或者失败
机器人运动类型 enumEltMoveType { 
    TRACK_MOVE_JOINT=0, 
    TRACK_MOVE_LINE=1, 
    TRACK_MOVE_ROTATE=2, 
    TRACK_MOVE_CIRCLE=3, };
在c/c++中的原函数
ret = elt_track_move(ELT_CTX ctx, int move_type, int pl, elt_error *err);
'''
Elite_dll.elt_track_move.argtypes = [c_void_p, c_long, c_long, POINTER(elt_error)]
Elite_dll.elt_track_move.restype = c_int
move_type = c_long(0)
pl = c_long(0)
error_message = elt_error()
#转换后在Python中的函数
# ret = Elite_dll.elt_track_move(c_void_p(elt_ctx), move_type, pl, byref(error_message))
#--------------------------------------------------------------------------------------------
'''
*************************************************************************
* 设置输出IO状态 
* @ctx 登陆上下文 
* @addr 输入IO地址，范围[0~127] 
* @status IO状态<EltIOStatus> 
* @err 错误信息 
* @return 成功或者失败
在c/c++中的原函数
int elt_set_output(ELT_CTX ctx, int addr, int status, elt_error *err)
'''
Elite_dll.elt_set_output.argtypes = [c_void_p, c_int, c_int, POINTER(elt_error)]
Elite_dll.elt_set_output.restype = c_int
#Y002 = c_int(2)
#value_Y002 = c_int(1)
#转换后在Python中的函数
#ret = Elite_dll.elt_set_output(c_void_p(elt_ctx), Y002, value_Y002, byref(elt_error))
#--------------------------------------------------------------------------------------------
'''
*************************************************************************
* 获取输入IO状态 
* @ctx 登陆上下文 
* @addr 输入IO地址，范围[0~127] 
* @status 存储获取的输入IO状态<EltIOStatus> 
* @err 错误信息 
* @return 成功或者失败
在c/c++中的原函数
int elt_get_output(ELT_CTX ctx, int addr, int *status, elt_error *err);
'''
Elite_dll.elt_get_output.argtypes = [c_void_p, c_int, POINTER(c_int), POINTER(elt_error)]
Elite_dll.elt_get_output.restype = c_int
#Y002 = c_int(2)
#value_Y002 = c_int(0)
#转换后在Python中的函数
#ret = Elite_dll.elt_get_output(c_void_p(elt_ctx), Y002, byref(value_Y002), byref(elt_error))
#--------------------------------------------------------------------------------------------

'''
*************************************************************************
'''
#--------------------------------------------------------------------------------------------
#endregion

#线程--读取系统当前的时间
class GetTimeThread(QThread):
    latest_time = pyqtSignal(str)
    def run(self):
        while True:
            datatime = QDateTime.currentDateTime()
            format_time = datatime.toString("yyyy-MM-dd HH:mm:ss:zzz ddd")
            #self.latest_time.emit(str(format_data))
            self.latest_time.emit(format_time)
            time.sleep(0.001)

#region 线程--8056读取机器人的状态
class GetDataThread(QThread):
    #使用8056，打开远程，不能再打开Modbus
    latest_posj1 = pyqtSignal(str)
    latest_posj2 = pyqtSignal(str)
    latest_posj3 = pyqtSignal(str)
    latest_posj4 = pyqtSignal(str)
    latest_posj5 = pyqtSignal(str)
    latest_posj6 = pyqtSignal(str)

    latest_posex = pyqtSignal(str)
    latest_posey = pyqtSignal(str)
    latest_posez = pyqtSignal(str)
    latest_poserx = pyqtSignal(str)
    latest_posery = pyqtSignal(str)
    latest_poserz = pyqtSignal(str)

    latest_robotstate = pyqtSignal(str)
    latest_mode = pyqtSignal(str)
    latest_synchronize = pyqtSignal(str)
    latest_brake = pyqtSignal(str)
    #以下暂无
    #latest_coordinate = pyqtSignal(str)
    #latest_toolnum = pyqtSignal(str)
    #latest_usernum = pyqtSignal(str)
    
    # startParm = startParm
    def __init__(self, startParm):
        super().__init__()
        self.startParm = startParm

    def run(self):
        # @UndefinedVariable
        self.handle = ctypes.windll.kernel32.OpenThread(win32con.PROCESS_ALL_ACCESS, False, int(QThread.currentThreadId()))
        '''
        global flag
        while flag:
            print('------------------------------')
            print("flag=",flag)
            time.sleep(2)
        '''

        HOST = "192.168.1.200"
        PORT = 8056
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST,PORT))
        index = 0
        index1 = 0
        lost = 0
        while True:
            #print("value_8056=",value_8056,"\n")
            dic = collections.OrderedDict()
            dic['MessageSize'] = 'I'
            dic['TimeStamp'] = 'Q'
            dic['autorun_cycleMode'] = 'B'
            dic['machinePos01'] = 'd'
            dic['machinePos02'] = 'd'
            dic['machinePos03'] = 'd'
            dic['machinePos04'] = 'd'
            dic['machinePos05'] = 'd'
            dic['machinePos06'] = 'd'
            dic['machinePos07'] = 'd'
            dic['machinePos08'] = 'd'
            dic['machinePose01'] = 'd'
            dic['machinePose02'] = 'd'
            dic['machinePose03'] = 'd'
            dic['machinePose04'] = 'd'
            dic['machinePose05'] = 'd'
            dic['machinePose06'] = 'd'
            dic['machineUserPose01'] = 'd'
            dic['machineUserPose02'] = 'd'
            dic['machineUserPose03'] = 'd'
            dic['machineUserPose04'] = 'd'
            dic['machineUserPose05'] = 'd'
            dic['machineUserPose06'] = 'd'
            dic['torque01'] = 'd'
            dic['torque02'] = 'd'
            dic['torque03'] = 'd'
            dic['torque04'] = 'd'
            dic['torque05'] = 'd'
            dic['torque06'] = 'd'
            dic['torque07'] = 'd'
            dic['torque08'] = 'd'
            dic['robotState'] = 'i'
            dic['servoReady'] = 'i'
            dic['can_motor_run'] = 'i'
            dic['motor_speed01'] = 'i'
            dic['motor_speed02'] = 'i'
            dic['motor_speed03'] = 'i'
            dic['motor_speed04'] = 'i'
            dic['motor_speed05'] = 'i'
            dic['motor_speed06'] = 'i'
            dic['motor_speed07'] = 'i'
            dic['motor_speed08'] = 'i'
            dic['robotMode'] = 'i'
            dic['analog_ioinput_time01'] = 'd'
            dic['analog_ioinput_time02'] = 'd'
            dic['analog_ioinput_time03'] = 'd'
            dic['analog_ioOutput01'] = 'd'
            dic['analog_ioOutput02'] = 'd'
            dic['analog_ioOutput03'] = 'd'
            dic['analog_ioOutput04'] = 'd'
            dic['analog_ioOutput05'] = 'd'
            dic['digital_ioinput_time'] = 'Q'
            dic['digital_ioOutput'] = 'Q'
            #接受套接字的数据。数据以字符串形式返回，bufsize指定最多可以接收的数量。flag提供有关消息的其他信息，通常可以忽略。
            data = s.recv(10240)
            # data[0]~data[364]
            if len(data) != 365:
                lost += 1
                index1 += 1
                #print(str(lost))
                continue
            #print("index =",index)
            names=[]
            ii=range(len(dic))
            for key,i in zip(dic,ii):
                fmtsize = struct.calcsize(dic[key])
                data1, data = data[0:fmtsize], data[fmtsize:]
                fmt="!" + dic[key]
                names.append(struct.unpack(fmt,data1))
                dic[key] = dic[key], struct.unpack(fmt, data1)
                #print(dic[key])
            output = ""
            for key in dic.keys():
                # 以下output就是一串分行的字符串
                output += str(key) + ":" + str(dic[key][1][0]) + ";\n"
                if key == "machinePos01":
                    self.latest_posj1.emit(str(round(dic[key][1][0],3)))
                    #print("key_value=",str(round(dic[key][1][0],3)))
                    #print("key_value=",dic[key][1][0])
                if key == "machinePos02":
                    self.latest_posj2.emit(str(round(dic[key][1][0],3)))
                if key == "machinePos03":
                    self.latest_posj3.emit(str(round(dic[key][1][0],3)))
                if key == "machinePos04":
                    self.latest_posj4.emit(str(round(dic[key][1][0],3)))
                if key == "machinePos05":
                    self.latest_posj5.emit(str(round(dic[key][1][0],3)))
                if key == "machinePos06":
                    self.latest_posj6.emit(str(round(dic[key][1][0],3)))
                
                if key == "machinePose01":
                    self.latest_posex.emit(str(round(dic[key][1][0],3)))
                if key == "machinePose02":
                    self.latest_posey.emit(str(round(dic[key][1][0],3)))
                if key == "machinePose03":
                    self.latest_posez.emit(str(round(dic[key][1][0],3)))
                if key == "machinePose04":
                    self.latest_poserx.emit(str(round(dic[key][1][0],3)))
                if key == "machinePose05":
                    self.latest_posery.emit(str(round(dic[key][1][0],3)))
                if key == "machinePose06":
                    self.latest_poserz.emit(str(round(dic[key][1][0],3)))

                if key == "robotState":
                    self.latest_robotstate.emit(str(round(dic[key][1][0],3)))
                if key == "robotMode":
                    self.latest_mode.emit(str(round(dic[key][1][0],3)))
                if key == "can_motor_run":
                    self.latest_synchronize.emit(str(round(dic[key][1][0],3)))
                if key == "servoReady":
                    self.latest_brake.emit(str(round(dic[key][1][0],3)))
            # 在output的前面增加"lost : " + str(lost) + " index : " + str(index) + ";"
            #output = "lost : " + str(lost) + " index : " + str(index) + ";" + output + "\n"
            # 更改为如下,把 ";"更改为"\n" ，让"lost : " + str(lost) + " index : " + str(index)单独在一行里显示
            # output = "lost : " + str(lost) + " index : " + str(index) + "\n" + output + "\n"
            if index % 10 == 0:
                # 打印时间戳
                timestamp01_value = dic['TimeStamp'][1][0] // 1000
                timeValue = time.gmtime(int(timestamp01_value))
                #print (time.strftime("%Y-%m-%d %H:%M:%S", timeValue))
                # 打印所有信息
                #print (output[0]+output[1]+output[2]+output[3]+output[4]+output[5]+output[6])
                lost_index = "lost : " + str(lost) + " index : " + str(index)
                #print(lost_index)
                #print(output)
            index = index +1
            output = ""
            dic = {}
            data = ""
            time.sleep(0.01)
        s.close()
#endregion

class GetJoystickDataThread(QThread):
    joystick_status = pyqtSignal(str)
    btn_l2 = pyqtSignal(str)
    btn_l1 = pyqtSignal(str)
    btn_left_up = pyqtSignal(str)
    btn_left_left = pyqtSignal(str)
    btn_left_right = pyqtSignal(str)
    btn_left_down = pyqtSignal(str)
    btn_r2 = pyqtSignal(str)
    btn_r1 = pyqtSignal(str)
    btn_right_up = pyqtSignal(str)
    btn_right_left = pyqtSignal(str)
    btn_right_right = pyqtSignal(str)
    btn_right_down = pyqtSignal(str)
    btn_leftstick_updown = pyqtSignal(str)
    btn_leftstick_leftright = pyqtSignal(str)
    btn_rightstick_updown = pyqtSignal(str)
    btn_rightstick_leftright = pyqtSignal(str)
    def run(self):
        pygame.init()
        done = False
        clock = pygame.time.Clock()
        pygame.joystick.init()
        while done==False:
            # EVENT PROCESSING STEP
            for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    done=True # Flag that we are done so we exit this loop
                '''
                # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
                if event.type == pygame.JOYAXISMOTION:
                    print("Joystick JOYAXISMOTION")
                if event.type == pygame.JOYBALLMOTION:
                    print("Joystick JOYBALLMOTION")    
                if event.type == pygame.JOYBUTTONDOWN:
                    print("Joystick button pressed.")
                if event.type == pygame.JOYBUTTONUP:
                    print("Joystick button released.")
                if event.type == pygame.JOYHATMOTION:
                    print("Joystick JOYHATMOTION.")
                '''

            # Get count of joysticks
            joystick_count = pygame.joystick.get_count()
            #self.joystick_num.emit(str(joystick_count))
            #print("Number of joysticks: {}".format(joystick_count))

            # For each joystick:
            for i in range(joystick_count):
                if i == 1:
                    joystick = pygame.joystick.Joystick(i)
                    #self.joystick_current_num.emit(str(joystick))
                    #print("Joystick={}".format(i))
                    joystick.init()
                    
                    # Get the name from the OS for the controller/joystick
                    name = joystick.get_name()
                    self.joystick_status.emit("Total=" + str(joystick_count) + ";" + "Current Joystick=" + str(i) + ";" + "Name=" + str(name))
                    #print("Joystick name: {}".format(name))

                    # Usually axis run in pairs, up/down for one, and left/right for
                    # the other.
                    axes = joystick.get_numaxes()
                    #print("Number of axes: {}".format(axes))
                    '''
                    for i in range( axes ):
                        axis = joystick.get_axis( i )
                        #print("Axis {} value: {:>6.3f}".format(i, axis))
                    '''
                    self.btn_leftstick_leftright.emit(str(round(joystick.get_axis(0),3)))
                    self.btn_leftstick_updown.emit(str(round(joystick.get_axis(1),3)))
                    self.btn_rightstick_updown.emit(str(round(joystick.get_axis(2),3)))
                    self.btn_rightstick_leftright.emit(str(round(joystick.get_axis(3),3)))

                    buttons = joystick.get_numbuttons()
                    #print("Number of buttons: {}".format(buttons))
                    '''
                    for i in range( buttons ):
                        button = joystick.get_button( i )
                    #print("Button {:>2} value: {}".format(i,button))
                    '''
                    self.btn_right_up.emit(str(joystick.get_button(0)))
                    self.btn_right_right.emit(str(joystick.get_button(1)))
                    self.btn_right_down.emit(str(joystick.get_button(2)))
                    self.btn_right_left.emit(str(joystick.get_button(3)))
                    self.btn_l2.emit(str(joystick.get_button(4)))
                    self.btn_r2.emit(str(joystick.get_button(5)))
                    self.btn_l1.emit(str(joystick.get_button(6)))
                    self.btn_r1.emit(str(joystick.get_button(7)))

                    # Hat switch. All or nothing for direction, not like joysticks.
                    # Value comes back in an array.
                    #hats = joystick.get_numhats()
                    #print("Number of hats: {}".format(hats))
                    '''
                    for i in range( hats ):
                        hat = joystick.get_hat(i)
                    #print("Hat {} value: {}".format(i, str(hat)))
                    '''
                    str_hat = str(joystick.get_hat(0))
                    if str_hat == "(0, 0)":
                        '''
                        self.btn_left_up.emit(str(joystick.get_hat(0)))
                        self.btn_left_left.emit(str(joystick.get_hat(0)))
                        self.btn_left_right.emit(str(joystick.get_hat(0)))
                        self.btn_left_down.emit(str(joystick.get_hat(0)))
                        '''
                        self.btn_left_up.emit(str(0))
                        self.btn_left_left.emit(str(0))
                        self.btn_left_right.emit(str(0))
                        self.btn_left_down.emit(str(0))
                    if str_hat == "(0, 1)":
                        self.btn_left_up.emit(str(1))
                    if str_hat == "(-1, 0)":
                        self.btn_left_left.emit(str(1))
                    if str_hat == "(1, 0)":
                        self.btn_left_right.emit(str(1))
                    if str_hat == "(0, -1)":
                        self.btn_left_down.emit(str(1))

            # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

            # Go ahead and update the screen with what we've drawn.
            #pygame.display.flip()

            # Limit to 20 frames per second
            clock.tick(20)

        # Close the window and quit.
        # If you forget this line, the program will 'hang'
        # on exit if running from IDLE.
        pygame.quit()

class EliteUISDK(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "SDK&json control UI"
        self.left = 1150
        self.top = 50
        self.width = 750
        self.height = 950
        self.input_time = QLineEdit(self)
        self.input_time.setGeometry(350,915,250,30)
        # self.elt_ctx_self = c_void_p()
        # 可以使用self.elt_ctx_self = -1 在json调用joystick;但是已经使用self.SDK_on这个变量，这个在elt_login更改
        self.elt_ctx_self = -1
        self.ret_login = 0
        self.button_on = 0
        self.SDK_on = 0
        # 在json的按钮CreateSocket里更改数值self.SDK_json_on == 1
        # 在json的按钮CloseSocket里更改数值self.SDK_json_on = 0；此处不行，因透传运行中，已经在死循环中。可使用PS2某个未使用按钮
        # 在摇杆的按钮BtnRightLeft，按下按钮为1是时，self.SDK_json_on = 0
        self.SDK_json_on = -1
        self.json_ps2_button_on = -1
        self.json_TT_pose = [0, 0, 0, 0, 0, 0]
        self.json_TT_pos = [0, 0, 0, 0, 0, 0, 0 , 0]
        self.json_btn_l2_value = 0
        self.json_btn_l1_value = 0
        self.json_btn_left_up_value = 0
        self.json_btn_left_left_value = 0
        self.json_btn_left_right_value = 0
        self.json_btn_left_down_value = 0
        self.json_btn_r2_value = 0
        self.json_btn_r1_value = 0
        self.json_btn_right_up_value = 0
        self.json_btn_right_left_value = 0
        self.json_btn_right_right_value = 0
        self.json_btn_right_down_value = 0
        self.json_btn_leftstick_updown_value = 0
        self.json_btn_leftstick_leftright_value = 0
        self.json_btn_rightstick_updown_value = 0
        #self.input_time.resize(100,800)
        #self.value_8056 = 0
        # self.ex = Constant(self)
        self.startParm = "cmd8056"
        #self.constant = Constant(self)
        #region GetDataThread实例化的getdata线程读取的数据输入到EliteUISDK页面所在的位置
        self.latest_posj1 = QLineEdit(self)
        self.latest_posj1.setGeometry(190,250,90,30)
        self.latest_posj2 = QLineEdit(self)
        self.latest_posj2.setGeometry(190,300,90,30)
        self.latest_posj3 = QLineEdit(self)
        self.latest_posj3.setGeometry(190,350,90,30)
        self.latest_posj4 = QLineEdit(self)
        self.latest_posj4.setGeometry(190,400,90,30)
        self.latest_posj5 = QLineEdit(self)
        self.latest_posj5.setGeometry(190,450,90,30)
        self.latest_posj6 = QLineEdit(self)
        self.latest_posj6.setGeometry(190,500,90,30)

        self.latest_posex = QLineEdit(self)
        self.latest_posex.setGeometry(430,250,90,30)
        self.latest_posey = QLineEdit(self)
        self.latest_posey.setGeometry(430,300,90,30)
        self.latest_posez = QLineEdit(self)
        self.latest_posez.setGeometry(430,350,90,30)
        self.latest_poserx = QLineEdit(self)
        self.latest_poserx.setGeometry(430,400,90,30)
        self.latest_posery = QLineEdit(self)
        self.latest_posery.setGeometry(430,450,90,30)
        self.latest_poserz = QLineEdit(self)
        self.latest_poserz.setGeometry(430,500,90,30)

        self.latest_robotstate = QLineEdit(self)
        self.latest_robotstate.setGeometry(220,0,100,30)
        self.latest_mode = QLineEdit(self)
        self.latest_mode.setGeometry(220,50,100,30)
        self.latest_synchronize = QLineEdit(self)
        self.latest_synchronize.setGeometry(220,100,100,30)
        self.latest_brake = QLineEdit(self)
        self.latest_brake.setGeometry(220,150,100,30)
        #endregion

        #region Joystick——PS2各按钮状态显示框
        self.joystick_status = QLineEdit(self)
        self.joystick_status.setGeometry(130,550,400,30)
        self.btn_l2 = QLineEdit(self)
        self.btn_l2.setGeometry(130,590,40,30)
        self.btn_l1 = QLineEdit(self)
        self.btn_l1.setGeometry(130,630,40,30)
        self.btn_left_up = QLineEdit(self)
        self.btn_left_up.setGeometry(160,670,40,30)
        self.btn_left_left = QLineEdit(self)
        self.btn_left_left.setGeometry(130,710,40,30)
        self.btn_left_right = QLineEdit(self)
        self.btn_left_right.setGeometry(190,710,40,30)
        self.btn_left_down = QLineEdit(self)
        self.btn_left_down.setGeometry(160,750,40,30)
        self.btn_r2 = QLineEdit(self)
        self.btn_r2.setGeometry(340,590,40,30)
        self.btn_r1 = QLineEdit(self)
        self.btn_r1.setGeometry(340,630,40,30)
        self.btn_right_up = QLineEdit(self)
        self.btn_right_up.setGeometry(320,670,40,30)
        self.btn_right_left = QLineEdit(self)
        self.btn_right_left.setGeometry(280,710,40,30)
        self.btn_right_right = QLineEdit(self)
        self.btn_right_right.setGeometry(340,710,40,30)
        self.btn_right_down = QLineEdit(self)
        self.btn_right_down.setGeometry(320,750,40,30)
        self.btn_leftstick_updown = QLineEdit(self)
        self.btn_leftstick_updown.setGeometry(130,790,50,30)
        self.btn_leftstick_leftright = QLineEdit(self)
        self.btn_leftstick_leftright.setGeometry(190,790,50,30)
        self.btn_rightstick_updown = QLineEdit(self)
        self.btn_rightstick_updown.setGeometry(280,790,50,30)
        self.btn_rightstick_leftright = QLineEdit(self)
        self.btn_rightstick_leftright.setGeometry(340,790,50,30)
        #endregion
        
        #region SDK_c++和c输入框,如Var_M_num,Output_Y的地址输入框,直接输入数值，如让Y003输出，直接输入3；
        self.Var_M_num = QLineEdit(self)
        self.Var_M_num.setGeometry(80,650,30,30)
        self.Output_Y = QLineEdit(self)
        self.Output_Y.setGeometry(80,800,30,30)
        #endregion
        #region SDK_json输入框
        # 输入示例
        self.json_address_M = QLineEdit(self)
        self.json_address_M.setGeometry(700,350,40,30)
        self.json_address_Y = QLineEdit(self)
        self.json_address_Y.setGeometry(700,400,40,30)
        #endregion
        self.UI()

    #region SDK 部分按钮clicked或pressed触发的API，该部分使用的是需要传入button.text参数；部分按钮在def UI(self)里，该部分不需要传入参数，直接使用sender()。待后续进一步了解在统一整理在一起
    def btnstate(self,btn): 
        if btn.text()=="TEACH":
            if btn.isChecked() == True:
                print( btn.text() + " is selected")
            else:
                print( btn.text() + " is deselected")
        if btn.text()=="PLAY":
            if btn.isChecked()== True :
                print( btn.text() + " is selected")
            else:
                print( btn.text() + " is deselected")
        if btn.text()=="REMOTE":
            if btn.isChecked()== True :
                print( btn.text() + " is selected")
            else:
                print( btn.text() + " is deselected")
        #region 单关节运动
        if btn.text()=="J1-":
            index = c_long(0)
            index.value = 0
            ret = Elite_dll.elt_jog(c_void_p(self.elt_ctx_self), index, byref(error_message))
        if btn.text()=="J1+":
            index = c_long(0)
            index.value = 1
            ret = Elite_dll.elt_jog(c_void_p(self.elt_ctx_self), index, byref(error_message))
        if btn.text()=="J2-":
            index = c_long(0)
            index.value = 2
            ret = Elite_dll.elt_jog(c_void_p(self.elt_ctx_self), index, byref(error_message))
        if btn.text()=="J2+":
            index = c_long(0)
            index.value = 3
            ret = Elite_dll.elt_jog(c_void_p(self.elt_ctx_self), index, byref(error_message))
        if btn.text()=="J3-":
            index = c_long(0)
            index.value = 4
            ret = Elite_dll.elt_jog(c_void_p(self.elt_ctx_self), index, byref(error_message))
        if btn.text()=="J3+":
            index = c_long(0)
            index.value = 5
            ret = Elite_dll.elt_jog(c_void_p(self.elt_ctx_self), index, byref(error_message))
        if btn.text()=="J4-":
            index = c_long(0)
            index.value = 6
            ret = Elite_dll.elt_jog(c_void_p(self.elt_ctx_self), index, byref(error_message))
        if btn.text()=="J4+":
            index = c_long(0)
            index.value = 7
            ret = Elite_dll.elt_jog(c_void_p(self.elt_ctx_self), index, byref(error_message))
        if btn.text()=="J5-":
            index = c_long(0)
            index.value = 8
            ret = Elite_dll.elt_jog(c_void_p(self.elt_ctx_self), index, byref(error_message))
        if btn.text()=="J5+":
            index = c_long(0)
            index.value = 9
            ret = Elite_dll.elt_jog(c_void_p(self.elt_ctx_self), index, byref(error_message))
        if btn.text()=="J6-":
            index = c_long(0)
            index.value = 10
            ret = Elite_dll.elt_jog(c_void_p(self.elt_ctx_self), index, byref(error_message))
        if btn.text()=="J6+":
            index = c_long(0)
            index.value = 11
            ret = Elite_dll.elt_jog(c_void_p(self.elt_ctx_self), index, byref(error_message))

        #endregion
        #region X Y Z Ry Rx Rz 运动
        if btn.text()=="X-":
            index = c_long(0)
            index.value = 0
            ret = Elite_dll.elt_jog(c_void_p(self.elt_ctx_self), index, byref(error_message))
        if btn.text()=="X+":
            index = c_long(0)
            index.value = 1
            ret = Elite_dll.elt_jog(c_void_p(self.elt_ctx_self), index, byref(error_message))
        if btn.text()=="Y-":
            index = c_long(0)
            index.value = 2
            ret = Elite_dll.elt_jog(c_void_p(self.elt_ctx_self), index, byref(error_message))
        if btn.text()=="Y+":
            index = c_long(0)
            index.value = 3
            ret = Elite_dll.elt_jog(c_void_p(self.elt_ctx_self), index, byref(error_message))
        if btn.text()=="Z-":
            index = c_long(0)
            index.value = 4
            ret = Elite_dll.elt_jog(c_void_p(self.elt_ctx_self), index, byref(error_message))
        if btn.text()=="Z+":
            index = c_long(0)
            index.value = 5
            ret = Elite_dll.elt_jog(c_void_p(self.elt_ctx_self), index, byref(error_message))
        if btn.text()=="Rx-":
            index = c_long(0)
            index.value = 6
            ret = Elite_dll.elt_jog(c_void_p(self.elt_ctx_self), index, byref(error_message))
        if btn.text()=="Rx+":
            index = c_long(0)
            index.value = 7
            ret = Elite_dll.elt_jog(c_void_p(self.elt_ctx_self), index, byref(error_message))
        if btn.text()=="Ry-":
            index = c_long(0)
            index.value = 8
            ret = Elite_dll.elt_jog(c_void_p(self.elt_ctx_self), index, byref(error_message))
        if btn.text()=="Ry+":
            index = c_long(0)
            index.value = 9
            ret = Elite_dll.elt_jog(c_void_p(self.elt_ctx_self), index, byref(error_message))
        if btn.text()=="Rz-":
            index = c_long(0)
            index.value = 10
            ret = Elite_dll.elt_jog(c_void_p(self.elt_ctx_self), index, byref(error_message))
        if btn.text()=="Rz+":
            index = c_long(0)
            index.value = 11
            ret = Elite_dll.elt_jog(c_void_p(self.elt_ctx_self), index, byref(error_message))
        #endregion
    #endregion

    #region json协议 未使用以下这种方式 发送methon(接口方法)的函数，调用时需要传入参数 
    def josnSendMethod(self,sock,method,params=None,id=1):
        if(not params):
             params=[]
        else:
            params=json.dumps(params)
        sendStr="{{\"method\":\"{0}\",\"params\":{1},\"jsonrpc\":\"2.0\",\"id\":{2}}}".format(method,params,id)+"\n"
        try:
            #print(sendStr)
            sock.sendall(bytes(sendStr,"utf-8"))
            ret=sock.recv(1024)
            jdata=json.loads(str(ret,"utf-8"))
            if("result" in jdata.keys()):
                return (True,json.loads(jdata["result"]),jdata["id"])
            elif("error" in jdata.keys()):
                return (False,json.loads(jdata["error"]),jdata["id"])
            else:
                return (False,None,None)
        except Exception as e:
            return (False,None,None)
    #endregion

    def UI(self): 
        self.getdata1 = GetTimeThread()
        self.getdata1.latest_time.connect(self.timeDisplay)
        # 创建线程后立刻启动线程，不需要启动信号
        self.getdata1.start()
        
        self.getjoystickdata = GetJoystickDataThread()
        self.getjoystickdata.joystick_status.connect(self.JoystickName)
        #regioin SDK_c++和C动态链接库或静态链接库下connect相应按钮的方法(函数)
        self.getjoystickdata.btn_l2.connect(self.BtnL2)
        self.getjoystickdata.btn_l1.connect(self.BtnL1)
        self.getjoystickdata.btn_left_up.connect(self.BtnLeftUp)
        self.getjoystickdata.btn_left_left.connect(self.BtnLeftLeft)
        self.getjoystickdata.btn_left_right.connect(self.BtnLeftRight)
        self.getjoystickdata.btn_left_down.connect(self.BtnLeftDown)
        self.getjoystickdata.btn_r2.connect(self.BtnR2)
        self.getjoystickdata.btn_r1.connect(self.BtnR1)
        self.getjoystickdata.btn_right_up.connect(self.BtnRightUp)
        self.getjoystickdata.btn_right_left.connect(self.BtnRightLeft)
        self.getjoystickdata.btn_right_right.connect(self.BtnRightRight)
        self.getjoystickdata.btn_right_down.connect(self.BtnRightDown)
        self.getjoystickdata.btn_leftstick_updown.connect(self.BtnLeftstickUpDown)
        self.getjoystickdata.btn_leftstick_leftright.connect(self.BtnLeftstickLeftRight)
        self.getjoystickdata.btn_rightstick_updown.connect(self.BtnRightstickUpDown)
        self.getjoystickdata.btn_rightstick_leftright.connect(self.BtnRightstickLeftRight)
        #endgion
        #regioin SDK_json下connect相应按钮的方法(函数)
        self.getjoystickdata.btn_l2.connect(self.Json_BtnL2)
        self.getjoystickdata.btn_l1.connect(self.Json_BtnL1)
        self.getjoystickdata.btn_left_up.connect(self.Json_BtnLeftUp)
        self.getjoystickdata.btn_left_left.connect(self.Json_BtnLeftLeft)
        self.getjoystickdata.btn_left_right.connect(self.Json_BtnLeftRight)
        self.getjoystickdata.btn_left_down.connect(self.Json_BtnLeftDown)
        self.getjoystickdata.btn_r2.connect(self.Json_BtnR2)
        self.getjoystickdata.btn_r1.connect(self.Json_BtnR1)
        self.getjoystickdata.btn_right_up.connect(self.Json_BtnRightUp)
        self.getjoystickdata.btn_right_left.connect(self.Json_BtnRightLeft)
        self.getjoystickdata.btn_right_right.connect(self.Json_BtnRightRight)
        self.getjoystickdata.btn_right_down.connect(self.Json_BtnRightDown)
        self.getjoystickdata.btn_leftstick_updown.connect(self.Json_BtnLeftstickUpDown)
        self.getjoystickdata.btn_leftstick_leftright.connect(self.Json_BtnLeftstickLeftRight)
        self.getjoystickdata.btn_rightstick_updown.connect(self.Json_BtnRightstickUpDown)
        self.getjoystickdata.btn_rightstick_leftright.connect(self.Json_BtnRightstickLeftRight)
        #endgion
        self.getjoystickdata.start()

        #region 调用函数GetDataThread()实例化创建一个8056的getdata线程
        # 线程的启动放在下面的函数def RobotAllState(self):  通过button 8056 pressed触发
        # 运行getdata线程，并保存getdata线程读取到的数据
        # 通过connect把最新的数据显示到对应***Display对应的文本框
        self.getdata = GetDataThread(self.startParm)
        self.getdata.latest_posj1.connect(self.posj1Display)
        self.getdata.latest_posj2.connect(self.posj2Display)
        self.getdata.latest_posj3.connect(self.posj3Display)
        self.getdata.latest_posj4.connect(self.posj4Display)
        self.getdata.latest_posj5.connect(self.posj5Display)
        self.getdata.latest_posj6.connect(self.posj6Display)

        self.getdata.latest_posex.connect(self.posexDisplay)
        self.getdata.latest_posey.connect(self.poseyDisplay)
        self.getdata.latest_posez.connect(self.posezDisplay)
        self.getdata.latest_poserx.connect(self.poserxDisplay)
        self.getdata.latest_posery.connect(self.poseryDisplay)
        self.getdata.latest_poserz.connect(self.poserzDisplay)

        self.getdata.latest_robotstate.connect(self.robotstateDisplay)
        self.getdata.latest_mode.connect(self.modeDisplay)
        self.getdata.latest_synchronize.connect(self.synchronizeDisplay)
        self.getdata.latest_synchronize.connect(self.brakeDisplay)
        #endregion

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        #region 定义SDK基本按钮名字、背景颜色以及在窗口的位置
        #-------------------------------------------------------------
        self.btn_8056on = QPushButton("8056on",self)
        self.btn_8056on.setStyleSheet('''QPushButton{background-color:rgb(255,0,255);border-radius:5px;}QPushButton:hover{background-color:rgb(255,255,0);}''')
        self.btn_8056on.move(10,0)
        #-------------------------------------------------------------
        self.btn_8056off = QPushButton("8056off",self)
        self.btn_8056off.setStyleSheet('''QPushButton{background-color:rgb(255,0,255);border-radius:5px;}QPushButton:hover{background-color:rgb(255,255,0);}''')
        self.btn_8056off.move(10,50)
        #-------------------------------------------------------------
        self.btn_createctx = QPushButton("CreateCtx",self)
        self.btn_createctx.setStyleSheet('''QPushButton{background-color:rgb(255,0,255);border-radius:5px;}QPushButton:hover{background-color:rgb(255,255,0);}''')
        self.btn_createctx.move(10,100)
        #-------------------------------------------------------------
        self.btn_login = QPushButton("Login",self)
        self.btn_login.setStyleSheet('''QPushButton{background-color:rgb(255,0,255);border-radius:5px;}QPushButton:hover{background-color:rgb(255,255,0);}''')
        self.btn_login.move(10,150)
        #-------------------------------------------------------------
        self.btn_logout = QPushButton("Logout",self)
        self.btn_logout.setStyleSheet('''QPushButton{background-color:rgb(255,0,255);border-radius:5px;}QPushButton:hover{background-color:rgb(255,255,0);}''')
        self.btn_logout.move(10,200)
        #-------------------------------------------------------------
        self.btn_destroyctx = QPushButton("DestroyCtx",self)
        self.btn_destroyctx.setStyleSheet('''QPushButton{background-color:rgb(255,0,255);border-radius:5px;}QPushButton:hover{background-color:rgb(255,255,0);}''')
        self.btn_destroyctx.move(10,250)
        #-------------------------------------------------------------
        self.btn_clearalarm = QPushButton("ClearAlarm",self)
        self.btn_clearalarm.setStyleSheet('''QPushButton{background-color:rgb(255,0,255);border-radius:5px;}QPushButton:hover{background-color:rgb(255,255,0);}''')
        self.btn_clearalarm.move(10,300)
        #-------------------------------------------------------------
        self.btn_syn = QPushButton("Syn",self)
        self.btn_syn.setStyleSheet('''QPushButton{background-color:rgb(255,0,255);border-radius:5px;}QPushButton:hover{background-color:rgb(255,255,0);}''')
        self.btn_syn.move(10,350)
        #-------------------------------------------------------------
        self.btn_unsyn = QPushButton("UnSyn",self)
        self.btn_unsyn.setStyleSheet('''QPushButton{background-color:rgb(255,0,255);border-radius:5px;}QPushButton:hover{background-color:rgb(255,255,0);}''')
        self.btn_unsyn.move(10,400)
        #-------------------------------------------------------------
        self.btn_servoenable = QPushButton("ServoEnable",self)
        self.btn_servoenable.setStyleSheet('''QPushButton{background-color:rgb(255,0,255);border-radius:5px;}QPushButton:hover{background-color:rgb(255,255,0);}''')
        self.btn_servoenable.move(10,450)
        #-------------------------------------------------------------
        self.btn_run = QPushButton("Run",self)
        self.btn_run.setStyleSheet('''QPushButton{background-color:rgb(255,0,255);border-radius:5px;}QPushButton:hover{background-color:rgb(255,255,0);}''')
        self.btn_run.move(10,500)
        #-------------------------------------------------------------
        self.btn_pause = QPushButton("Pause",self)
        self.btn_pause.setStyleSheet('''QPushButton{background-color:rgb(255,0,255);border-radius:5px;}QPushButton:hover{background-color:rgb(255,255,0);}''')
        self.btn_pause.move(10,550)
        #-------------------------------------------------------------
        self.btn_dragmove = QPushButton("DragMove",self)
        self.btn_dragmove.setStyleSheet('''QPushButton{background-color:rgb(255,0,255);border-radius:5px;}QPushButton:hover{background-color:rgb(255,255,0);}''')
        self.btn_dragmove .move(10,600)
        #-------------------------------------------------------------
        self.btn_Var_M = QPushButton("Var_M",self)
        self.btn_Var_M.setStyleSheet('''QPushButton{background-color:rgb(255,0,255);border-radius:5px;}QPushButton:hover{background-color:rgb(255,255,0);}''')
        #self.btn_Var_M.move(10,650)
        self.btn_Var_M.setGeometry(10,650,70,30)
        #-------------------------------------------------------------
        self.btn_waypoint = QPushButton("Waypoint",self)
        self.btn_waypoint.setStyleSheet('''QPushButton{background-color:rgb(255,0,255);border-radius:5px;}QPushButton:hover{background-color:rgb(255,255,0);}''')
        self.btn_waypoint.move(10,700)
        #-------------------------------------------------------------
        self.btn_stop = QPushButton("Stop",self)
        self.btn_stop.setStyleSheet('''QPushButton{background-color:rgb(255,0,255);border-radius:5px;}QPushButton:hover{background-color:rgb(255,255,0);}''')
        self.btn_stop.move(10,750)
        #-------------------------------------------------------------
        self.btn_output = QPushButton("Output_Y",self)
        self.btn_output.setStyleSheet('''QPushButton{background-color:rgb(255,0,255);border-radius:5px;}QPushButton:hover{background-color:rgb(255,255,0);}''')
        #self.btn_output.move(10,800)
        self.btn_output.setGeometry(10,800,70,30)
        #-------------------------------------------------------------
        #endregion

        #region 定义SDK Button 定义关节J1 J2 J3 J4 J5 J6按钮以及在窗口的位置
        btn_j1negative = QPushButton("J1-",self)
        btn_j1negative.setGeometry(130,250,60,30) #（x坐标，y坐标，宽，高）
        #btn_j1negative.move(150,0)
        #-------------------------------------------------------------
        btn_j1positive = QPushButton("J1+",self)
        btn_j1positive.setGeometry(280,250,60,30) #（x坐标，y坐标，宽，高）
        #btn_j1positive.move(250,0)
        #-------------------------------------------------------------
        btn_j2negative = QPushButton("J2-",self)
        btn_j2negative.setGeometry(130,300,60,30) #（x坐标，y坐标，宽，高）
        #-------------------------------------------------------------
        btn_j2positive = QPushButton("J2+",self)
        btn_j2positive.setGeometry(280,300,60,30) #（x坐标，y坐标，宽，高）
        #-------------------------------------------------------------
        #-------------------------------------------------------------
        btn_j3negative = QPushButton("J3-",self)
        btn_j3negative.setGeometry(130,350,60,30) #（x坐标，y坐标，宽，高）
        #-------------------------------------------------------------
        btn_j3positive = QPushButton("J3+",self)
        btn_j3positive.setGeometry(280,350,60,30) #（x坐标，y坐标，宽，高）
        #-------------------------------------------------------------
        #-------------------------------------------------------------
        btn_j4negative = QPushButton("J4-",self)
        btn_j4negative.setGeometry(130,400,60,30) #（x坐标，y坐标，宽，高）
        #-------------------------------------------------------------
        btn_j4positive = QPushButton("J4+",self)
        btn_j4positive.setGeometry(280,400,60,30) #（x坐标，y坐标，宽，高）
        #-------------------------------------------------------------
        #-------------------------------------------------------------
        btn_j5negative = QPushButton("J5-",self)
        btn_j5negative.setGeometry(130,450,60,30) #（x坐标，y坐标，宽，高）
        #-------------------------------------------------------------
        btn_j5positive = QPushButton("J5+",self)
        btn_j5positive.setGeometry(280,450,60,30) #（x坐标，y坐标，宽，高）
        #-------------------------------------------------------------
        #-------------------------------------------------------------
        btn_j6negative = QPushButton("J6-",self)
        btn_j6negative.setGeometry(130,500,60,30) #（x坐标，y坐标，宽，高）
        #-------------------------------------------------------------
        btn_j6positive = QPushButton("J6+",self)
        btn_j6positive.setGeometry(280,500,60,30) #（x坐标，y坐标，宽，高）
        #-------------------------------------------------------------
        #endregion

        #region 定义SDK Button 定义X Y Z Rx Ry Rz 按钮以及在窗口的位置
        btn_xnegative = QPushButton("X-",self)
        btn_xnegative.setGeometry(370,250,60,30) #（x坐标，y坐标，宽，高）
        #-------------------------------------------------------------
        btn_xpositive = QPushButton("X+",self)
        btn_xpositive.setGeometry(520,250,60,30) #（x坐标，y坐标，宽，高）
        #-------------------------------------------------------------
        btn_ynegative = QPushButton("Y-",self)
        btn_ynegative.setGeometry(370,300,60,30) #（x坐标，y坐标，宽，高）
        #-------------------------------------------------------------
        btn_ypositive = QPushButton("Y+",self)
        btn_ypositive.setGeometry(520,300,60,30) #（x坐标，y坐标，宽，高）
        #-------------------------------------------------------------
        btn_znegative = QPushButton("Z-",self)
        btn_znegative.setGeometry(370,350,60,30) #（x坐标，y坐标，宽，高）
        #-------------------------------------------------------------
        btn_zpositive = QPushButton("Z+",self)
        btn_zpositive.setGeometry(520,350,60,30) #（x坐标，y坐标，宽，高）
        #-------------------------------------------------------------
        btn_rxnegative = QPushButton("Rx-",self)
        btn_rxnegative.setGeometry(370,400,60,30) #（x坐标，y坐标，宽，高）
        #-------------------------------------------------------------
        btn_rxpositive = QPushButton("Rx+",self)
        btn_rxpositive.setGeometry(520,400,60,30) #（x坐标，y坐标，宽，高）
        #-------------------------------------------------------------
        btn_rynegative = QPushButton("Ry-",self)
        btn_rynegative.setGeometry(370,450,60,30) #（x坐标，y坐标，宽，高）
        #-------------------------------------------------------------
        btn_rypositive = QPushButton("Ry+",self)
        btn_rypositive.setGeometry(520,450,60,30) #（x坐标，y坐标，宽，高）
        #-------------------------------------------------------------
        btn_rznegative = QPushButton("Rz-",self)
        btn_rznegative.setGeometry(370,500,60,30) #（x坐标，y坐标，宽，高）
        #-------------------------------------------------------------
        btn_rzpositive = QPushButton("Rz+",self)
        btn_rzpositive.setGeometry(520,500,60,30) #（x坐标，y坐标，宽，高）
        #-------------------------------------------------------------
        #endregion

        #region 定义json基本按钮名字、背景颜色以及在窗口的位置
        #-------------------------------------------------------------
        self.btn_createsocket = QPushButton("CreateSocket",self)
        self.btn_createsocket.setStyleSheet('''QPushButton{background-color:rgb(255,0,255);border-radius:5px;}QPushButton:hover{background-color:rgb(255,255,0);}''')
        self.btn_createsocket.move(640,0)
        #-------------------------------------------------------------
        self.btn_closesocket = QPushButton("CloseSocket",self)
        self.btn_closesocket.setStyleSheet('''QPushButton{background-color:rgb(255,0,255);border-radius:5px;}QPushButton:hover{background-color:rgb(255,255,0);}''')
        self.btn_closesocket.move(640,50)
        #-------------------------------------------------------------
        self.btn_checkjbiexist = QPushButton("JBIExist",self)
        self.btn_checkjbiexist.setStyleSheet('''QPushButton{background-color:rgb(255,0,255);border-radius:5px;}QPushButton:hover{background-color:rgb(255,255,0);}''')
        self.btn_checkjbiexist.move(640,100)
        #-------------------------------------------------------------
        self.btn_runjbi = QPushButton("RunJBI",self)
        self.btn_runjbi.setStyleSheet('''QPushButton{background-color:rgb(255,0,255);border-radius:5px;}QPushButton:hover{background-color:rgb(255,255,0);}''')
        self.btn_runjbi.move(640,150)
        #-------------------------------------------------------------
        self.btn_set_payload = QPushButton("ToolLoad",self)
        self.btn_set_payload.setStyleSheet('''QPushButton{background-color:rgb(255,0,255);border-radius:5px;}QPushButton:hover{background-color:rgb(255,255,0);}''')
        self.btn_set_payload.move(640,200)
        #-------------------------------------------------------------
        self.btn_pathmove_v2 = QPushButton("路点2.0绕工具",self)
        self.btn_pathmove_v2.setStyleSheet('''QPushButton{background-color:rgb(255,0,255);border-radius:5px;}QPushButton:hover{background-color:rgb(255,255,0);}''')
        self.btn_pathmove_v2.move(640,250)
        #-------------------------------------------------------------
        self.btn_ps2tt = QPushButton("PS2 透传",self)
        self.btn_ps2tt.setStyleSheet('''QPushButton{background-color:rgb(255,0,255);border-radius:5px;}QPushButton:hover{background-color:rgb(255,255,0);}''')
        self.btn_ps2tt.move(640,300)
        #-------------------------------------------------------------
        self.btn_json_set_m = QPushButton("json_M",self)
        self.btn_json_set_m.setStyleSheet('''QPushButton{background-color:rgb(255,0,255);border-radius:5px;}QPushButton:hover{background-color:rgb(255,255,0);}''')
        #self.btn_set_json_m.move(640,350)
        self.btn_json_set_m.setGeometry(640,350,60,30)
        #-------------------------------------------------------------
        self.btn_json_set_y = QPushButton("json_Y",self)
        self.btn_json_set_y.setStyleSheet('''QPushButton{background-color:rgb(255,0,255);border-radius:5px;}QPushButton:hover{background-color:rgb(255,255,0);}''')
        #self.btn_set_json_y.move(640,400)
        self.btn_json_set_y.setGeometry(640,400,60,30)
        #-------------------------------------------------------------
        self.btn_json_movj = QPushButton("MOVJ",self)
        self.btn_json_movj.setStyleSheet('''QPushButton{background-color:rgb(255,0,255);border-radius:5px;}QPushButton:hover{background-color:rgb(255,255,0);}''')
        self.btn_json_movj.setGeometry(640,450,50,30)
        #-------------------------------------------------------------
        self.btn_methodtest = QPushButton("MethodTest",self)
        self.btn_methodtest.setStyleSheet('''QPushButton{background-color:rgb(255,0,255);border-radius:5px;}QPushButton:hover{background-color:rgb(255,255,0);}''')
        self.btn_methodtest.move(640,910)
        #-------------------------------------------------------------
        #endregion

        #!!!!!!!!!!!!!!!!!!!!!!! Label !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #region Label标签文字 机器人各状态
        labelrobotstate = QLabel('RobotState',self)
        labelrobotstate.setGeometry(130,0,120,30)
        labelmode = QLabel('Mode',self)
        labelmode.setGeometry(130,50,120,30)
        labelsyn = QLabel('SynState',self)
        labelsyn.setGeometry(130,100,120,30)
        labelbrake = QLabel('BrakeState',self)
        labelbrake.setGeometry(130,150,120,30)

        labelteachspeed = QLabel('TEACHSpeed',self)
        labelteachspeed.setGeometry(420,00,120,30)
        labelplayspeed = QLabel('PLAYSpeed',self)
        labelplayspeed.setGeometry(420,50,120,30)
        labelcoordinate = QLabel('Coordinate',self)
        labelcoordinate.setGeometry(420,100,120,30)
        labeltoolnum = QLabel('ToolNum',self)
        labeltoolnum.setGeometry(420,150,120,30)
        labelusernum = QLabel('UserNum',self)
        labelusernum.setGeometry(420,200,120,30)
        #endregion

        '''
        #region Joystick PS2的各种状态
        L2 = QLabel("按钮L2", self)
        L2.setGeometry(130,600,120,30)
        L1 = QLabel("按钮L1", self)
        L1.setGeometry(130,650,120,30)
        HatLeft = QLabel("帽子左", self)
        L2.setGeometry(130,600,120,30)
        LeftGanUpDown = QLabel("左杆上下",self)
        LeftGanUpDown.setGeometry(130,600,120,30)
        LeftGanUpDown = QLabel("左杆左右",self)
        LeftGanUpDown.setGeometry(130,600,120,30)
        #endregion
        '''
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        
        #region SDK button 触发的函数
        #clicked指的是按下在松开时触发
        #pressed指的是按下触发
        #self.btn_8056on.clicked.connect(self.SDK_buttonClicked)
        #self.btn_8056off.clicked.connect(self.SDK_buttonClicked)
        self.btn_8056on.pressed.connect(self.RobotAllState)
        self.btn_8056off.pressed.connect(self.RobotAllState)
        
        self.btn_createctx.clicked.connect(self.SDK_buttonClicked)
        self.btn_login.clicked.connect(self.SDK_buttonClicked)
        self.btn_logout.clicked.connect(self.SDK_buttonClicked)
        self.btn_destroyctx.clicked.connect(self.SDK_buttonClicked)
        self.btn_Var_M.clicked.connect(self.SDK_buttonClicked)
        self.btn_syn.clicked.connect(self.SDK_buttonClicked)
        self.btn_unsyn.clicked.connect(self.SDK_buttonClicked)
        self.btn_clearalarm.clicked.connect(self.SDK_buttonClicked)
        self.btn_servoenable.clicked.connect(self.SDK_buttonClicked)
        self.btn_run.clicked.connect(self.SDK_buttonClicked)
        self.btn_pause.clicked.connect(self.SDK_buttonClicked)
        self.btn_dragmove.clicked.connect(self.SDK_buttonClicked)
        self.btn_waypoint.clicked.connect(self.SDK_buttonClicked)
        self.btn_stop.pressed.connect(self.SDK_buttonClicked)
        self.btn_output.pressed.connect(self.SDK_buttonClicked)

        #region 定义关节J1 J2 J3 J4 J5 J6按钮pressed连接的函数
        #J1
        #点击信号与槽函数进行连接，实现的目的：输入安妞的当前状态，按下还是释放
        #btn_j1negative.clicked.connect(lambda:self.btnstate(btn_j1negative))
        #J1
        btn_j1negative.pressed.connect(lambda:self.btnstate(btn_j1negative))
        btn_j1negative.released.connect(self.SDK_buttonClicked)
        #btn_j1negative.setAutoRepeat(True)
        btn_j1negative.setAutoRepeatDelay(150)
        btn_j1negative.setAutoRepeatInterval(1)
        #btn_j1positive.clicked.connect(self.SDK_buttonClicked)
        btn_j1positive.pressed.connect(lambda:self.btnstate(btn_j1positive))
        btn_j1positive.released.connect(self.SDK_buttonClicked)
        #btn_j1positive.setAutoRepeat(True)
        btn_j1positive.setAutoRepeatDelay(150)
        btn_j1positive.setAutoRepeatInterval(1)
        #J2
        btn_j2negative.pressed.connect(lambda:self.btnstate(btn_j2negative))
        btn_j2negative.released.connect(self.SDK_buttonClicked)
        #btn_j2negative.setAutoRepeat(True)
        btn_j2negative.setAutoRepeatDelay(150)
        btn_j2negative.setAutoRepeatInterval(1)
        btn_j2positive.pressed.connect(lambda:self.btnstate(btn_j2positive))
        btn_j2positive.released.connect(self.SDK_buttonClicked)
        #btn_j2positive.setAutoRepeat(True)
        btn_j2positive.setAutoRepeatDelay(150)
        btn_j2positive.setAutoRepeatInterval(1)
        #J3
        btn_j3negative.pressed.connect(lambda:self.btnstate(btn_j3negative))
        btn_j3negative.released.connect(self.SDK_buttonClicked)
        #btn_j3negative.setAutoRepeat(True)
        btn_j3negative.setAutoRepeatDelay(150)
        btn_j3negative.setAutoRepeatInterval(1)
        btn_j3positive.pressed.connect(lambda:self.btnstate(btn_j3positive))
        btn_j3positive.released.connect(self.SDK_buttonClicked)
        #btn_j3positive.setAutoRepeat(True)
        btn_j3positive.setAutoRepeatDelay(150)
        btn_j3positive.setAutoRepeatInterval(1)
        #J4
        btn_j4negative.pressed.connect(lambda:self.btnstate(btn_j4negative))
        btn_j4negative.released.connect(self.SDK_buttonClicked)
        #btn_j4negative.setAutoRepeat(True)
        btn_j4negative.setAutoRepeatDelay(150)
        btn_j4negative.setAutoRepeatInterval(1)
        btn_j4positive.pressed.connect(lambda:self.btnstate(btn_j4positive))
        btn_j4positive.released.connect(self.SDK_buttonClicked)
        #btn_j4positive.setAutoRepeat(True)
        btn_j4positive.setAutoRepeatDelay(150)
        btn_j4positive.setAutoRepeatInterval(1)
        #J5
        btn_j5negative.pressed.connect(lambda:self.btnstate(btn_j5negative))
        btn_j5negative.released.connect(self.SDK_buttonClicked)
        #btn_j5negative.setAutoRepeat(True)
        btn_j5negative.setAutoRepeatDelay(150)
        btn_j5negative.setAutoRepeatInterval(1)
        btn_j5positive.pressed.connect(lambda:self.btnstate(btn_j5positive))
        btn_j5positive.released.connect(self.SDK_buttonClicked)
        #btn_j5positive.setAutoRepeat(True)
        btn_j5positive.setAutoRepeatDelay(150)
        btn_j5positive.setAutoRepeatInterval(1)
        #J6
        btn_j6negative.pressed.connect(lambda:self.btnstate(btn_j6negative))
        btn_j6negative.released.connect(self.SDK_buttonClicked)
        #btn_j6negative.setAutoRepeat(True)
        btn_j6negative.setAutoRepeatDelay(150)
        btn_j6negative.setAutoRepeatInterval(1)
        btn_j6positive.pressed.connect(lambda:self.btnstate(btn_j6positive))
        btn_j6positive.released.connect(self.SDK_buttonClicked)
        #btn_j6positive.setAutoRepeat(True)
        btn_j6positive.setAutoRepeatDelay(150)
        btn_j6positive.setAutoRepeatInterval(1)
        #endregion
        #region 定义X Y Z Rx Ry Rz 按钮pressed连接
        #X
        btn_xnegative.pressed.connect(lambda:self.btnstate(btn_xnegative))
        btn_xnegative.released.connect(self.SDK_buttonClicked)
        #btn_xnegative.setAutoRepeat(True)
        btn_xnegative.setAutoRepeatDelay(150)
        btn_xnegative.setAutoRepeatInterval(1)
        btn_xpositive.pressed.connect(lambda:self.btnstate(btn_xpositive))
        btn_xpositive.released.connect(self.SDK_buttonClicked)
        #btn_xpositive.setAutoRepeat(True)
        btn_xpositive.setAutoRepeatDelay(150)
        btn_xpositive.setAutoRepeatInterval(1)
        #Y
        btn_ynegative.pressed.connect(lambda:self.btnstate(btn_ynegative))
        btn_ynegative.released.connect(self.SDK_buttonClicked)
        #btn_ynegative.setAutoRepeat(True)
        btn_ynegative.setAutoRepeatDelay(150)
        btn_ynegative.setAutoRepeatInterval(1)
        btn_ypositive.pressed.connect(lambda:self.btnstate(btn_ypositive))
        btn_ypositive.released.connect(self.SDK_buttonClicked)
        #btn_ypositive.setAutoRepeat(True)
        btn_ypositive.setAutoRepeatDelay(150)
        btn_ypositive.setAutoRepeatInterval(1)
        #Z
        btn_znegative.pressed.connect(lambda:self.btnstate(btn_znegative))
        btn_znegative.released.connect(self.SDK_buttonClicked)
        #btn_znegative.setAutoRepeat(True)
        btn_znegative.setAutoRepeatDelay(150)
        btn_znegative.setAutoRepeatInterval(1)
        btn_zpositive.pressed.connect(lambda:self.btnstate(btn_zpositive))
        btn_zpositive.released.connect(self.SDK_buttonClicked)
        #btn_zpositive.setAutoRepeat(True)
        btn_zpositive.setAutoRepeatDelay(150)
        btn_zpositive.setAutoRepeatInterval(1)
        #Rx
        btn_rxnegative.pressed.connect(lambda:self.btnstate(btn_rxnegative))
        btn_rxnegative.released.connect(self.SDK_buttonClicked)
        #btn_rxnegative.setAutoRepeat(True)
        btn_rxnegative.setAutoRepeatDelay(150)
        btn_rxnegative.setAutoRepeatInterval(1)
        btn_rxpositive.pressed.connect(lambda:self.btnstate(btn_rxpositive))
        btn_rxpositive.released.connect(self.SDK_buttonClicked)
        #btn_rxpositive.setAutoRepeat(True)
        btn_rxpositive.setAutoRepeatDelay(150)
        btn_rxpositive.setAutoRepeatInterval(1)
        #Ry
        btn_rynegative.pressed.connect(lambda:self.btnstate(btn_rynegative))
        btn_rynegative.released.connect(self.SDK_buttonClicked)
        #btn_rynegative.setAutoRepeat(True)
        btn_rynegative.setAutoRepeatDelay(150)
        btn_rynegative.setAutoRepeatInterval(1)
        btn_rypositive.pressed.connect(lambda:self.btnstate(btn_rypositive))
        btn_rypositive.released.connect(self.SDK_buttonClicked)
        #btn_rypositive.setAutoRepeat(True)
        btn_rypositive.setAutoRepeatDelay(150)
        btn_rypositive.setAutoRepeatInterval(1)
        #Rz
        btn_rznegative.pressed.connect(lambda:self.btnstate(btn_rznegative))
        btn_rznegative.released.connect(self.SDK_buttonClicked)
        #btn_rznegative.setAutoRepeat(True)
        btn_rznegative.setAutoRepeatDelay(150)
        btn_rznegative.setAutoRepeatInterval(1)
        btn_rzpositive.pressed.connect(lambda:self.btnstate(btn_rzpositive))
        btn_rzpositive.released.connect(self.SDK_buttonClicked)
        #btn_rzpositive.setAutoRepeat(True)
        btn_rzpositive.setAutoRepeatDelay(150)
        btn_rzpositive.setAutoRepeatInterval(1)
        #endregion
        #endregion
        
        #region json协议 button 触发的函数
        self.btn_createsocket.pressed.connect(self.json_buttonClicked)
        self.btn_closesocket.pressed.connect(self.json_buttonClicked)
        #josnSendMethod(self,sock,method,params=None,id=1):
        '''
        btn_runjbi.pressed.connect(lambda:self.josnSendMethod(self.sock,"checkJbiExist",{"filename":"ab.jbi"}))
        btn_runjbi.setAutoRepeat(True)
        btn_runjbi.setAutoRepeatDelay(150)
        btn_runjbi.setAutoRepeatInterval(1)
        '''
        self.btn_runjbi.pressed.connect(self.json_buttonClicked)
        self.btn_set_payload.pressed.connect(self.json_buttonClicked)
        self.btn_pathmove_v2.pressed.connect(self.json_buttonClicked)
        self.btn_json_set_y.pressed.connect(self.json_buttonClicked)
        self.btn_json_set_m.pressed.connect(self.json_buttonClicked)
        self.btn_json_movj.pressed.connect(self.json_buttonClicked)
        self.btn_methodtest.pressed.connect(self.json_buttonClicked)
        #endregion
        self.statusBar()

        #btn_operationmode = QPushButton("Operation Mode",self)
        #button.move("This is an example button")
        btn_teach = QRadioButton("TEACH",self)                        #实例化一个单选择的按钮
        btn_teach.setChecked(True)                                    #设置按钮点点击状态
        btn_teach.toggled.connect(lambda:self.btnstate(btn_teach))    #绑定点击事件
        btn_teach.move(10,880)
        btn_play = QRadioButton("PLAY",self)                           #实例化一个单选择的按钮
        btn_play.setChecked(True)                                      #设置按钮点点击状态
        btn_play.toggled.connect(lambda:self.btnstate(btn_play))       #绑定点击事件
        btn_play.move(10,900)
        btn_remote = QRadioButton("REMOTE",self)                       #实例化一个单选择的按钮
        btn_remote.setChecked(True)                                    #设置按钮点点击状态
        btn_remote.toggled.connect(lambda:self.btnstate(btn_remote))   #绑定点击事件
        btn_remote.move(10,920)
        self.show()

    #实时读取当前系统的时间并写入到GUI
    def timeDisplay(self,data):
        self.input_time.setText(data)

    #region 以下是各按钮clicked或者pressed后触发的函数或者调用GetDataThread实例化getdata线程触发的函数
    #region 调用GetDataThread实例化getdata线程读取到的数据--关节角度(pos)写入并显示到UI页面
    def posj1Display(self,data):
        self.latest_posj1.setText(data)
    def posj2Display(self,data):
        self.latest_posj2.setText(data)
    def posj3Display(self,data):
        self.latest_posj3.setText(data)
    def posj4Display(self,data):
        self.latest_posj4.setText(data)
    def posj5Display(self,data):
        self.latest_posj5.setText(data)
    def posj6Display(self,data):
        self.latest_posj6.setText(data)
    #endregion

    #region 调用GetDataThread实例化getdata线程读取到的数据--world下的位姿(X Y Z Rx Ry Rz)写入并显示到UI页面里
    def posexDisplay(self,data):
        self.latest_posex.setText(data)
    def poseyDisplay(self,data):
        self.latest_posey.setText(data)
    def posezDisplay(self,data):
        self.latest_posez.setText(data)
    def poserxDisplay(self,data):
        self.latest_poserx.setText(data)
    def poseryDisplay(self,data):
        self.latest_posery.setText(data)
    def poserzDisplay(self,data):
        self.latest_poserz.setText(data)
    #endregion

    #region 调用GetDataThread实例化getdata线程读取到的数据--机器人状态写入并显示到UI页面里机器人状态
    def robotstateDisplay(self,data):
        if data =="0":
            data = "Stop"
        if data =="1":
            data = "Pause"
        if data =="3":
            data = "Running"
        if data == "4":
            data = "Error"
            print("急停中...")
            self.btn_servoenable.setStyleSheet('''QPushButton{background-color:rgb(255,0,255);border-radius:5px;}QPushButton:hover{background-color:rgb(255,255,0);}''')
        self.latest_robotstate.setText(data)
    def modeDisplay(self,data):
        if data =="0":
            data = "TEACH"
        if data =="1":
            data = "PLAY"
        if data =="2":
            data = "REMOTE"
        self.latest_mode.setText(data)
    def synchronizeDisplay(self,data):
        if data =="0":
            data = "未同步"
        if data =="1":
            data = "同步"
            self.btn_servoenable.setStyleSheet('''QPushButton{background-color:rgb(255,0,255);border-radius:5px;}QPushButton:hover{background-color:rgb(255,255,0);}''')
        self.latest_synchronize.setText(data)
    def brakeDisplay(self,data):
        if data =="0":
            data = "Brake"
        if data =="1":
            data = "ReleaseBrake"
        self.latest_brake.setText(data)
    #endregion

    #region SDK__C++和C语言的动态链接库和静态链接库
    # 在elt_login成功后，调用GetJopstickDataThread实例化后的getjoystickdata，elt_login成功后SDK_on=1，操作手柄才有效
    # 实时读取已经连接好PS2的各按键的数值
    # 把数值写入到窗口的框框，同时有定义了功能的按键，调用相应的jog
    def JoystickName(self,data):
        self.joystick_status.setText(data)
    def BtnL2(self,data):
        #print("----",self.elt_ctx_self)
        self.btn_l2.setText(data)
        num_data = float(data)
        if self.ret_login == 1 and num_data == 0 and self.button_on == 1 and self.SDK_on == 1:
            state = c_long(0)
            ret = Elite_dll.elt_get_robot_state(c_void_p(self.elt_ctx_self), byref(state), byref(error_message))
            if state.value == 3 and num_data == 0:
                ret = Elite_dll.elt_stop(c_void_p(self.elt_ctx_self), byref(error_message))
                self.button_on = 0
        if num_data == 1 and self.ret_login == 1 and self.SDK_on == 1:
            self.button_on = 1
            index = c_long(0)
            index.value = 5
            ret = Elite_dll.elt_jog(c_void_p(self.elt_ctx_self), index, byref(error_message))
    def BtnL1(self,data):
        self.btn_l1.setText(data)
        num_data = float(data)
        if self.ret_login == 1 and num_data == 0 and self.button_on == 2 and self.SDK_on == 1:
            state = c_long(0)
            ret = Elite_dll.elt_get_robot_state(c_void_p(self.elt_ctx_self), byref(state), byref(error_message))
            if state.value == 3 and num_data == 0:
                ret = Elite_dll.elt_stop(c_void_p(self.elt_ctx_self), byref(error_message))
                self.button_on = 0
        if num_data == 1 and self.ret_login == 1 and self.SDK_on == 1:
            self.button_on = 2
            index = c_long(0)
            index.value = 4
            ret = Elite_dll.elt_jog(c_void_p(self.elt_ctx_self), index, byref(error_message))
    def BtnLeftUp(self,data):
        self.btn_left_up.setText(data)
    def BtnLeftLeft(self,data):
        self.btn_left_left.setText(data)
    def BtnLeftRight(self,data):
        self.btn_left_right.setText(data)
    def BtnLeftDown(self,data):
        self.btn_left_down.setText(data)
    def BtnR2(self,data):
        self.btn_r2.setText(data)
        num_data = float(data)
        if self.ret_login == 1 and num_data == 0 and self.button_on == 3 and self.SDK_on == 1:
            state = c_long(0)
            ret = Elite_dll.elt_get_robot_state(c_void_p(self.elt_ctx_self), byref(state), byref(error_message))
            if state.value == 3 and num_data == 0:
                ret = Elite_dll.elt_stop(c_void_p(self.elt_ctx_self), byref(error_message))
                self.button_on = 0
        if num_data == 1 and self.ret_login == 1 and self.SDK_on == 1:
            self.button_on = 3
            index = c_long(0)
            index.value = 11
            ret = Elite_dll.elt_jog(c_void_p(self.elt_ctx_self), index, byref(error_message))
    def BtnR1(self,data):
        self.btn_r1.setText(data)
        num_data = float(data)
        if self.ret_login == 1 and num_data == 0 and self.button_on == 4 and self.SDK_on == 1:
            state = c_long(0)
            ret = Elite_dll.elt_get_robot_state(c_void_p(self.elt_ctx_self), byref(state), byref(error_message))
            if state.value == 3 and num_data == 0:
                ret = Elite_dll.elt_stop(c_void_p(self.elt_ctx_self), byref(error_message))
                self.button_on = 0
        if num_data == 1 and self.ret_login == 1 and self.SDK_on == 1:
            self.button_on = 4
            index = c_long(0)
            index.value = 10
            ret = Elite_dll.elt_jog(c_void_p(self.elt_ctx_self), index, byref(error_message))
    def BtnRightUp(self,data):
        self.btn_right_up.setText(data)
    def BtnRightLeft(self,data):
        self.btn_right_left.setText(data)
        # "复位SDK c++或c的动态链接库"
        '''
        if data == "1":
            self.SDK_on = 0
        '''
    def BtnRightRight(self,data):
        self.btn_right_right.setText(data)
    def BtnRightDown(self,data):
        self.btn_right_down.setText(data)
    def BtnLeftstickUpDown(self,data):
        #print("====",str(self.elt_ctx_self))
        self.btn_leftstick_updown.setText(data)
        num_data = float(data)
        if self.ret_login == 1 and num_data == 0 and self.button_on == 5 and self.SDK_on == 1:
            state = c_long(0)
            ret = Elite_dll.elt_get_robot_state(c_void_p(self.elt_ctx_self), byref(state), byref(error_message))
            if state.value == 3 and num_data == 0:
                ret = Elite_dll.elt_stop(c_void_p(self.elt_ctx_self), byref(error_message))
                self.button_on = 0
        if num_data > 0.1 and self.ret_login == 1 and self.SDK_on == 1:
            self.button_on = 5
            index = c_long(0)
            index.value = 0
            ret = Elite_dll.elt_jog(c_void_p(self.elt_ctx_self), index, byref(error_message))
        if num_data < -0.1 and self.ret_login == 1 and self.SDK_on == 1:
            self.button_on = 5
            index = c_long(0)
            index.value = 1
            ret = Elite_dll.elt_jog(c_void_p(self.elt_ctx_self), index, byref(error_message))
    def BtnLeftstickLeftRight(self,data):
        self.btn_leftstick_leftright.setText(data)
        num_data = float(data)
        if self.ret_login == 1 and num_data == 0 and self.button_on == 7 and self.SDK_on == 1:
            state = c_long(0)
            ret = Elite_dll.elt_get_robot_state(c_void_p(self.elt_ctx_self), byref(state), byref(error_message))
            if state.value == 3 and num_data == 0:
                ret = Elite_dll.elt_stop(c_void_p(self.elt_ctx_self), byref(error_message))
                self.button_on = 0
        if num_data > 0.1 and self.ret_login == 1 and self.SDK_on == 1:
            self.button_on = 7
            index = c_long(0)
            index.value = 2
            ret = Elite_dll.elt_jog(c_void_p(self.elt_ctx_self), index, byref(error_message))
        if num_data < -0.1 and self.ret_login == 1 and self.SDK_on == 1:
            self.button_on = 7
            index = c_long(0)
            index.value = 3
            ret = Elite_dll.elt_jog(c_void_p(self.elt_ctx_self), index, byref(error_message))
    def BtnRightstickUpDown(self,data):
        self.btn_rightstick_updown.setText(data)
        num_data = float(data)
        if self.ret_login == 1 and num_data == 0 and self.button_on == 9 and self.SDK_on == 1:
            state = c_long(0)
            ret = Elite_dll.elt_get_robot_state(c_void_p(self.elt_ctx_self), byref(state), byref(error_message))
            if state.value == 3 and num_data == 0:
                ret = Elite_dll.elt_stop(c_void_p(self.elt_ctx_self), byref(error_message))
                self.button_on = 0
        if num_data > 0.1 and self.ret_login == 1 and self.SDK_on == 1:
            self.button_on = 9
            index = c_long(0)
            index.value = 6
            ret = Elite_dll.elt_jog(c_void_p(self.elt_ctx_self), index, byref(error_message))
        if num_data < -0.1 and self.ret_login == 1 and self.SDK_on == 1:
            self.button_on = 9
            index = c_long(0)
            index.value = 7
            ret = Elite_dll.elt_jog(c_void_p(self.elt_ctx_self), index, byref(error_message))
    def BtnRightstickLeftRight(self,data):
        self.btn_rightstick_leftright.setText(data)
        num_data = float(data)
        if self.ret_login == 1 and num_data == 0 and self.button_on == 11 and self.SDK_on == 1:
            state = c_long(0)
            ret = Elite_dll.elt_get_robot_state(c_void_p(self.elt_ctx_self), byref(state), byref(error_message))
            if state.value == 3 and num_data == 0:
                ret = Elite_dll.elt_stop(c_void_p(self.elt_ctx_self), byref(error_message))
                self.button_on = 0
        if num_data > 0.1 and self.ret_login == 1 and self.SDK_on == 1:
            self.button_on = 11
            index = c_long(0)
            index.value = 8
            ret = Elite_dll.elt_jog(c_void_p(self.elt_ctx_self), index, byref(error_message))
        if num_data < -0.1 and self.ret_login == 1 and self.SDK_on == 1:
            self.button_on = 11
            index = c_long(0)
            index.value = 9
            ret = Elite_dll.elt_jog(c_void_p(self.elt_ctx_self), index, byref(error_message))
    #endregion
    
    # region SDK__json，实时更新第752行的各全局json变量下PS2摇杆按钮的值
    # 第988行，调用GetJopstickDataThread实例化后的getjoystickdata
    # GetJopstickDataThread传回的字符串值，保存到self.getjoystickdata.btn_l2
    # connect到json_BtnL2()，字符串值传入到data
    # 再把data转换成float复制给对应的按钮self.json_btnl2_value
    def Json_BtnL2(self,data):
        self.json_btn_l2_value = float(data)
        if self.SDK_json_on == 1 and self.json_btn_l2_value == 0 and self.json_ps2_button_on == 1:
            self.json_ps2_button_on = 0
            #stop
            print("stop")
        if self.SDK_json_on == 1 and self.json_btn_l2_value == 1:
            self.json_ps2_button_on = 1
            print("self.json_btn_l2_value",self.json_btn_l2_value)
    def Json_BtnL1(self,data):
        self.json_btn_l1_value = float(data)
        if self.SDK_json_on == 1 and self.json_btn_l1_value == 0 and self.json_ps2_button_on == 2:
            self.json_ps2_button_on = 0
            #stop
            print("stop")
        if self.SDK_json_on == 1 and self.json_btn_l1_value == 1:
            self.json_ps2_button_on = 2
            print("self.json_btn_l1_value",self.json_btn_l1_value)
    def Json_BtnLeftUp(self,data):
        self.json_btn_left_up_value = float(data)
        if self.SDK_json_on == 1 and self.json_btn_left_up_value == 0 and self.json_ps2_button_on == 3:
            self.json_ps2_button_on = 0
            #stop
            print("stop")
        if self.SDK_json_on == 1 and self.json_btn_left_up_value == 1:
            self.json_ps2_button_on = 3
            print("self.json_btn_left_up_value",self.json_btn_left_up_value) 
    def Json_BtnLeftLeft(self,data):
        self.json_btn_left_left_value = float(data)
        if self.SDK_json_on == 1 and self.json_btn_left_left_value == 0 and self.json_ps2_button_on == 4:
            self.json_ps2_button_on = 0
            #stop
            print("stop")
        if self.SDK_json_on == 1 and self.json_btn_left_left_value == 1:
            self.json_ps2_button_on = 4
            print("self.json_btn_left_left_value",self.json_btn_left_left_value)
    def Json_BtnLeftRight(self,data):
        self.json_btn_left_right_value = float(data)
        if self.SDK_json_on == 1 and self.json_btn_left_right_value == 0 and self.json_ps2_button_on == 5:
            self.json_ps2_button_on = 0
            #stop
            print("stop")
        if self.SDK_json_on == 1 and self.json_btn_left_right_value == 1:
            self.json_ps2_button_on = 5
            print("self.json_btn_left_right_value",self.json_btn_left_right_value)
    def Json_BtnLeftDown(self,data):
        self.json_btn_left_down_value = float(data)
        if self.SDK_json_on == 1 and self.json_btn_left_down_value == 0 and self.json_ps2_button_on == 6:
            self.json_ps2_button_on = 0
            #stop
            print("stop")
        if self.SDK_json_on == 1 and self.json_btn_left_down_value == 1:
            self.json_ps2_button_on = 6
            print("self.json_btn_left_down_value",self.json_btn_left_down_value)
    def Json_BtnR2(self,data):
        self.json_btn_r2_value = float(data)
        if self.SDK_json_on == 1 and self.json_btn_r2_value == 0 and self.json_ps2_button_on == 7:
            self.json_ps2_button_on = 0
            #stop
            print("stop")
        if self.SDK_json_on == 1 and self.json_btn_r2_value == 1:
            self.json_ps2_button_on = 7
            print("self.json_btn_r2_value",self.json_btn_r2_value)
    def Json_BtnR1(self,data):
        self.json_btn_r1_value = float(data)
        if self.SDK_json_on == 1 and self.json_btn_r1_value == 0 and self.json_ps2_button_on == 8:
            self.json_ps2_button_on = 0
            #stop
            print("stop")
        if self.SDK_json_on == 1 and self.json_btn_r1_value == 1:
            self.json_ps2_button_on = 8
            print("self.json_btn_r1_value",self.json_btn_r1_value)
    def Json_BtnRightUp(self,data):
        self.json_btn_right_up_value = float(data)
        if self.SDK_json_on == 1 and self.json_btn_right_up_value == 0 and self.json_ps2_button_on == 9:
            self.json_ps2_button_on = 0
            #stop
            print("stop")
        if self.SDK_json_on == 1 and self.json_btn_right_up_value == 1:
            self.json_ps2_button_on = 9
            print("self.json_btn_right_up_value",self.json_btn_right_up_value)
    def Json_BtnRightLeft(self,data):
        self.json_btn_right_left_value = float(data)
        if self.SDK_json_on == 1 and self.json_btn_right_left_value == 0 and self.json_ps2_button_on == 10:
            self.json_ps2_button_on = 0
            #stop
            print("stop")
        if self.SDK_json_on == 1 and self.json_btn_right_left_value == 1:
            self.json_ps2_button_on = 10
            print("self.json_btn_right_left_value",self.json_btn_right_left_value)
        '''
        if data == "1":
            self.SDK_json_on = 0
        '''
    def Json_BtnRightRight(self,data):
        self.json_btn_right_right_value = float(data)
        if self.SDK_json_on == 1 and self.json_btn_right_right_value == 0 and self.json_ps2_button_on == 11:
            self.json_ps2_button_on = 0
            #stop
            print("stop")
        if self.SDK_json_on == 1 and self.json_btn_right_right_value == 1:
            self.json_ps2_button_on = 11
            print("self.json_btn_right_right_value",self.json_btn_right_right_value)
    def Json_BtnRightDown(self,data):
        self.json_btn_right_down_value = float(data)
        if self.SDK_json_on == 1 and self.json_btn_right_down_value == 0 and self.json_ps2_button_on == 12:
            self.json_ps2_button_on = 0
            #stop
            print("stop")
        if self.SDK_json_on == 1 and self.json_btn_right_down_value == 1:
            self.json_ps2_button_on = 12
            print("self.json_btn_right_down_value",self.json_btn_right_down_value)
    def Json_BtnLeftstickUpDown(self,data):
        self.json_btn_leftstick_updown_value = float(data)
        if self.SDK_json_on == 1 and self.json_btn_leftstick_updown_value < 0.1 and self.json_btn_leftstick_updown_value > -0.1 and self.json_ps2_button_on == 13:
            self.json_ps2_button_on = 0
            #stop
            print("stop")
        if self.SDK_json_on == 1 and self.json_btn_leftstick_updown_value > 0.1:
            self.json_ps2_button_on = 13
            print("self.json_btn_leftstick_updown_value",self.json_btn_leftstick_updown_value)
        if self.SDK_json_on == 1 and self.json_btn_leftstick_updown_value < -0.1:
            self.json_ps2_button_on = 13
            print("self.json_btn_leftstick_updown_value",self.json_btn_leftstick_updown_value)
    def Json_BtnLeftstickLeftRight(self,data):
        self.json_btn_leftstick_leftright_value = float(data)
        if self.SDK_json_on == 1 and self.json_btn_leftstick_leftright_value < 0.1 and self.json_btn_leftstick_leftright_value > -0.1 and self.json_ps2_button_on == 14:
            self.json_ps2_button_on = 0
            #stop
            print("stop")
        if self.SDK_json_on == 1 and self.json_btn_leftstick_leftright_value > 0.1:
            self.json_ps2_button_on = 14
            print("self.json_btn_leftstick_leftright_value",self.json_btn_leftstick_leftright_value)
        if self.SDK_json_on == 1 and self.json_btn_leftstick_leftright_value < -0.1:
            self.json_ps2_button_on = 14
            print("self.json_btn_leftstick_leftright_value",self.json_btn_leftstick_leftright_value)
    def Json_BtnRightstickUpDown(self,data):
        self.json_btn_rightstick_updown_value = float(data)
        if self.SDK_json_on == 1 and self.json_btn_rightstick_updown_value < 0.1 and self.json_btn_rightstick_updown_value > -0.1 and self.json_ps2_button_on == 15:
            self.json_ps2_button_on = 0
            #stop
            print("stop")
        if self.SDK_json_on == 1 and self.json_btn_rightstick_updown_value > 0.1:
            self.json_ps2_button_on = 15
            print("self.json_btn_rightstick_updown_value",self.json_btn_rightstick_updown_value)
        if self.SDK_json_on == 1 and self.json_btn_rightstick_updown_value < -0.1:
            self.json_ps2_button_on = 15
            print("self.json_btn_rightstick_updown_value",self.json_btn_rightstick_updown_value)
    def Json_BtnRightstickLeftRight(self,data):
        self.json_btn_rightstick_leftright_value = float(data)
        if self.SDK_json_on == 1 and self.json_btn_rightstick_leftright_value < 0.1 and self.json_btn_rightstick_leftright_value > -0.1 and self.json_ps2_button_on == 16:
            self.json_ps2_button_on = 0
            #stop
            print("stop")
        if self.SDK_json_on == 1 and self.json_btn_rightstick_leftright_value > 0.1:
            self.json_ps2_button_on = 16
            print("self.json_btn_rightstick_leftright_value",self.json_btn_rightstick_leftright_value)
        if self.SDK_json_on == 1 and self.json_btn_rightstick_leftright_value < -0.1:
            self.json_ps2_button_on = 16
            print("self.json_btn_rightstick_leftright_value",self.json_btn_rightstick_leftright_value)
    #endregion

    #region SDK各按钮对应的SDK函数(API)
    def SDK_buttonClicked(self):
        sender = self.sender()
        '''
        if sender.text() == "8056on":
            self.value_8056 = 1
            print("self.value_8056=",self.value_8056)
        if sender.text() == "8056ff":
            self.value_8056 = 0
            print("self.value_8056=",self.value_8056)
        '''
        if sender.text() == "CreateCtx":
            self.elt_ctx_self = Elite_dll.elt_create_ctx(robot_IP, robot_SDK_port)
            print("elt_ctx_self=",self.elt_ctx_self)
            self.btn_createctx.setStyleSheet('''QPushButton{background-color:rgb(0,255,0);border-radius:5px;}QPushButton:hover{background-color:rgb(255,255,0);}''')
            self.btn_destroyctx.setStyleSheet('''QPushButton{background-color:rgb(255,0,255);border-radius:5px;}QPushButton:hover{background-color:rgb(255,255,0);}''')
            #self.statusBar().showMessage(sender.text() + ' was pressed')
        if sender.text() == "Login":
            self.SDK_on = 1
            self.ret_login = Elite_dll.elt_login(c_void_p(self.elt_ctx_self))
            self.btn_login.setStyleSheet('''QPushButton{background-color:rgb(0,255,0);border-radius:5px;}QPushButton:hover{background-color:rgb(255,255,0);}''')
            self.btn_logout.setStyleSheet('''QPushButton{background-color:rgb(255,0,255);border-radius:5px;}QPushButton:hover{background-color:rgb(255,255,0);}''')
            print("login=",self.ret_login)
        if sender.text() == "Logout":
            self.ret_login = 0
            self.SDK_on = 0
            ret = ret = Elite_dll.elt_logout(c_void_p(self.elt_ctx_self))
            self.btn_logout.setStyleSheet('''QPushButton{background-color:rgb(0,255,0);border-radius:5px;}QPushButton:hover{background-color:rgb(255,255,0);}''')
            self.btn_login.setStyleSheet('''QPushButton{background-color:rgb(255,0,255);border-radius:5px;}QPushButton:hover{background-color:rgb(255,255,0);}''')
            print("logout=",ret)
        if sender.text() == "DestroyCtx":
            ret = Elite_dll.elt_destroy_ctx(c_void_p(self.elt_ctx_self))
            self.btn_destroyctx.setStyleSheet('''QPushButton{background-color:rgb(0,255,0);border-radius:5px;}QPushButton:hover{background-color:rgb(255,255,0);}''')
            self.btn_createctx.setStyleSheet('''QPushButton{background-color:rgb(255,0,255);border-radius:5px;}QPushButton:hover{background-color:rgb(255,255,0);}''')
            self.elt_ctx_self = c_void_p(-1)
            print("destroyctx=",ret)
        if sender.text() == "Syn":
            ret = Elite_dll.elt_sync_on(c_void_p(self.elt_ctx_self), byref(error_message))
            #print("synchronize=",ret)
            print("同步=",ret)
        if sender.text() == "UnSyn":
            ret = Elite_dll.elt_sync_off(c_void_p(self.elt_ctx_self), byref(error_message))
            print("unsynchronize=",ret)
        if sender.text() == "ClearAlarm":
            #force = 0普通清楚报警
            force = 0
            ret = Elite_dll.elt_clear_alarm(c_void_p(self.elt_ctx_self), force, byref(error_message))
            #print("ClearAlarm=",ret)
            print("清报警=", ret)
        if sender.text() == "ServoEnable":
            state = c_long(0)
            status = c_long(0)
            v_status = 0
            ret = Elite_dll.elt_get_robot_state(c_void_p(self.elt_ctx_self), byref(state), byref(error_message))
            if state.value !=4:
                ret = Elite_dll.elt_get_servo_status(c_void_p(self.elt_ctx_self), byref(status), byref(error_message))
                if status.value == 0:
                    state = 1
                    ret_enable = Elite_dll.elt_set_servo_status(c_void_p(self.elt_ctx_self), state, byref(error_message))
                    self.btn_servoenable.setStyleSheet('''QPushButton{background-color:rgb(0,255,0);border-radius:5px;}QPushButton:hover{background-color:rgb(255,255,0);}''')
                    print("ServoState=",state)
                    print("ServoEnable =",ret_enable)
                if status.value == 1:
                    state = 0
                    self.btn_servoenable.setStyleSheet('''QPushButton{background-color:rgb(255,0,255);border-radius:5px;}QPushButton:hover{background-color:rgb(255,255,0);}''')
                    ret_disenable = Elite_dll.elt_set_servo_status(c_void_p(self.elt_ctx_self), state, byref(error_message))
                    print("ServoState=",state)
                    print("ServoDisenable =",ret_disenable)

        if sender.text() == "Run":
            state = c_long(0)
            ret = Elite_dll.elt_get_robot_state(c_void_p(self.elt_ctx_self), byref(state), byref(error_message))
            if state.value !=4:
                ret = Elite_dll.elt_run(c_void_p(self.elt_ctx_self), byref(error_message))
            print("Run =",ret)
        if sender.text() == "Pause":
            state = c_long(0)
            ret = Elite_dll.elt_get_robot_state(c_void_p(self.elt_ctx_self), byref(state), byref(error_message))
            if state.value !=4:
                ret = Elite_dll.elt_pause(c_void_p(self.elt_ctx_self), byref(error_message))
            print("Pause =",ret)
        if sender.text() == "Var_M":
            #self.Var_M_num.Text()的Text不能大写text
            #Address_M = c_int(int(self.Var_M_num.Text())) 错误
            Address_M = c_int(int(self.Var_M_num.text()))
            status = c_long(0)
            v_status = 0
            ret = Elite_dll.elt_get_virtual_output(c_void_p(self.elt_ctx_self), Address_M.value, byref(status), byref(error_message))
            print("Address_M=", status)
            if status.value == 0:
                v_status = 1
                ret = Elite_dll.elt_set_virtual_output(c_void_p(self.elt_ctx_self), Address_M.value, v_status, byref(error_message))
            if status.value  == 1:
                v_status = 0
                ret = Elite_dll.elt_set_virtual_output(c_void_p(self.elt_ctx_self), Address_M.value, v_status, byref(error_message))
                print("ret=",ret)
        if sender.text() == "Waypoint":
            speed = c_double(50)
            ret = Elite_dll.elt_set_waypoint_max_joint_speed(c_void_p(self.elt_ctx_self), speed, byref(error_message))
            ret = Elite_dll.elt_clear_waypoint(c_void_p(self.elt_ctx_self), byref(error_message))
            print("clear alarm =",ret)

            waypoint_array1 = (c_double*8)(0, -90 ,0 ,-90 ,90 ,0, 0 , 0)
            waypoint_array2 = (c_double*8)(0, -90 ,90 ,-90 ,90 ,0, 0 , 0)
            waypoint_array3 = (c_double*8)(0, -90 ,-90 ,-90 ,90 ,0, 0 , 0)
            waypoint_array4 = (c_double*8)(0, -90 ,0 ,-90 , 90, 90, 0 , 0)
            
            ret = Elite_dll.elt_add_waypoint(c_void_p(self.elt_ctx_self), waypoint_array1, byref(error_message))
            ret = Elite_dll.elt_add_waypoint(c_void_p(self.elt_ctx_self), waypoint_array2, byref(error_message))
            ret = Elite_dll.elt_add_waypoint(c_void_p(self.elt_ctx_self), waypoint_array3, byref(error_message))
            ret = Elite_dll.elt_add_waypoint(c_void_p(self.elt_ctx_self), waypoint_array4, byref(error_message))
            print("success to add waypoint =",ret)
            move_type = c_long(0)
            move_type.value = 0
            pl = c_long(0)
            pl.value = 7
            ret = Elite_dll.elt_track_move(c_void_p(self.elt_ctx_self), move_type, pl, byref(error_message))
            print("elt_track_move =",ret)
        if sender.text() == "Stop":
            state = c_long(0)
            ret = Elite_dll.elt_get_robot_state(c_void_p(self.elt_ctx_self), byref(state), byref(error_message))
            if state.value !=4:
                ret = Elite_dll.elt_stop(c_void_p(self.elt_ctx_self), byref(error_message))
            print("Stop =",ret)
        if sender.text() == "J1-" or sender.text() == "J1+":
            state = c_long(0)
            ret = Elite_dll.elt_get_robot_state(c_void_p(self.elt_ctx_self), byref(state), byref(error_message))
            if state.value !=4:
                ret = Elite_dll.elt_stop(c_void_p(self.elt_ctx_self), byref(error_message))
        if sender.text() == "J2-" or sender.text() == "J2+":
            state = c_long(0)
            ret = Elite_dll.elt_get_robot_state(c_void_p(self.elt_ctx_self), byref(state), byref(error_message))
            if state.value !=4:
                ret = Elite_dll.elt_stop(c_void_p(self.elt_ctx_self), byref(error_message))
        if sender.text() == "J3-" or sender.text() == "J3+":
            state = c_long(0)
            ret = Elite_dll.elt_get_robot_state(c_void_p(self.elt_ctx_self), byref(state), byref(error_message))
            if state.value !=4:
                ret = Elite_dll.elt_stop(c_void_p(self.elt_ctx_self), byref(error_message))
        if sender.text() == "J4-" or sender.text() == "J4+":
            state = c_long(0)
            ret = Elite_dll.elt_get_robot_state(c_void_p(self.elt_ctx_self), byref(state), byref(error_message))
            if state.value !=4:
                ret = Elite_dll.elt_stop(c_void_p(self.elt_ctx_self), byref(error_message))
        if sender.text() == "J5-" or sender.text() == "J5+":
            state = c_long(0)
            ret = Elite_dll.elt_get_robot_state(c_void_p(self.elt_ctx_self), byref(state), byref(error_message))
            if state.value !=4:
                ret = Elite_dll.elt_stop(c_void_p(self.elt_ctx_self), byref(error_message))
        if sender.text() == "J6-" or sender.text() == "J6+":
            state = c_long(0)
            ret = Elite_dll.elt_get_robot_state(c_void_p(self.elt_ctx_self), byref(state), byref(error_message))
            if state.value !=4:
                ret = Elite_dll.elt_stop(c_void_p(self.elt_ctx_self), byref(error_message))
        if sender.text() == "X-" or sender.text() == "X+":
            state = c_long(0)
            ret = Elite_dll.elt_get_robot_state(c_void_p(self.elt_ctx_self), byref(state), byref(error_message))
            if state.value !=4:
                ret = Elite_dll.elt_stop(c_void_p(self.elt_ctx_self), byref(error_message))
        if sender.text() == "Y-" or sender.text() == "Y+":
            state = c_long(0)
            ret = Elite_dll.elt_get_robot_state(c_void_p(self.elt_ctx_self), byref(state), byref(error_message))
            if state.value !=4:
                ret = Elite_dll.elt_stop(c_void_p(self.elt_ctx_self), byref(error_message))
        if sender.text() == "Z-" or sender.text() == "Z+":
            state = c_long(0)
            ret = Elite_dll.elt_get_robot_state(c_void_p(self.elt_ctx_self), byref(state), byref(error_message))
            if state.value !=4:
                ret = Elite_dll.elt_stop(c_void_p(self.elt_ctx_self), byref(error_message))
        if sender.text() == "Rx-" or sender.text() == "Rx+":
            state = c_long(0)
            ret = Elite_dll.elt_get_robot_state(c_void_p(self.elt_ctx_self), byref(state), byref(error_message))
            if state.value !=4:
                ret = Elite_dll.elt_stop(c_void_p(self.elt_ctx_self), byref(error_message))
        if sender.text() == "Ry-" or sender.text() == "Ry+":
            state = c_long(0)
            ret = Elite_dll.elt_get_robot_state(c_void_p(self.elt_ctx_self), byref(state), byref(error_message))
            if state.value !=4:
                ret = Elite_dll.elt_stop(c_void_p(self.elt_ctx_self), byref(error_message))
        if sender.text() == "Rz-" or sender.text() == "Rz+":
            state = c_long(0)
            ret = Elite_dll.elt_get_robot_state(c_void_p(self.elt_ctx_self), byref(state), byref(error_message))
            if state.value !=4:
                ret = Elite_dll.elt_stop(c_void_p(self.elt_ctx_self), byref(error_message))
        if sender.text() == "Output_Y":
            '''
            Address_Y = c_int(int(self.Output_Y.text()))
            print("type_Address_Y",type(Address_Y))
            print("type_Output_Y.Text()=",type(self.Output_Y.text()))
            print("type_Output_Y.Text().toNumber()=",type(int(self.Output_Y.text())))
            print("value_Y",Address_Y.value)
            '''
            Address_Y = c_int(int(self.Output_Y.text()))
            #print("===",self.Output_Y.text())
            value_Y002 = c_long(0)
            ret = Elite_dll.elt_get_output(c_void_p(self.elt_ctx_self), Address_Y.value, byref(value_Y002), byref(error_message))
            print("value_Y002 =", value_Y002)
            if value_Y002.value == 0:
                v_Y002 = 1
                ret = Elite_dll.elt_set_output(c_void_p(self.elt_ctx_self), Address_Y.value, v_Y002, byref(error_message))
            if value_Y002.value == 1:
                v_Y002 = 0
                ret = Elite_dll.elt_set_output(c_void_p(self.elt_ctx_self), Address_Y.value, v_Y002, byref(error_message))
    #endregion

    #region json协议各按钮对应的method(接口方法)
    def json_buttonClicked(self):
        sender = self.sender()
        if sender.text() == "CreateSocket" and self.SDK_json_on == -1 or self.SDK_json_on == 0:
            Robot_IP = "192.168.1.200"
            TCP_Port = 8055
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #print("self.sock=",self.sock.family)
            #print("self.sock=",self.sock)
            try:
                self.sock.connect((Robot_IP,TCP_Port))
                #return (True,self.sock)
            except Exception as e:
                self.sock.close()
                #return (False,)
            self.btn_createsocket.setStyleSheet('''QPushButton{background-color:rgb(0,255,0);border-radius:5px;}QPushButton:hover{background-color:rgb(255,255,0);}''')
            self.btn_closesocket.setStyleSheet('''QPushButton{background-color:rgb(255,0,255);border-radius:5px;}QPushButton:hover{background-color:rgb(255,255,0);}''')
            #self.statusBar().showMessage(sender.text() + ' was pressed')
            self.SDK_json_on = 1
            print("self.SDK_json_on=",self.SDK_json_on)
        if sender.text() == "CloseSocket" and self.SDK_json_on == 1:
            if(self.sock):
                self.sock.close()
                self.sock=None
            else:
                self.sock=None
            self.btn_closesocket.setStyleSheet('''QPushButton{background-color:rgb(0,255,0);border-radius:5px;}QPushButton:hover{background-color:rgb(255,255,0);}''')
            self.btn_createsocket.setStyleSheet('''QPushButton{background-color:rgb(255,0,255);border-radius:5px;}QPushButton:hover{background-color:rgb(255,255,0);}''')
            self.SDK_json_on = 0
            print("self.SDK_json_on=",self.SDK_json_on)
        if sender.text() == "RunJBI" and self.SDK_json_on == 1:
            method = "checkJbiExist"
            params = json.dumps({"filename":"ab.jbi"})
            id = 1
            sendStr="{{\"method\":\"{0}\",\"params\":{1},\"jsonrpc\":\"2.0\",\"id\":{2}}}".format(method,params,id)+"\n"
            try:
                #print(sendStr)
                self.sock.sendall(bytes(sendStr,"utf-8"))
                ret = self.sock.recv(1024)
                jdata = json.loads(str(ret,"utf-8"))
                if("result" in jdata.keys()):
                    method = "runJbi"
                    params = json.dumps({"filename":"ab.jbi"})
                    id = 2
                    sendStr="{{\"method\":\"{0}\",\"params\":{1},\"jsonrpc\":\"2.0\",\"id\":{2}}}".format(method,params,id)+"\n"
                    try:
                        #print(sendStr)
                        self.sock.sendall(bytes(sendStr,"utf-8"))
                        ret = self.sock.recv(1024)
                        jdata = json.loads(str(ret,"utf-8"))
                        if("result" in jdata.keys()):
                            checkRunning=3
                            while(checkRunning==3):                                             #wait for the jbi program is over
                                #suc,result,id=sendCMD(sock,"getJbiState")
                                method = "getJbiState"
                                #不可以params = None
                                params = []
                                id = 3
                                sendStr="{{\"method\":\"{0}\",\"params\":{1},\"jsonrpc\":\"2.0\",\"id\":{2}}}".format(method,params,id)+"\n"
                                self.sock.sendall(bytes(sendStr,"utf-8"))
                                ret = self.sock.recv(1024)
                                jdata = json.loads(str(ret,"utf-8"))
                                checkRunning = json.loads(jdata["runState"])
                                time.sleep(0.5)
                            #return (True,json.loads(jdata["result"]),jdata["id"])
                        elif("error" in jdata.keys()):
                            print("{0},{1},{2}",format(False,json.loads(jdata["error"]),jdata["id"]))
                            #return (False,json.loads(jdata["error"]),jdata["id"])
                        else:
                            print("False,None,None")
                            #return (False,None,None)
                    except Exception as e:
                        print("False,None,None")
                        #return (False,None,None)
                    #return (True,json.loads(jdata["result"]),jdata["id"])
                elif("error" in jdata.keys()):
                    print("{0},{1},{2}",format(False,json.loads(jdata["error"]),jdata["id"]))
                    #return (False,json.loads(jdata["error"]),jdata["id"])
                else:
                    print("False,None,None")
                    #return (False,None,None)
            except Exception as e:
                print("False,None,None")
                #return (False,None,None)

        if sender.text() == "ToolLoad" and self.SDK_json_on == 1:
            method = "cmd_set_payload"
            params = json.dumps({"point":[0,0,0],"tool_num":1,"m":0})
            id = 4
            sendStr="{{\"method\":\"{0}\",\"params\":{1},\"jsonrpc\":\"2.0\",\"id\":{2}}}".format(method,params,id)+"\n"
            self.sock.sendall(bytes(sendStr,"utf-8"))
            ret = self.sock.recv(1024)
            jdata = json.loads(str(ret,"utf-8"))
        if sender.text() == "路点2.0绕工具" and self.SDK_json_on == 1:
            #读取的关节角度
            method = "getRobotPose"
            params = []
            id = 8
            sendStr="{{\"method\":\"{0}\",\"params\":{1},\"jsonrpc\":\"2.0\",\"id\":{2}}}".format(method,params,id)+"\n"
            self.sock.sendall(bytes(sendStr,"utf-8"))
            ret = self.sock.recv(1024)
            jdata = json.loads(str(ret,"utf-8"))
            currentpose = json.loads(jdata["result"])
            
            #把当前的位姿逆解为关节
            method = "inverseKinematic"
            params = json.dumps({"targetPose":currentpose})
            id = 7
            sendStr="{{\"method\":\"{0}\",\"params\":{1},\"jsonrpc\":\"2.0\",\"id\":{2}}}".format(method,params,id)+"\n"
            self.sock.sendall(bytes(sendStr,"utf-8"))
            ret = self.sock.recv(1024)
            jdata = json.loads(str(ret,"utf-8"))
            currentpos = json.loads(jdata["result"])

            method = "clearPathPoint"
            params = []
            id = 5
            sendStr="{{\"method\":\"{0}\",\"params\":{1},\"jsonrpc\":\"2.0\",\"id\":{2}}}".format(method,params,id)+"\n"
            self.sock.sendall(bytes(sendStr,"utf-8"))
            ret = self.sock.recv(1024)
            jdata = json.loads(str(ret,"utf-8"))
            if("result" in jdata.keys()):
                n = 0
                while n < 2:
                    print("-------------")
                    Angle = 15
                    num = 20
                    for k in range(1,num+1):
                        #列表复制
                        json_waypose_array1 = currentpose[:]
                        json_waypose_array1[3] = json_waypose_array1[3] + (Angle * math.pi / 180) - (k-1)*(Angle * math.pi / 180)/(num-1)
                        json_waypose_array1[4] = json_waypose_array1[4] - (k-1)*(Angle * math.pi / 180)/(num-1)

                        method = "inverseKinematic"
                        params = json.dumps({"targetPose":json_waypose_array1})
                        id = 7
                        sendStr="{{\"method\":\"{0}\",\"params\":{1},\"jsonrpc\":\"2.0\",\"id\":{2}}}".format(method,params,id)+"\n"
                        self.sock.sendall(bytes(sendStr,"utf-8"))
                        ret = self.sock.recv(1024)
                        jdata = json.loads(str(ret,"utf-8"))
                        json_waypoint_array1 = json.loads(jdata["result"])

                        method = "addPathPoint"
                        id = 6
                        speed = 100
                        if (k == 1):
                            speed = 10
                        params = json.dumps({"wayPoint":json_waypoint_array1,"moveType":2,"speed":speed,"smooth":7})
                        sendStr="{{\"method\":\"{0}\",\"params\":{1},\"jsonrpc\":\"2.0\",\"id\":{2}}}".format(method,params,id)+"\n"
                        self.sock.sendall(bytes(sendStr,"utf-8"))
                        ret = self.sock.recv(1024)
                    
                    for k in range(1,num+1):
                        json_waypose_array2 = currentpose[:]
                        json_waypose_array2[3] = json_waypose_array2[3] - (k-1)*(Angle * math.pi / 180)/(num-1)
                        json_waypose_array2[4] = json_waypose_array2[4] - (Angle * math.pi / 180) + (k-1)*(Angle * math.pi / 180)/(num-1)
                        
                        method = "inverseKinematic"
                        params = json.dumps({"targetPose":json_waypose_array2})
                        id = 7
                        sendStr="{{\"method\":\"{0}\",\"params\":{1},\"jsonrpc\":\"2.0\",\"id\":{2}}}".format(method,params,id)+"\n"
                        self.sock.sendall(bytes(sendStr,"utf-8"))
                        ret = self.sock.recv(1024)
                        jdata = json.loads(str(ret,"utf-8"))
                        json_waypoint_array2 = json.loads(jdata["result"])

                        method = "addPathPoint"
                        id = 6
                        params = json.dumps({"wayPoint":json_waypoint_array2,"moveType":2,"speed":100,"smooth":7})
                        sendStr="{{\"method\":\"{0}\",\"params\":{1},\"jsonrpc\":\"2.0\",\"id\":{2}}}".format(method,params,id)+"\n"
                        self.sock.sendall(bytes(sendStr,"utf-8"))
                        ret = self.sock.recv(1024)
                    
                    for k in range(1,num+1):
                        json_waypose_array3 = currentpose[:]
                        json_waypose_array3[3] = json_waypose_array3[3] - (Angle * math.pi / 180) + (k-1)*(Angle * math.pi / 180)/(num-1)
                        json_waypose_array3[4] = json_waypose_array3[4] + (k-1)*(Angle * math.pi / 180)/(num-1)
                        
                        method = "inverseKinematic"
                        params = json.dumps({"targetPose":json_waypose_array3})
                        id = 7
                        sendStr="{{\"method\":\"{0}\",\"params\":{1},\"jsonrpc\":\"2.0\",\"id\":{2}}}".format(method,params,id)+"\n"
                        self.sock.sendall(bytes(sendStr,"utf-8"))
                        ret = self.sock.recv(1024)
                        jdata = json.loads(str(ret,"utf-8"))
                        json_waypoint_array3 = json.loads(jdata["result"])

                        method = "addPathPoint"
                        id = 6
                        params = json.dumps({"wayPoint":json_waypoint_array3,"moveType":2,"speed":100,"smooth":7})
                        sendStr="{{\"method\":\"{0}\",\"params\":{1},\"jsonrpc\":\"2.0\",\"id\":{2}}}".format(method,params,id)+"\n"
                        self.sock.sendall(bytes(sendStr,"utf-8"))
                        ret = self.sock.recv(1024)
                    for k in range(1,num+1):
                        json_waypose_array4 = currentpose[:]
                        json_waypose_array4[3] = json_waypose_array4[3] + (k-1)*(Angle * math.pi / 180)/(num-1)
                        json_waypose_array4[4] = json_waypose_array4[4] + (Angle * math.pi / 180) - (k-1)*(Angle * math.pi / 180)/(num-1)
                        
                        method = "inverseKinematic"
                        params = json.dumps({"targetPose":json_waypose_array4})
                        id = 7
                        sendStr="{{\"method\":\"{0}\",\"params\":{1},\"jsonrpc\":\"2.0\",\"id\":{2}}}".format(method,params,id)+"\n"
                        self.sock.sendall(bytes(sendStr,"utf-8"))
                        ret = self.sock.recv(1024)
                        jdata = json.loads(str(ret,"utf-8"))
                        json_waypoint_array4 = json.loads(jdata["result"])

                        method = "addPathPoint"
                        id = 6
                        params = json.dumps({"wayPoint":json_waypoint_array4,"moveType":2,"speed":100,"smooth":7})
                        sendStr="{{\"method\":\"{0}\",\"params\":{1},\"jsonrpc\":\"2.0\",\"id\":{2}}}".format(method,params,id)+"\n"
                        self.sock.sendall(bytes(sendStr,"utf-8"))
                        ret = self.sock.recv(1024)
                    n = n + 1
                    
                method = "addPathPoint"
                id = 6
                params = json.dumps({"wayPoint":currentpos,"moveType":0,"speed":100,"smooth":7})
                sendStr="{{\"method\":\"{0}\",\"params\":{1},\"jsonrpc\":\"2.0\",\"id\":{2}}}".format(method,params,id)+"\n"
                self.sock.sendall(bytes(sendStr,"utf-8"))
                ret = self.sock.recv(1024)
                jdata = json.loads(str(ret,"utf-8"))

                if("result" in jdata.keys()):
                    method = "moveByPath"
                    params = []
                    id = 7
                    sendStr="{{\"method\":\"{0}\",\"params\":{1},\"jsonrpc\":\"2.0\",\"id\":{2}}}".format(method,params,id)+"\n"
                    self.sock.sendall(bytes(sendStr,"utf-8"))
                    ret = self.sock.recv(1024)
                    jdata = json.loads(str(ret,"utf-8"))
                    if("result" in jdata.keys()):
                        method = "getRobotState"
                        params = []
                        id = 8
                        time.sleep(0.5)
                        sendStr="{{\"method\":\"{0}\",\"params\":{1},\"jsonrpc\":\"2.0\",\"id\":{2}}}".format(method,params,id)+"\n"
                        self.sock.sendall(bytes(sendStr,"utf-8"))
                        ret = self.sock.recv(1024)
                        jdata = json.loads(str(ret,"utf-8"))
                        robotrunningstate = 3
                        #wait for the pathmove is over
                        while(robotrunningstate == 3):
                            #suc,result,id=sendCMD(sock,"getJbiState")
                            method = "getRobotState"
                            #不可以params = None
                            params = []
                            id = 8
                            sendStr="{{\"method\":\"{0}\",\"params\":{1},\"jsonrpc\":\"2.0\",\"id\":{2}}}".format(method,params,id)+"\n"
                            self.sock.sendall(bytes(sendStr,"utf-8"))
                            ret = self.sock.recv(1024)
                            jdata = json.loads(str(ret,"utf-8"))
                            robotrunningstate = json.loads(jdata["result"])
                            time.sleep(0.1)
            #region 以下是人为输入4个点,
            '''
            method = "clearPathPoint"
            params = []
            id = 5
            sendStr="{{\"method\":\"{0}\",\"params\":{1},\"jsonrpc\":\"2.0\",\"id\":{2}}}".format(method,params,id)+"\n"
            self.sock.sendall(bytes(sendStr,"utf-8"))
            ret = self.sock.recv(1024)
            jdata = json.loads(str(ret,"utf-8"))
            if("result" in jdata.keys()):
                method = "addPathPoint"

                id = 6
                #以下4个点，每个点角度偏差45度
                #json_waypoint_array0 = (c_double*8)(0, -90 ,90 ,-90 ,90 , 0, 0 , 0)
                #json_waypoint_array1 = (c_double*8)(0, -90.930, 112.336, -156.385, 90, 0, 0, 0)
                #json_waypoint_array2 = (c_double*8)(7.121, -86.584, 95.731, -92.086, 45.463, 10.015, 0, 0)
                #json_waypoint_array3 = (c_double*8)(0, -77.342, 76.856, -44.537, 90, 0, 0, 0)
                #json_waypoint_array4 = (c_double*8)(-7.343, -90.784, 99.979, -91.919, 134.510, -10.324, 0, 0)

                #json_waypoint_array1 = [0, -90.930, 112.336, -156.385, 90, 0, 0, 0]
                #json_waypoint_array2 = [7.121, -86.584, 95.731, -92.086, 45.463, 10.015, 0, 0]
                #json_waypoint_array3 = [0, -77.342, 76.856, -44.537, 90, 0, 0, 0]
                #json_waypoint_array4 = [-7.343, -90.784, 99.979, -91.919, 134.510, -10.324, 0, 0]

                json_waypoint_array1 = [0, -97.332, 95.331, -105.990, 90, 0, 0, 0]
                json_waypoint_array2 = [6.619, -87.245, 80.768, -81.379, 72.133, 6.956, 0, 0]
                json_waypoint_array3 = [0, -80.263, 69.103, -60.849, 90, 0, 0, 0]
                json_waypoint_array4 = [-6.811, -91.161, 84.726, -81.360, 107.860, -7.157, 0, 0]

                params = json.dumps({"wayPoint":[0, -90 ,90 ,-90 ,90 , 0, 0 , 0],"moveType":0,"speed":100,"smooth":7})
                sendStr="{{\"method\":\"{0}\",\"params\":{1},\"jsonrpc\":\"2.0\",\"id\":{2}}}".format(method,params,id)+"\n"
                self.sock.sendall(bytes(sendStr,"utf-8"))
                ret = self.sock.recv(1024)
                n = 0
                while n <= 10:
                    params = json.dumps({"wayPoint":json_waypoint_array1,"moveType":2,"speed":100,"smooth":7})
                    sendStr="{{\"method\":\"{0}\",\"params\":{1},\"jsonrpc\":\"2.0\",\"id\":{2}}}".format(method,params,id)+"\n"
                    self.sock.sendall(bytes(sendStr,"utf-8"))
                    ret = self.sock.recv(1024)
                    params = json.dumps({"wayPoint":json_waypoint_array2,"moveType":2,"speed":100,"smooth":7})
                    sendStr="{{\"method\":\"{0}\",\"params\":{1},\"jsonrpc\":\"2.0\",\"id\":{2}}}".format(method,params,id)+"\n"
                    self.sock.sendall(bytes(sendStr,"utf-8"))
                    ret = self.sock.recv(1024)
                    params = json.dumps({"wayPoint":json_waypoint_array3,"moveType":2,"speed":100,"smooth":7})
                    sendStr="{{\"method\":\"{0}\",\"params\":{1},\"jsonrpc\":\"2.0\",\"id\":{2}}}".format(method,params,id)+"\n"
                    self.sock.sendall(bytes(sendStr,"utf-8"))
                    ret = self.sock.recv(1024)
                    params = json.dumps({"wayPoint":json_waypoint_array4,"moveType":2,"speed":100,"smooth":7})
                    sendStr="{{\"method\":\"{0}\",\"params\":{1},\"jsonrpc\":\"2.0\",\"id\":{2}}}".format(method,params,id)+"\n"
                    self.sock.sendall(bytes(sendStr,"utf-8"))
                    ret = self.sock.recv(1024)
                    jdata = json.loads(str(ret,"utf-8"))
                    n = n + 1

                if("result" in jdata.keys()):
                    method = "moveByPath"
                    params = []
                    id = 7
                    sendStr="{{\"method\":\"{0}\",\"params\":{1},\"jsonrpc\":\"2.0\",\"id\":{2}}}".format(method,params,id)+"\n"
                    self.sock.sendall(bytes(sendStr,"utf-8"))
                    ret = self.sock.recv(1024)
                    jdata = json.loads(str(ret,"utf-8"))
                    if("result" in jdata.keys()):
                        method = "getRobotState"
                        params = []
                        id = 8
                        time.sleep(0.5)
                        sendStr="{{\"method\":\"{0}\",\"params\":{1},\"jsonrpc\":\"2.0\",\"id\":{2}}}".format(method,params,id)+"\n"
                        self.sock.sendall(bytes(sendStr,"utf-8"))
                        ret = self.sock.recv(1024)
                        jdata = json.loads(str(ret,"utf-8"))
                        robotrunningstate = 3
                        #wait for the pathmove is over
                        while(robotrunningstate == 3):
                            #suc,result,id=sendCMD(sock,"getJbiState")
                            method = "getRobotState"
                            #不可以params = None
                            params = []
                            id = 8
                            sendStr="{{\"method\":\"{0}\",\"params\":{1},\"jsonrpc\":\"2.0\",\"id\":{2}}}".format(method,params,id)+"\n"
                            self.sock.sendall(bytes(sendStr,"utf-8"))
                            ret = self.sock.recv(1024)
                            jdata = json.loads(str(ret,"utf-8"))
                            robotrunningstate = json.loads(jdata["result"])
                            time.sleep(0.1)
            '''
            #endregion
        if sender.text() == "PS2 透传" and self.SDK_json_on == 1:
            print("PS2 透传")
            # 获取机器人状态
            # suc , result , id = sendCMD(sock , "getRobotState")
            method = "getRobotState"
            params = []
            id = 9
            sendStr="{{\"method\":\"{0}\",\"params\":{1},\"jsonrpc\":\"2.0\",\"id\":{2}}}".format(method,params,id)+"\n"
            self.sock.sendall(bytes(sendStr,"utf-8"))
            ret = self.sock.recv(1024)
            jdata = json.loads(str(ret,"utf-8"))
            self.robot_state = json.loads(jdata["result"])
            if (self.robot_state == 4):
                # 清除报警
                # suc , result , id = sendCMD(sock , "clearAlarm", {"force": 0})
                method = "clearAlarm"
                params = json.dumps({"force": 0})
                id = 10
                sendStr="{{\"method\":\"{0}\",\"params\":{1},\"jsonrpc\":\"2.0\",\"id\":{2}}}".format(method,params,id)+"\n"
                self.sock.sendall(bytes(sendStr,"utf-8"))
                ret = self.sock.recv(1024)
                jdata = json.loads(str(ret,"utf-8"))
                self.ret_clearalarm = json.loads(jdata["result"])
                print("testpass")
                time.sleep(5)
            # 获取同步状态
            suc , result , id = sendCMD(sock , "getMotorStatus")
            if (result == 0):
                # 同步伺服编码器数据
                suc , result , id = sendCMD(sock , "syncMotorStatus")
                time.sleep (0.5)
        if sender.text() == "json_M" and self.SDK_json_on == 1:
            _json_address_M = int(self.json_address_M.text())
            method = "getVirtualOutput"
            params = json.dumps({"addr":_json_address_M})
            id = 9
            sendStr = "{{\"method\":\"{0}\",\"params\":{1},\"jsonrpc\":\"2.0\",\"id\":{2}}}".format(method,params,id)+"\n"
            
            self.sock.sendall(bytes(sendStr,"utf-8"))
            sock_recv = self.sock.recv(1024)
            jdata = json.loads(str(sock_recv,"utf-8"))
            self.json_address_M_value =json.loads(jdata["result"])
            if (self.json_address_M_value == 0):
                method = "setVirtualOutput"
                params = json.dumps({"addr":_json_address_M,"status":1})
                id = 10
                sendStr = "{{\"method\":\"{0}\",\"params\":{1},\"jsonrpc\":\"2.0\",\"id\":{2}}}".format(method,params,id)+"\n"
                self.sock.sendall(bytes(sendStr,"utf-8"))
                sock_recv = self.sock.recv(1024)
            if (self.json_address_M_value == 1):
                method = "setVirtualOutput"
                params = json.dumps({"addr":_json_address_M,"status":0})
                id = 10
                sendStr = "{{\"method\":\"{0}\",\"params\":{1},\"jsonrpc\":\"2.0\",\"id\":{2}}}".format(method,params,id)+"\n"
                self.sock.sendall(bytes(sendStr,"utf-8"))
                sock_recv = self.sock.recv(1024)
        if sender.text() == "json_Y" and self.SDK_json_on == 1:
            _json_address_Y = int(self.json_address_Y.text())
            method = "getOutput"
            params = json.dumps({"addr":_json_address_Y})
            id = 11
            sendStr = "{{\"method\":\"{0}\",\"params\":{1},\"jsonrpc\":\"2.0\",\"id\":{2}}}".format(method,params,id)+"\n"
            self.sock.sendall(bytes(sendStr,"utf-8"))
            sock_recv = self.sock.recv(1024)
            jdata = json.loads(str(sock_recv,"utf-8"))
            self.json_address_Y_value =json.loads(jdata["result"])
            if (self.json_address_Y_value == 0):
                method = "setOutput"
                params = json.dumps({"addr":_json_address_Y,"status":1})
                id = 12
                sendStr = "{{\"method\":\"{0}\",\"params\":{1},\"jsonrpc\":\"2.0\",\"id\":{2}}}".format(method,params,id)+"\n"
                self.sock.sendall(bytes(sendStr,"utf-8"))
                sock_recv = self.sock.recv(1024)
            if (self.json_address_Y_value == 1):
                method = "setOutput"
                params = json.dumps({"addr":_json_address_Y,"status":0})
                id = 12
                sendStr = "{{\"method\":\"{0}\",\"params\":{1},\"jsonrpc\":\"2.0\",\"id\":{2}}}".format(method,params,id)+"\n"
                self.sock.sendall(bytes(sendStr,"utf-8"))
                sock_recv = self.sock.recv(1024)
        if sender.text() == "MOVJ" and self.SDK_json_on == 1:
            target_pos0 = [180, -90, 0, -90, 90, 0, 0, 0]
            method = "moveByJoint"
            params = json.dumps({"targetPos":target_pos0,"speed":10})
            id = 13
            sendStr = "{{\"method\":\"{0}\",\"params\":{1},\"jsonrpc\":\"2.0\",\"id\":{2}}}".format(method,params,id)+"\n"
            self.sock.sendall(bytes(sendStr,"utf-8"))
            sock_recv = self.sock.recv(1024)

        if sender.text() == "MethodTest":
            #region
            '''
            print("PS2 透传")
            # 获取机器人状态
            # suc , result , id = sendCMD(sock , "getRobotState")
            method = "getRobotState"
            params = []
            id = 9
            sendStr="{{\"method\":\"{0}\",\"params\":{1},\"jsonrpc\":\"2.0\",\"id\":{2}}}".format(method,params,id)+"\n"
            self.sock.sendall(bytes(sendStr,"utf-8"))
            ret = self.sock.recv(1024)
            jdata = json.loads(str(ret,"utf-8"))
            self.robot_state = json.loads(jdata["result"])
            if (self.robot_state == 4):
                # 清除报警
                # suc , result , id = sendCMD(sock , "clearAlarm", {"force": 0})
                method = "clearAlarm"
                params = json.dumps({"force": 0})
                id = 10
                sendStr="{{\"method\":\"{0}\",\"params\":{1},\"jsonrpc\":\"2.0\",\"id\":{2}}}".format(method,params,id)+"\n"
                self.sock.sendall(bytes(sendStr,"utf-8"))
                ret = self.sock.recv(1024)
                jdata = json.loads(str(ret,"utf-8"))
                self.ret_clearalarm = json.loads(jdata["result"])
                print("testpass",self.ret_clearalarm)
                time.sleep (0.5)
            # 获取同步状态
            # suc , result , id = sendCMD(sock , "getMotorStatus")
            method = "getMotorStatus"
            params = []
            id = 11
            sendStr="{{\"method\":\"{0}\",\"params\":{1},\"json\":\"2.0\",\"id\":{2}}}".format(method,params,id)+"\n"
            self.sock.sendall(bytes(sendStr,"utf-8"))
            ret = self.sock.recv(1024)
            jdata = json.loads(str(ret,"utf-8"))
            self.ret_Syn_state = json.loads(jdata["result"])
            if (self.ret_Syn_state == 0):
                # 同步伺服编码器数据
                # suc , result , id = sendCMD(sock , "syncMotorStatus")
                method = "syncMotorStatus"
                params = []
                id = 12
                sendStr="{{\"method\":\"{0}\",\"params\":\"{1}\",\"json\":\"2.0\".\"id\":{2}}}".format(metod,params,id)+"\n"
                self.sock.sendall(bytes(sendStr,"utf-8"))
                ret = self.sock.recv(1024)
                jdata = json.loads(str(ret,"utf-8"))
                self.ret_set_Syn_Motor = json.loads(jdata["result"])
                time.sleep (0.5)
            '''
            #endregion
            
            method = "getRobotPose"
            params = []
            id = 200
            sendStr="{{\"method\":\"{0}\",\"params\":{1},\"jsonrpc\":\"2.0\",\"id\":{2}}}".format(method,params,id)+"\n"
            self.sock.sendall(bytes(sendStr,"utf-8"))
            ret = self.sock.recv(1024)
            jdata = json.loads(str(ret,"utf-8"))
            currentpose = json.loads(jdata["result"])
            print(currentpose)
            print(currentpose[0],currentpose[1],currentpose[2])

            method = "inverseKinematic"
            params = json.dumps({"targetPose":currentpose})
            id = 201
            sendStr="{{\"method\":\"{0}\",\"params\":{1},\"jsonrpc\":\"2.0\",\"id\":{2}}}".format(method,params,id)+"\n"
            self.sock.sendall(bytes(sendStr,"utf-8"))
            ret = self.sock.recv(1024)
            jdata = json.loads(str(ret,"utf-8"))
            currentpos = json.loads(jdata["result"])
            print(currentpos)
            
            
    #endregion
    #endregion

    def RobotAllState(self):
        sender = self.sender()
        if sender.text() == "8056on":
            #self.btn_8056on.setStyleSheet('''QPushButton{background-color:rgb(0,255,0);border-radius:5px;}QPushButton:hover{background-color:rgb(255,255,0);}''')
            self.btn_8056on.setStyleSheet('''QPushButton{background-color:rgb(0,255,0);border-radius:5px;}QPushButton:hover{background-color:rgb(255,255,0);}''')
            #self.btn_8056off.setStyleSheet('''QPushButton{background-color:rgb(255,0,255);border-radius:5px;}QPushButton:hover{background-color:rgb(255,255,0);}''')
            self.btn_8056off.setStyleSheet('''QPushButton{background-color:rgb(255,0,255);border-radius:5px;}QPushButton:hover{background-color:rgb(255,255,0);}''')

            #region 运行GetDataThread线程，并保存GetDataThread线程读取到的数据
            self.getdata.start()
            self.btn_8056on.setEnabled(False)
            self.btn_8056off.setEnabled(True)
        if sender.text() == "8056off":
            #button1.setStyleSheet("QPushButton{font-family:'宋体';font-size:32px;color:rgb(0,0,0,255);}\
            #QPushButton{background-color:rgb(170,200,50)}\ QPushButton:hover{background-color:rgb(50, 170, 200)}")
            #self.btn_8056off.setStyleSheet('''QPushButton{background-color:rgb(0,255,0);border-radius:5px;}QPushButton:hover{background-color:rgb(255,255,0);}''')
            self.btn_8056off.setStyleSheet('''QPushButton{background-color:rgb(0,255,0);border-radius:5px;}QPushButton:hover{background-color:rgb(255,255,0);}''')
            #self.btn_8056on.setStyleSheet('''QPushButton{background-color:rgb(255,0,255);border-radius:5px;}QPushButton:hover{background-color:rgb(255,255,0);}''')
            self.btn_8056on.setStyleSheet('''QPushButton{background-color:rgb(255,0,255);border-radius:5px;}QPushButton:hover{background-color:rgb(255,255,0);}''')
            #ret = ctypes.windll.kernel32.TerminateThread(self.getdata.handle, 0) # @UndefinedVariable 
            #print('终止线程', self.getdata.handle, ret)
            #self.getdata.destroyed()
            self.getdata.disconnect()
            self.btn_8056off.setEnabled(False)
            self.btn_8056on.setEnabled(True)

if __name__ == '__main__':
    global flag
    
    flag  = True
    app_EliteUISDK = QApplication(sys.argv)
    Elite = EliteUISDK()
    sys.exit(app_EliteUISDK.exec_())

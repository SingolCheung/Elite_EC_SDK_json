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
# python3用pip3 install pywin32
import win32con
from win32process import SuspendThread, ResumeThread

####Python端代码#####
class elt_error(Structure):
    _field_ = [
        ('code', c_int),
        ('err_msg', c_char * 256)
    ]

#region 动态链接库Dll的所有函数接口--API
#动态链接库的路径
dllpath = "D:\\Informations\\VScode\\GUI_sdk\\eltrobot.dll"
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
#M528 = c_int(528)
#status = c_int(0)
error_message = elt_error()
#转换后在Python中的函数
# ret = Elite_dll.elt_get_virtual_output(c_void_p(elt_ctx), M528, byref(status), byref(error_message))
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
#M528 = c_int(528)
#status = c_int(0)
error_message = elt_error()
#转换后在Python中的函数
#ret = Elite_dll.elt_set_virtual_output(c_void_p(elt_ctx), M528, status, byref(elt_error))
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
'''
#--------------------------------------------------------------------------------------------
#endregion

class GetTimeThread(QThread):
    latest_time = pyqtSignal(str)
    def run(self):
        while True:
            data = QDateTime.currentDateTime()
            format_data = data.toString("yyyy-MM-dd HH:mm:ss:zzz ddd")
            #self.latest_time.emit(str(format_data))
            self.latest_time.emit(format_data)
            time.sleep(0.001)
#以下暂时没用
#要配合class EliteUISDK(QMainWindow):里的# self.ex = Constant(self)
class Constant(QMainWindow): #创建一个dialog,用作被调用类
    latest_8056 = pyqtSignal(str) #创建槽信号
    global falg
    def __init__(self, parent=None):
        super(Constant, self).__init__(parent)
        self.title = "Constant"
        self.left = 50
        self.top = 50
        self.width = 400
        self.height = 200
        self.value_8056 = 0
        self.flag8056 = True
        self.initUi_Constant()
 
    def initUi_Constant(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        #-------------------------------------------------------------
        self.btn_8056on = QPushButton("8056on",self)
        self.btn_8056on.setStyleSheet('''QPushButton{background-color:rgb(255,0,255);border-radius:5px;}QPushButton:hover{background-color:rgb(255,255,0);}''')
        self.btn_8056on.move(50,75)
        #-------------------------------------------------------------
        self.btn_8056off = QPushButton("8056off",self)
        self.btn_8056off.setStyleSheet('''QPushButton{background-color:rgb(255,0,255);border-radius:5px;}QPushButton:hover{background-color:rgb(255,255,0);}''')
        self.btn_8056off.move(250,75)
        #-------------------------------------------------------------
        #clicked指的是按下在松开时触发
        #pressed指的是按下触发
        self.btn_8056on.clicked.connect(self.buttonClicked)
        self.btn_8056off.clicked.connect(self.buttonClicked)
        self.show()

    # 各按钮对应的SDK函数(API)
    def buttonClicked(self):
        sender = self.sender()
        if sender.text() == "8056on":
            self.value_8056 = 1
            flag = False
            print("self.value_8056=",self.value_8056)
            print("flag =",flag)
        if sender.text() == "8056off":
            self.value_8056 = 2
            flag = True
            print("self.value_8056=",self.value_8056)
            print("flag =",flag)
        #TypeError: Constant.latest_8056[] signal has 0 argument(s) but 1 provided
        #是因为latest_8056 = pyqtSignal(str)，没有输入str 
        self.latest_8056.emit(str(self.value_8056))
        print("self.latest_8056=",self.latest_8056)

#region GetDataThread
class GetDataThread(QThread):
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
            if index %10 == 0:
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

class EliteUISDK(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "SDK control UI"
        self.left = 1300
        self.top = 50
        self.width = 600
        self.height = 950
        self.elt_ctx_self = c_void_p()
        self.input_time = QLineEdit(self)
        self.input_time.setGeometry(350,915,250,30)
        #self.input_time.resize(100,800)
        #self.value_8056 = 0
        # self.ex = Constant(self)
        self.startParm = "cmd8056"
        #self.constant = Constant(self)
        #region GetDataThread线程读取的数据输入到EliteUISDK页面所在的位置
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
        self.UI()
    #按钮执行事件
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

    def UI(self): 
        self.getdata1 = GetTimeThread()
        self.getdata1.latest_time.connect(self.timeDisplay)
        # 创建线程后立刻启动线程，不需要启动信号
        self.getdata1.start()
        
        #region 实例化创建一个8056的线程
        # 实例化创建一个线程
        # 运行GetDataThread线程，并保存GetDataThread线程读取到的数据
        # 线程的启动放在def workerStart(self):
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
        '''
        self.current_time = GetTimeThread()
        self.current_time.latest_time.connect(self.timeDisplay)
        self.current_time.start()
        #region 运行GetDataThread线程，并保存GetDataThread线程读取到的数据
        self.current_posj1 = GetDataThread()
        self.current_posj1.latest_posj1.connect(self.posj1Display)
        self.current_posj1.start()
        self.current_posj2 = GetDataThread()
        self.current_posj2.latest_posj2.connect(self.posj2Display)
        self.current_posj2.start()
        self.current_posj3 = GetDataThread()
        self.current_posj3.latest_posj3.connect(self.posj3Display)
        self.current_posj3.start()
        self.current_posj4 = GetDataThread()
        self.current_posj4.latest_posj4.connect(self.posj4Display)
        self.current_posj4.start()
        self.current_posj5 = GetDataThread()
        self.current_posj5.latest_posj5.connect(self.posj5Display)
        self.current_posj5.start()
        self.current_posj6 = GetDataThread()
        self.current_posj6.latest_posj6.connect(self.posj6Display)
        self.current_posj6.start()

        self.current_posex = GetDataThread()
        self.current_posex.latest_posex.connect(self.posexDisplay)
        self.current_posex.start()
        self.current_posey = GetDataThread()
        self.current_posey.latest_posey.connect(self.poseyDisplay)
        self.current_posey.start()
        self.current_posez = GetDataThread()
        self.current_posez.latest_posez.connect(self.posezDisplay)
        self.current_posez.start()
        self.current_poserx = GetDataThread()
        self.current_poserx.latest_poserx.connect(self.poserxDisplay)
        self.current_poserx.start()
        self.current_posery = GetDataThread()
        self.current_posery.latest_posery.connect(self.poseryDisplay)
        self.current_posery.start()
        self.current_poserz = GetDataThread()
        self.current_poserz.latest_poserz.connect(self.poserzDisplay)
        self.current_poserz.start()

        self.current_robotstate = GetDataThread()
        self.current_robotstate.latest_robotstate.connect(self.robotstateDisplay)
        self.current_robotstate.start()
        self.current_mode = GetDataThread()
        self.current_mode.latest_mode.connect(self.modeDisplay)
        self.current_mode.start()
        self.current_synchronize = GetDataThread()
        self.current_synchronize.latest_synchronize.connect(self.synchronizeDisplay)
        self.current_synchronize.start()
        self.current_brake = GetDataThread()
        self.current_brake.latest_synchronize.connect(self.brakeDisplay)
        self.current_brake.start()
        #endregion
        '''
        #endregion
        
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        #region 定义基本按钮名字、背景颜色以及在窗口的位置
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
        self.btn_Var_M .move(10,650)
        #-------------------------------------------------------------
        self.btn_waypoint = QPushButton("Waypoint",self)
        self.btn_waypoint.setStyleSheet('''QPushButton{background-color:rgb(255,0,255);border-radius:5px;}QPushButton:hover{background-color:rgb(255,255,0);}''')
        self.btn_waypoint.move(10,700)
        #-------------------------------------------------------------
        #endregion
        
        #region Button 定义关节按钮以及在窗口的位置
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
        #region Button 定义X Y Z Rx Ry Rz 按钮以及在窗口的位置
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
        #-------------------------------------------------------------

        #!!!!!!!!!!!!!!!!!!!!!!! Label !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
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
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        #clicked指的是按下在松开时触发
        #pressed指的是按下触发
        #self.btn_8056on.clicked.connect(self.buttonClicked)
        #self.btn_8056off.clicked.connect(self.buttonClicked)
        self.btn_8056on.clicked.connect(self.workerStart)
        self.btn_8056off.clicked.connect(self.workerStart)
        
        self.btn_createctx.clicked.connect(self.buttonClicked)
        self.btn_login.clicked.connect(self.buttonClicked)
        self.btn_logout.clicked.connect(self.buttonClicked)
        self.btn_destroyctx.clicked.connect(self.buttonClicked)
        self.btn_Var_M.clicked.connect(self.buttonClicked)
        self.btn_syn.clicked.connect(self.buttonClicked)
        self.btn_unsyn.clicked.connect(self.buttonClicked)
        self.btn_clearalarm.clicked.connect(self.buttonClicked)
        self.btn_servoenable.clicked.connect(self.buttonClicked)
        self.btn_run.clicked.connect(self.buttonClicked)
        self.btn_pause.clicked.connect(self.buttonClicked)
        self.btn_dragmove.clicked.connect(self.buttonClicked)
        self.btn_waypoint.clicked.connect(self.buttonClicked)
        #region 关节按钮pressed连接
        #J1
        #点击信号与槽函数进行连接，实现的目的：输入安妞的当前状态，按下还是释放
        #btn_j1negative.clicked.connect(lambda:self.btnstate(btn_j1negative))
        btn_j1negative.pressed.connect(lambda:self.btnstate(btn_j1negative))
        btn_j1negative.setAutoRepeat(True)
        btn_j1negative.setAutoRepeatDelay(150)
        btn_j1negative.setAutoRepeatInterval(1)
        #btn_j1positive.clicked.connect(self.buttonClicked)
        btn_j1positive.pressed.connect(lambda:self.btnstate(btn_j1positive))
        btn_j1positive.setAutoRepeat(True)
        btn_j1positive.setAutoRepeatDelay(150)
        btn_j1positive.setAutoRepeatInterval(1)
        #J2
        btn_j2negative.pressed.connect(lambda:self.btnstate(btn_j2negative))
        btn_j2negative.setAutoRepeat(True)
        btn_j2negative.setAutoRepeatDelay(150)
        btn_j2negative.setAutoRepeatInterval(1)
        btn_j2positive.pressed.connect(lambda:self.btnstate(btn_j2positive))
        btn_j2positive.setAutoRepeat(True)
        btn_j2positive.setAutoRepeatDelay(150)
        btn_j2positive.setAutoRepeatInterval(1)
        #J3
        btn_j3negative.pressed.connect(lambda:self.btnstate(btn_j3negative))
        btn_j3negative.setAutoRepeat(True)
        btn_j3negative.setAutoRepeatDelay(150)
        btn_j3negative.setAutoRepeatInterval(1)
        btn_j3positive.pressed.connect(lambda:self.btnstate(btn_j3positive))
        btn_j3positive.setAutoRepeat(True)
        btn_j3positive.setAutoRepeatDelay(150)
        btn_j3positive.setAutoRepeatInterval(1)
        #J4
        btn_j4negative.pressed.connect(lambda:self.btnstate(btn_j4negative))
        btn_j4negative.setAutoRepeat(True)
        btn_j4negative.setAutoRepeatDelay(150)
        btn_j4negative.setAutoRepeatInterval(1)
        btn_j4positive.pressed.connect(lambda:self.btnstate(btn_j4positive))
        btn_j4positive.setAutoRepeat(True)
        btn_j4positive.setAutoRepeatDelay(150)
        btn_j4positive.setAutoRepeatInterval(1)
        #J5
        btn_j5negative.pressed.connect(lambda:self.btnstate(btn_j5negative))
        btn_j5negative.setAutoRepeat(True)
        btn_j5negative.setAutoRepeatDelay(150)
        btn_j5negative.setAutoRepeatInterval(1)
        btn_j5positive.pressed.connect(lambda:self.btnstate(btn_j5positive))
        btn_j5positive.setAutoRepeat(True)
        btn_j5positive.setAutoRepeatDelay(150)
        btn_j5positive.setAutoRepeatInterval(1)
        #J6
        btn_j6negative.pressed.connect(lambda:self.btnstate(btn_j6negative))
        btn_j6negative.setAutoRepeat(True)
        btn_j6negative.setAutoRepeatDelay(150)
        btn_j6negative.setAutoRepeatInterval(1)
        btn_j6positive.pressed.connect(lambda:self.btnstate(btn_j6positive))
        btn_j6positive.setAutoRepeat(True)
        btn_j6positive.setAutoRepeatDelay(150)
        btn_j6positive.setAutoRepeatInterval(1)
        #endregion
        #region X Y Z Rx Ry Rz 按钮pressed连接
        #X
        btn_xnegative.pressed.connect(lambda:self.btnstate(btn_xnegative))
        btn_xnegative.setAutoRepeat(True)
        btn_xnegative.setAutoRepeatDelay(150)
        btn_xnegative.setAutoRepeatInterval(1)
        btn_xpositive.pressed.connect(lambda:self.btnstate(btn_xpositive))
        btn_xpositive.setAutoRepeat(True)
        btn_xpositive.setAutoRepeatDelay(150)
        btn_xpositive.setAutoRepeatInterval(1)
        #Y
        btn_ynegative.pressed.connect(lambda:self.btnstate(btn_ynegative))
        btn_ynegative.setAutoRepeat(True)
        btn_ynegative.setAutoRepeatDelay(150)
        btn_ynegative.setAutoRepeatInterval(1)
        btn_ypositive.pressed.connect(lambda:self.btnstate(btn_ypositive))
        btn_ypositive.setAutoRepeat(True)
        btn_ypositive.setAutoRepeatDelay(150)
        btn_ypositive.setAutoRepeatInterval(1)
        #Z
        btn_znegative.pressed.connect(lambda:self.btnstate(btn_znegative))
        btn_znegative.setAutoRepeat(True)
        btn_znegative.setAutoRepeatDelay(150)
        btn_znegative.setAutoRepeatInterval(1)
        btn_zpositive.pressed.connect(lambda:self.btnstate(btn_zpositive))
        btn_zpositive.setAutoRepeat(True)
        btn_zpositive.setAutoRepeatDelay(150)
        btn_zpositive.setAutoRepeatInterval(1)
        #Rx
        btn_rxnegative.pressed.connect(lambda:self.btnstate(btn_rxnegative))
        btn_rxnegative.setAutoRepeat(True)
        btn_rxnegative.setAutoRepeatDelay(150)
        btn_rxnegative.setAutoRepeatInterval(1)
        btn_rxpositive.pressed.connect(lambda:self.btnstate(btn_rxpositive))
        btn_rxpositive.setAutoRepeat(True)
        btn_rxpositive.setAutoRepeatDelay(150)
        btn_rxpositive.setAutoRepeatInterval(1)
        #Ry
        btn_rynegative.pressed.connect(lambda:self.btnstate(btn_rynegative))
        btn_rynegative.setAutoRepeat(True)
        btn_rynegative.setAutoRepeatDelay(150)
        btn_rynegative.setAutoRepeatInterval(1)
        btn_rypositive.pressed.connect(lambda:self.btnstate(btn_rypositive))
        btn_rypositive.setAutoRepeat(True)
        btn_rypositive.setAutoRepeatDelay(150)
        btn_rypositive.setAutoRepeatInterval(1)
        #Rz
        btn_rznegative.pressed.connect(lambda:self.btnstate(btn_rznegative))
        btn_rznegative.setAutoRepeat(True)
        btn_rznegative.setAutoRepeatDelay(150)
        btn_rznegative.setAutoRepeatInterval(1)
        btn_rzpositive.pressed.connect(lambda:self.btnstate(btn_rzpositive))
        btn_rzpositive.setAutoRepeat(True)
        btn_rzpositive.setAutoRepeatDelay(150)
        btn_rzpositive.setAutoRepeatInterval(1)
        #endregion
        self.statusBar()

        #btn_operationmode = QPushButton("Operation Mode",self)
        #button.move("This is an example button")
        
        btn_teach = QRadioButton("TEACH",self)                        #实例化一个单选择的按钮
        btn_teach.setChecked(True)                                    #设置按钮点点击状态
        btn_teach.toggled.connect(lambda:self.btnstate(btn_teach))    #绑定点击事件
        btn_teach.move(10,800)
        btn_play = QRadioButton("PLAY",self)                           #实例化一个单选择的按钮
        btn_play.setChecked(True)                                      #设置按钮点点击状态
        btn_play.toggled.connect(lambda:self.btnstate(btn_play))       #绑定点击事件
        btn_play.move(10,830)
        btn_remote = QRadioButton("REMOTE",self)                       #实例化一个单选择的按钮
        btn_remote.setChecked(True)                                    #设置按钮点点击状态
        btn_remote.toggled.connect(lambda:self.btnstate(btn_remote))   #绑定点击事件
        btn_remote.move(10,860)
        self.show()

    def timeDisplay(self,data):
        self.input_time.setText(data)
    #region 把从GetDataThread读取到的数据--关节角度(pos)写入并显示到UI页面里
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
    #region 把从GetDataThread读取到的数据--world下的位姿(X Y Z Rx Ry Rz)写入并显示到UI页面里
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
    #region 把从GetDataThread读取到的数据--机器人状态写入并显示到UI页面里机器人状态
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

    #region 各按钮对应的SDK函数(API)
    def buttonClicked(self):
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
            ret = Elite_dll.elt_login(c_void_p(self.elt_ctx_self))
            self.btn_login.setStyleSheet('''QPushButton{background-color:rgb(0,255,0);border-radius:5px;}QPushButton:hover{background-color:rgb(255,255,0);}''')
            self.btn_logout.setStyleSheet('''QPushButton{background-color:rgb(255,0,255);border-radius:5px;}QPushButton:hover{background-color:rgb(255,255,0);}''')
            print("login=",ret)
        if sender.text() == "Logout":
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
                    ret = Elite_dll.elt_set_servo_status(c_void_p(self.elt_ctx_self), state, byref(error_message))
                    self.btn_servoenable.setStyleSheet('''QPushButton{background-color:rgb(0,255,0);border-radius:5px;}QPushButton:hover{background-color:rgb(255,255,0);}''')
                    print("ServoState=",state)
                if status.value == 1:
                    state = 0
                    self.btn_servoenable.setStyleSheet('''QPushButton{background-color:rgb(255,0,255);border-radius:5px;}QPushButton:hover{background-color:rgb(255,255,0);}''')
                    ret = Elite_dll.elt_set_servo_status(c_void_p(self.elt_ctx_self), state, byref(error_message))
                    print("ServoState=",state)
            print("ServoEnable =",ret)
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
            M528 = c_int(528)
            status = c_long(0)
            v_status = 0
            ret = Elite_dll.elt_get_virtual_output(c_void_p(self.elt_ctx_self), M528, byref(status), byref(error_message))
            print("M528=", status)
            if status.value == 0:
                v_status = 1
                ret = Elite_dll.elt_set_virtual_output(c_void_p(self.elt_ctx_self), M528, v_status, byref(error_message))
            if status.value  == 1:
                v_status = 0
                ret = Elite_dll.elt_set_virtual_output(c_void_p(self.elt_ctx_self), M528, v_status, byref(error_message))
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
        
    #endregion

    def workerStart(self):
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
            self.getdata.destroyed()
            
            self.btn_8056off.setEnabled(False)
            self.btn_8056on.setEnabled(True)

if __name__ == '__main__':
    global flag
    flag  = True
    app_EliteUISDK = QApplication(sys.argv)
    Elite = EliteUISDK()
    sys.exit(app_EliteUISDK.exec_())

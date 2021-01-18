# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication, QRadioButton, QLabel, QLineEdit, QDialog, QFormLayout, QVBoxLayout
# from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread, pyqtSignal, QDateTime
from PyQt5.QtGui import *
import time
from ctypes import *
import ctypes
import socket
import collections
import struct
import math
import json
import pygame

####Python端代码#####
class elt_error(Structure):
    _field_ = [
        ('code', c_int),
        ('err_msg', c_char * 256)
    ]

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
        self.json_setservo_once = 0
        #self.input_time.resize(100,800)
        #self.value_8056 = 0
        # self.ex = Constant(self)
        #self.constant = Constant(self)
        #region Joystick——PS2各按钮状态显示框
        self.joystick_status = QLineEdit(self)
        self.joystick_status.setGeometry(130,550,400,30)
        #endregion
        
        #region SDK_json输入框
        # 输入示例
        self.json_address_M = QLineEdit(self)
        self.json_address_M.setGeometry(700,350,40,30)
        self.json_address_Y = QLineEdit(self)
        self.json_address_Y.setGeometry(700,400,40,30)
        #endregion
        self.UI()

    def UI(self): 
        self.getdata1 = GetTimeThread()
        self.getdata1.latest_time.connect(self.timeDisplay)
        # 创建线程后立刻启动线程，不需要启动信号
        self.getdata1.start()
        
        self.getjoystickdata = GetJoystickDataThread()
        self.getjoystickdata.joystick_status.connect(self.JoystickName)
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

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

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

        self.show()

    #实时读取当前系统的时间并写入到GUI
    def timeDisplay(self,data):
        self.input_time.setText(data)

    def JoystickName(self,data):
        self.joystick_status.setText(data)

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
            method = "stop"
            params = []
            id = 14
            sendStr="{{\"method\":\"{0}\",\"params\":{1},\"jsonrpc\":\"2.0\",\"id\":{2}}}".format(method,params,id)+"\n"
            self.sock.sendall(bytes(sendStr,"utf-8"))
            ret = self.sock.recv(1024)
            jdata = json.loads(str(ret,"utf-8"))
            print("stop")
        if self.SDK_json_on == 1 and self.json_btn_l2_value == 1:
            self.json_ps2_button_on = 1
            method = "jog"
            params = json.dumps({"index":0})
            id = 15
            sendStr="{{\"method\":\"{0}\",\"params\":{1},\"jsonrpc\":\"2.0\",\"id\":{2}}}".format(method,params,id)+"\n"
            self.sock.sendall(bytes(sendStr,"utf-8"))
            ret = self.sock.recv(1024)
            jdata = json.loads(str(ret,"utf-8"))
            #print("self.json_btn_l2_value",self.json_btn_l2_value)
    def Json_BtnL1(self,data):
        self.json_btn_l1_value = float(data)
        if self.SDK_json_on == 1 and self.json_btn_l1_value == 0 and self.json_ps2_button_on == 2:
            self.json_ps2_button_on = 0
            #stop
            method = "stop"
            params = []
            id = 16
            sendStr="{{\"method\":\"{0}\",\"params\":{1},\"jsonrpc\":\"2.0\",\"id\":{2}}}".format(method,params,id)+"\n"
            self.sock.sendall(bytes(sendStr,"utf-8"))
            ret = self.sock.recv(1024)
            jdata = json.loads(str(ret,"utf-8"))
            print("stop")
        if self.SDK_json_on == 1 and self.json_btn_l1_value == 1:
            self.json_ps2_button_on = 2
            method = "jog"
            params = json.dumps({"index":1})
            id = 17
            sendStr="{{\"method\":\"{0}\",\"params\":{1},\"jsonrpc\":\"2.0\",\"id\":{2}}}".format(method,params,id)+"\n"
            self.sock.sendall(bytes(sendStr,"utf-8"))
            ret = self.sock.recv(1024)
            jdata = json.loads(str(ret,"utf-8"))
            #print("self.json_btn_l1_value",self.json_btn_l1_value)
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
        self.json_btn_left_right_value = int(data)
        if self.SDK_json_on == 1 and self.json_btn_left_right_value == 0 and self.json_ps2_button_on == 5:
            self.json_ps2_button_on = 0
            self.json_setservo_once = 0
            #stop
            print("release button")
        if self.SDK_json_on == 1 and self.json_btn_left_right_value == 1:
            self.json_ps2_button_on = 5
            if self.json_setservo_once == 0:
                #获取伺服使能
                method = "getServoStatus"
                params = []
                id = 18
                sendStr="{{\"method\":\"{0}\",\"params\":{1},\"jsonrpc\":\"2.0\",\"id\":{2}}}".format(method,params,id)+"\n"
                self.sock.sendall(bytes(sendStr,"utf-8"))
                ret = self.sock.recv(1024)
                jdata = json.loads(str(ret,"utf-8"))
                print("18 jdata=",jdata)
                self.servo_status_value = json.loads(jdata["result"])
                if self.servo_status_value == 0 and self.json_setservo_once == 0:
                    method = "set_servo_status"
                    params = json.dumps({"status":1})
                    id = 19
                    sendStr="{{\"method\":\"{0}\",\"params\":{1},\"jsonrpc\":\"2.0\",\"id\":{2}}}".format(method,params,id)+"\n"
                    self.sock.sendall(bytes(sendStr,"utf-8"))
                    ret = self.sock.recv(1024)
                    jdata = json.loads(str(ret,"utf-8"))
                    print("19 jdata=",jdata)
                    self.json_setservo_once = 1
                    #self.setservoon_status_value = json.loads(jdata["result"])
                if self.servo_status_value == 1 and self.json_setservo_once == 0:
                    method = "set_servo_status"
                    params = json.dumps({"status":0})
                    id = 20
                    sendStr="{{\"method\":\"{0}\",\"params\":{1},\"jsonrpc\":\"2.0\",\"id\":{2}}}".format(method,params,id)+"\n"
                    self.sock.sendall(bytes(sendStr,"utf-8"))
                    ret = self.sock.recv(1024)
                    jdata = json.loads(str(ret,"utf-8"))
                    print("20 jdata=",jdata)
                    self.json_setservo_once = 1
            #print("self.json_btn_left_right_value",self.json_btn_left_right_value)
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
            method = "stop"
            params = []
            id = 26
            sendStr="{{\"method\":\"{0}\",\"params\":{1},\"jsonrpc\":\"2.0\",\"id\":{2}}}".format(method,params,id)+"\n"
            self.sock.sendall(bytes(sendStr,"utf-8"))
            ret = self.sock.recv(1024)
            jdata = json.loads(str(ret,"utf-8"))
            print("stop")
        if self.SDK_json_on == 1 and self.json_btn_r2_value == 1:
            self.json_ps2_button_on = 7
            method = "jog"
            params = json.dumps({"index":10})
            id = 27
            sendStr="{{\"method\":\"{0}\",\"params\":{1},\"jsonrpc\":\"2.0\",\"id\":{2}}}".format(method,params,id)+"\n"
            self.sock.sendall(bytes(sendStr,"utf-8"))
            ret = self.sock.recv(1024)
            jdata = json.loads(str(ret,"utf-8"))
            #print("self.json_btn_r2_value",self.json_btn_r2_value)
    def Json_BtnR1(self,data):
        self.json_btn_r1_value = float(data)
        if self.SDK_json_on == 1 and self.json_btn_r1_value == 0 and self.json_ps2_button_on == 8:
            self.json_ps2_button_on = 0
            #stop
            method = "stop"
            params = []
            id = 28
            sendStr="{{\"method\":\"{0}\",\"params\":{1},\"jsonrpc\":\"2.0\",\"id\":{2}}}".format(method,params,id)+"\n"
            self.sock.sendall(bytes(sendStr,"utf-8"))
            ret = self.sock.recv(1024)
            jdata = json.loads(str(ret,"utf-8"))
            print("stop")
        if self.SDK_json_on == 1 and self.json_btn_r1_value == 1:
            self.json_ps2_button_on = 8
            method = "jog"
            params = json.dumps({"index":11})
            id = 29
            sendStr="{{\"method\":\"{0}\",\"params\":{1},\"jsonrpc\":\"2.0\",\"id\":{2}}}".format(method,params,id)+"\n"
            self.sock.sendall(bytes(sendStr,"utf-8"))
            ret = self.sock.recv(1024)
            jdata = json.loads(str(ret,"utf-8"))
            #print("self.json_btn_r1_value",self.json_btn_r1_value)
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
            method = "stop"
            params = []
            id = 20
            sendStr="{{\"method\":\"{0}\",\"params\":{1},\"jsonrpc\":\"2.0\",\"id\":{2}}}".format(method,params,id)+"\n"
            self.sock.sendall(bytes(sendStr,"utf-8"))
            ret = self.sock.recv(1024)
            jdata = json.loads(str(ret,"utf-8"))
            print("stop")
        if self.SDK_json_on == 1 and self.json_btn_leftstick_updown_value > 0.1:
            self.json_ps2_button_on = 13
            method = "jog"
            params = json.dumps({"index":2})
            id = 21
            sendStr="{{\"method\":\"{0}\",\"params\":{1},\"jsonrpc\":\"2.0\",\"id\":{2}}}".format(method,params,id)+"\n"
            self.sock.sendall(bytes(sendStr,"utf-8"))
            ret = self.sock.recv(1024)
            jdata = json.loads(str(ret,"utf-8"))
            #print("self.json_btn_leftstick_updown_value",self.json_btn_leftstick_updown_value)
        if self.SDK_json_on == 1 and self.json_btn_leftstick_updown_value < -0.1:
            self.json_ps2_button_on = 13
            method = "jog"
            params = json.dumps({"index":3})
            id = 22
            sendStr="{{\"method\":\"{0}\",\"params\":{1},\"jsonrpc\":\"2.0\",\"id\":{2}}}".format(method,params,id)+"\n"
            self.sock.sendall(bytes(sendStr,"utf-8"))
            ret = self.sock.recv(1024)
            jdata = json.loads(str(ret,"utf-8"))
            #print("self.json_btn_leftstick_updown_value",self.json_btn_leftstick_updown_value)
    def Json_BtnLeftstickLeftRight(self,data):
        self.json_btn_leftstick_leftright_value = float(data)
        if self.SDK_json_on == 1 and self.json_btn_leftstick_leftright_value < 0.1 and self.json_btn_leftstick_leftright_value > -0.1 and self.json_ps2_button_on == 14:
            self.json_ps2_button_on = 0
            #stop
            method = "stop"
            params = []
            id = 23
            sendStr="{{\"method\":\"{0}\",\"params\":{1},\"jsonrpc\":\"2.0\",\"id\":{2}}}".format(method,params,id)+"\n"
            self.sock.sendall(bytes(sendStr,"utf-8"))
            ret = self.sock.recv(1024)
            jdata = json.loads(str(ret,"utf-8"))
            print("stop")
        if self.SDK_json_on == 1 and self.json_btn_leftstick_leftright_value > 0.1:
            self.json_ps2_button_on = 14
            method = "jog"
            params = json.dumps({"index":4})
            id = 24
            sendStr="{{\"method\":\"{0}\",\"params\":{1},\"jsonrpc\":\"2.0\",\"id\":{2}}}".format(method,params,id)+"\n"
            self.sock.sendall(bytes(sendStr,"utf-8"))
            ret = self.sock.recv(1024)
            jdata = json.loads(str(ret,"utf-8"))
            #print("self.json_btn_leftstick_leftright_value",self.json_btn_leftstick_leftright_value)
        if self.SDK_json_on == 1 and self.json_btn_leftstick_leftright_value < -0.1:
            self.json_ps2_button_on = 14
            method = "jog"
            params = json.dumps({"index":5})
            id = 25
            sendStr="{{\"method\":\"{0}\",\"params\":{1},\"jsonrpc\":\"2.0\",\"id\":{2}}}".format(method,params,id)+"\n"
            self.sock.sendall(bytes(sendStr,"utf-8"))
            ret = self.sock.recv(1024)
            jdata = json.loads(str(ret,"utf-8"))
            #print("self.json_btn_leftstick_leftright_value",self.json_btn_leftstick_leftright_value)
    def Json_BtnRightstickUpDown(self,data):
        self.json_btn_rightstick_updown_value = float(data)
        if self.SDK_json_on == 1 and self.json_btn_rightstick_updown_value < 0.1 and self.json_btn_rightstick_updown_value > -0.1 and self.json_ps2_button_on == 15:
            self.json_ps2_button_on = 0
            #stop
            method = "stop"
            params = []
            id = 30
            sendStr="{{\"method\":\"{0}\",\"params\":{1},\"jsonrpc\":\"2.0\",\"id\":{2}}}".format(method,params,id)+"\n"
            self.sock.sendall(bytes(sendStr,"utf-8"))
            ret = self.sock.recv(1024)
            jdata = json.loads(str(ret,"utf-8"))
            print("stop")
        if self.SDK_json_on == 1 and self.json_btn_rightstick_updown_value > 0.1:
            self.json_ps2_button_on = 15
            method = "jog"
            params = json.dumps({"index":6})
            id = 31
            sendStr="{{\"method\":\"{0}\",\"params\":{1},\"jsonrpc\":\"2.0\",\"id\":{2}}}".format(method,params,id)+"\n"
            self.sock.sendall(bytes(sendStr,"utf-8"))
            ret = self.sock.recv(1024)
            jdata = json.loads(str(ret,"utf-8"))
            #print("self.json_btn_rightstick_updown_value",self.json_btn_rightstick_updown_value)
        if self.SDK_json_on == 1 and self.json_btn_rightstick_updown_value < -0.1:
            self.json_ps2_button_on = 15
            method = "jog"
            params = json.dumps({"index":7})
            id = 32
            sendStr="{{\"method\":\"{0}\",\"params\":{1},\"jsonrpc\":\"2.0\",\"id\":{2}}}".format(method,params,id)+"\n"
            self.sock.sendall(bytes(sendStr,"utf-8"))
            ret = self.sock.recv(1024)
            jdata = json.loads(str(ret,"utf-8"))
            #print("self.json_btn_rightstick_updown_value",self.json_btn_rightstick_updown_value)
    def Json_BtnRightstickLeftRight(self,data):
        self.json_btn_rightstick_leftright_value = float(data)
        if self.SDK_json_on == 1 and self.json_btn_rightstick_leftright_value < 0.1 and self.json_btn_rightstick_leftright_value > -0.1 and self.json_ps2_button_on == 16:
            self.json_ps2_button_on = 0
            #stop
            method = "stop"
            params = []
            id = 33
            sendStr="{{\"method\":\"{0}\",\"params\":{1},\"jsonrpc\":\"2.0\",\"id\":{2}}}".format(method,params,id)+"\n"
            self.sock.sendall(bytes(sendStr,"utf-8"))
            ret = self.sock.recv(1024)
            jdata = json.loads(str(ret,"utf-8"))
            print("stop")
        if self.SDK_json_on == 1 and self.json_btn_rightstick_leftright_value > 0.1:
            self.json_ps2_button_on = 16
            method = "jog"
            params = json.dumps({"index":8})
            id = 34
            sendStr="{{\"method\":\"{0}\",\"params\":{1},\"jsonrpc\":\"2.0\",\"id\":{2}}}".format(method,params,id)+"\n"
            self.sock.sendall(bytes(sendStr,"utf-8"))
            ret = self.sock.recv(1024)
            jdata = json.loads(str(ret,"utf-8"))
            #print("self.json_btn_rightstick_leftright_value",self.json_btn_rightstick_leftright_value)
        if self.SDK_json_on == 1 and self.json_btn_rightstick_leftright_value < -0.1:
            self.json_ps2_button_on = 16
            method = "jog"
            params = json.dumps({"index":9})
            id = 35
            sendStr="{{\"method\":\"{0}\",\"params\":{1},\"jsonrpc\":\"2.0\",\"id\":{2}}}".format(method,params,id)+"\n"
            self.sock.sendall(bytes(sendStr,"utf-8"))
            ret = self.sock.recv(1024)
            jdata = json.loads(str(ret,"utf-8"))
            #print("self.json_btn_rightstick_leftright_value",self.json_btn_rightstick_leftright_value)
    #endregion

    #region json协议各按钮对应的method(接口方法)
    def json_buttonClicked(self):
        sender = self.sender()
        if self.SDK_json_on == -1 or self.SDK_json_on == 0 and sender.text() == "CreateSocket":
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
        if self.SDK_json_on == 1 and sender.text() == "CloseSocket":
            if(self.sock):
                self.sock.close()
                self.sock=None
            else:
                self.sock=None
            self.btn_closesocket.setStyleSheet('''QPushButton{background-color:rgb(0,255,0);border-radius:5px;}QPushButton:hover{background-color:rgb(255,255,0);}''')
            self.btn_createsocket.setStyleSheet('''QPushButton{background-color:rgb(255,0,255);border-radius:5px;}QPushButton:hover{background-color:rgb(255,255,0);}''')
            self.SDK_json_on = 0
            print("self.SDK_json_on=",self.SDK_json_on)
        if self.SDK_json_on == 1 and sender.text() == "RunJBI":
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

        if self.SDK_json_on == 1 and sender.text() == "ToolLoad":
            method = "cmd_set_payload"
            params = json.dumps({"point":[0,0,0],"tool_num":1,"m":0})
            id = 4
            sendStr="{{\"method\":\"{0}\",\"params\":{1},\"jsonrpc\":\"2.0\",\"id\":{2}}}".format(method,params,id)+"\n"
            self.sock.sendall(bytes(sendStr,"utf-8"))
            ret = self.sock.recv(1024)
            jdata = json.loads(str(ret,"utf-8"))
        if self.SDK_json_on == 1 and sender.text() == "路点2.0绕工具":
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
        if self.SDK_json_on == 1 and sender.text() == "PS2 透传":
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
        if self.SDK_json_on == 1 and sender.text() == "json_M":
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
        if self.SDK_json_on == 1 and sender.text() == "json_Y":
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
        if self.SDK_json_on == 1 and sender.text() == "MOVJ":
            target_pos0 = [180, -90, 0, -90, 90, 0, 0, 0]
            method = "moveByJoint"
            params = json.dumps({"targetPos":target_pos0,"speed":10})
            id = 13
            sendStr = "{{\"method\":\"{0}\",\"params\":{1},\"jsonrpc\":\"2.0\",\"id\":{2}}}".format(method,params,id)+"\n"
            self.sock.sendall(bytes(sendStr,"utf-8"))
            sock_recv = self.sock.recv(1024)

        if self.SDK_json_on == 1 and sender.text() == "MethodTest":
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

if __name__ == '__main__':
    global flag
    
    flag  = True
    app_EliteUISDK = QApplication(sys.argv)
    Elite = EliteUISDK()
    sys.exit(app_EliteUISDK.exec_())

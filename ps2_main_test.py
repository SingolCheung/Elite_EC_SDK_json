# 调用方法，将以下几行代码新建一个文件如：ps2_test.py
from ps2 import PS2Controller
import time

ps2ctl = PS2Controller(di_pin_no=26, do_pin_no=27, cs_pin_no=14, clk_pin_no=12)
ps2ctl.init()
while True:
    key_car= ps2ctl.read_once()   # 收到的字符格式为 keys:UP,RIGHT: pos(lx,ly):0,-1: pos(rx,ry): 0,-1:
    #print("检测到按键：",key_car)    
    key_list= key_car.split(':')  # 用：来将字符串进行分割，写入数组key_list中  key_list[1]输入的按键、key_list[3]左摇杆坐标、key_list[5]右摇杆坐标
    if key_list[1]=="UP": 
      print(key_car," 前进")
      
    if key_list[1]=="UP,LEFT": 
      print(key_car," 左上方")
    time.sleep(0.2)
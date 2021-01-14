#!/usr/bin/python3
# 文件名：server.py

# 导入 socket、sys 模块
import socket
import sys
import time

# 创建 socket 对象
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

# 获取本地主机名
host = socket.gethostname()
#print("host=",host) host=电脑的名称（我的电脑名称SingolCheung）
port = 8082

# 绑定端口号
#serversocket.bind((host, port))
# 该成指定本程序所在电脑的IP地址
serversocket.bind(("192.168.1.53", port))
print("server bind port and IP")

# 设置最大连接数，超过后排队
serversocket.listen(5)
print("listening............")

while True:
    # 建立客户端连接
    clientsocket,addr = serversocket.accept()      
    print("listen到client的IP地址: %s" % str(addr))
    server_recv_from_client = clientsocket.recv(1024)
    print("data=",server_recv_from_client)

    #msg='欢迎访问菜鸟教程！'+ "\r\n"
    #clientsocket.send(msg.encode('utf-8'))
    sendStr = "欢迎访问菜鸟教程！" + "\r\n"
    clientsocket.send(bytes(sendStr ,"utf -8"))

    print("开始发送T1")

    sendStr = "T1"
    clientsocket.send(bytes(sendStr ,"utf -8"))
    #time.sleep(0.5)
    #while(server_recv_from_client != "client has received: T1"):
    server_recv_from_client = clientsocket.recv(60)
    print("data=",server_recv_from_client)

    sendStr = "x,y,z,Rx,Ry,Rz"
    clientsocket.send(bytes(sendStr ,"utf -8"))
    #time.sleep(0.5)
    server_recv_from_client = clientsocket.recv(60)
    print("data=",server_recv_from_client)

    sendStr = "2"
    clientsocket.send(bytes(sendStr ,"utf -8"))
    #time.sleep(0.5)
    server_recv_from_client = clientsocket.recv(60)
    print("data=",server_recv_from_client)

    clientsocket.close()
    print("socket close")
    break
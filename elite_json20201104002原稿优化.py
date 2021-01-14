import socket
import json
import time

#v1.2

def connectETController(ip,port=8055):
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  print("sock=",sock.family)
  print("sock=",sock)
  try:
    sock.connect((ip,port))
    return (True,sock)
  except Exception as e:
    sock.close()
    return (False,)

def disconnectETController(sock):
  if(sock):
    sock.close()
    sock=None
  else:
    sock=None

def sendCMD(sock,cmd,params=None,id=1):
  if(not params):
    params=[]
  else:
    params=json.dumps(params)
  sendStr="{{\"method\":\"{0}\",\"params\":{1},\"jsonrpc\":\"2.0\",\"id\":{2}}}".format(cmd,params,id)+"\n"
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

if __name__ == "__main__":
  robot_ip="192.168.1.200"
  jbi_filename = "ab"
  #jbi的名称可以带后缀格式".jbi"，如下
  #jbi_filename = "ab.jbi"
  conSuc,sock=connectETController(robot_ip)
  if(conSuc):
    suc,result,id=sendCMD(sock,"checkJbiExist",{"filename":jbi_filename})     #check file exist
    if(suc and result==1):
      suc,result,id=sendCMD(sock,"runJbi",{"filename":jbi_filename})          #run jbi file
      if(suc and result):
        checkRunning=3
        while(checkRunning==3):                                             #wait for the jbi program is over
          suc,result,id=sendCMD(sock,"getJbiState")
          checkRunning=result["runState"]
          time.sleep(0.1)
    '''
    suc,result,id=sendCMD(sock,"getSysVarP",{"addr":1}) 
    print(result)
    '''
  disconnectETController(sock)
        




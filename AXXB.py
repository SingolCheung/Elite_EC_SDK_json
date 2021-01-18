import cv2
import numpy as np

# suppress=True用numpy输出时不用科学计数法
# precision=3 小数后3位
# floatmode='fixed'小数位补零
np.set_printoptions(suppress=True,precision=3,floatmode='fixed')

######图像坐标三个点
A= np.array([
[1188.0, 1090.0, 1],
[ 215.0,   10.0, 1],
[  15.0,  339.0, 1]
])
print("A=\n",A)

B= np.array([
[277.85,  17.22, 1],
[282.27, -30.26, 1],
[242.78,  16.11, 1]
])
print("B=\n",B)

X=np.array([])
X=np.linalg.solve(A,B)
print("X=\n",X)
#print("X=\n",[round(i,3) for i in X])

a1 = np.array([500,200,1])
b1=np.dot(X,a1)
#[round(i,3) for i in y]
print("b1=\n",b1)
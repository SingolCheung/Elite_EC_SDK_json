import numpy as np
import matplotlib.pyplot as plt


#创建坐标系 其实可以用plt.show()
x=np.linspace(0,1,5)
y=np.linspace(0,1,4)
xv,yv=np.meshgrid(x,y)
#print(xv)
#print(yv)
plt.plot(xv,yv,'*')
plt.show()
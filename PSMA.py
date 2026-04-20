import matplotlib.pyplot as plt
import numpy as np

x1 = np.array([10,100,20,90,30,80,40,70,50,60])
y1 = np.array([1,2,3,4,5,6,7,8,9,10])
y2 = np.array([1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5,10.5])
x2 = np.array([60])
y3 = np.array([11])
font1 = {'family':'Comic Sans MS', 'fontsize':15}

plt.plot(x1, y1, linewidth = '10', color = 'g', marker = 'o', label = 'x', ls = '--')
plt.plot(x1,y2, linewidth = '10', color = 'g', marker = 'o', label = 'x', ls = '--')
plt.plot(x2, y3, marker = '*', markersize = 50, color = 'y')
plt.xlabel('John 8:44')
plt.title('JEBAĆ ŻYDÓW', fontdict = font1)
plt.show()
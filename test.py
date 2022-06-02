import matplotlib.pyplot as plt
import math
import numpy
def funct(deg,k):
    v = abs(math.sin(deg))**math.sin(k)
    return v
d = numpy.arange(0,360,0.01)
k = 0.05
k1 = 0.119
k2 = 0.189
k3 = 0.2
y = [funct(math.radians(deg),k) for deg in d]
y1  = [funct(math.radians(deg),k1) for deg in d]
y2  = [funct(math.radians(deg),k2) for deg in d]
y3  = [funct(math.radians(deg),k3) for deg in d]
plt.plot(d,y)
plt.plot(d,y1)
plt.plot(d,y2)
plt.plot(d,y3)

plt.show()

import numpy as np
import matplotlib.pyplot as plt

print('-------------------------------------------------------')

x = np.linspace(start=-3., stop=3., num=1000)
y1 = np.exp(x)

fig = plt.figure()
axes = fig.add_axes([0,0,1,1])
axes.plot(x, y1)

plt.show()

print('-------------------------------------------------------')

y2 = 10 + 0.4*x - 0.3*x**2 + 0.1*x**3

fig = plt.figure()
axes = fig.add_axes([0,0,1,1])

axes.plot(x[500:], y1[500:])
axes.plot(x, y2)

plt.show()

print('-------------------------------------------------------')
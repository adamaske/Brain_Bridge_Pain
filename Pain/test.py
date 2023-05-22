import matplotlib.pyplot as plt
import numpy as np

dt = 0.001  #deltatime
t = np.arange(0, 1, dt)
f = np.cos(2*np.pi*1*t) #+ np.sin(2*np.pi*120*t) #sum of 2 frequencies
plt.plot(t, f)
plt.show()
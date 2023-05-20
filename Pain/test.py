import matplotlib.pyplot as plt
import numpy as np

time = np.linspace(0, 5, 1000)

wave = np.random.rand(1000)

plt.plot(time, wave)
plt.show()
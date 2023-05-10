import numpy as np
from scipy.fft import fft
data = np.random.uniform(-4, 4, 1250)
fft_data = fft(data)
fft_abs = np.abs(fft_data)
import matplotlib.pyplot as plt

plt.plot(data)
plt.show()
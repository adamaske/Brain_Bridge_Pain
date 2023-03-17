import numpy as np
import scipy as sp
import matplotlib.pyplot as plt

plt.style.use(['Science', 'notebook'])
plt.rcParams['figure.figsize'] = [16,22]
plt.rcParams.update({'font.size' : 18})

#create a simple signal with two frequencies
dt = 0.001  #deltatime
t = np.arange(0, 1, dt)
f = np.sin(2*np.pi*50*t) + np.sin(2*np.pi*120*t) #sum of 2 frequencies
f_clean = f
f = f + 2.5*np.random.randn(len(t)) #adding noise

#how many time steps
n = len(t) 
#create a FFT from f with n time, data f, length of data n, array of fft coefficent, magnitude and phase, 
#amplitude and share of sin v cos
fhat = np.fft.fft(f, n)
#power spectrum density, how much did it contribute to the signal
#psd[50] and psd[120] should be large
#lambda * lambda.conj = lambda.length^2. This means
#this fhat * fhat.conj = an array of fhat.magnitude^2 / n
psd = fhat * np.conj(fhat)/n  
#this is an array of frequency indices with length n
freq = (1/(dt*n)) * np.arange(n)
L = np.arange(1, np.floor(n/2), dtype='int')

#Every value above 100 becomes a 1, every below 100 becomes 0, boolean operation for array
indices = psd > 100 
#Zero them out, the indicies is now full of zeros except L[50]and L[120] because they were multiplied with 1 not 0
psdclean = psd * indices 
fhat = indices * fhat #Zero out small fourier, same as psdclean
#Do inverse fft on the filtered frequencies
ffilt = np.fft.ifft(fhat)

fig,axis = plt.subplots(3,1)
plt.sca(axis[0])
plt.plot(t, f, color='c', linewidth=1.5, label='Noisy')
plt.plot(t, f_clean, color='k', linewidth=2, label='Clean')
plt.xlim(t[0], t[-1])
plt.legend()

plt.sca(axis[1])
#for each frequency L, plot value psd[L]
plt.plot(freq[L], psd[L], color='r', linewidth=1.5, label='FFT-PowerSpectrum')
plt.xlim(freq[L[0]], freq[L[-1]]) #plot from the first frequency to the last
plt.legend()


plt.sca(axis[2])
plt.plot(t, ffilt, color='k', linewidth=2, label='Inverse FFT')
plt.xlim(t[0], t[-1])
plt.legend()

plt.show()
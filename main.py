import numpy as np
import scipy as sp
from scipy import signal
import matplotlib.pyplot as plt
rng = np.random.default_rng()

plt.rcParams['figure.figsize'] = [16,22]
plt.rcParams.update({'font.size' : 18})

plt.tight_layout()
def windowed_ft(t, x, Fs, w_pos_sec, w_len):
    
    N = len(x)
    w_pos = int(Fs * w_pos_sec)
    w_padded = np.zeros(N)
    w_padded[w_pos:w_pos + w_len] = 1
    x = x * w_padded    
    plt.figure(figsize=(8, 2))

    
    plt.subplot(1, 2, 1)
    plt.plot(t, x, c='k')
    plt.plot(t, w_padded, c='r')
    plt.xlim([min(t), max(t)])
    plt.ylim([-1.1, 1.1])
    plt.xlabel('Time (seconds)')

    plt.subplot(1, 2, 2)
    X = np.abs(np.fft.fft(x)) / Fs
    freq = np.fft.fftfreq(N, d=1/Fs)
    X = X[:N//2]
    freq = freq[:N//2]
    plt.plot(freq, X, c='k')
    plt.xlim([0, 7])
    plt.ylim([0, 3])
    plt.xlabel('Frequency (Hz)')
    plt.tight_layout()
    plt.show()
    

Fs = 128
duration = 10
omega1 = 1
omega2 = 5
N = int(duration * Fs)
t = np.arange(N) / Fs
t1 = t[:N//2]
t2 = t[N//2:]

x1 = 1.0 * np.sin(2 * np.pi * omega1 * t1)
x2 = 1 * np.sin(2 * np.pi * omega2 * t2)
x = np.concatenate((x1, x2))
w_len = 4 * Fs
windowed_ft(t, x, Fs, w_pos_sec=1, w_len=w_len)
windowed_ft(t, x, Fs, w_pos_sec=3, w_len=w_len)
windowed_ft(t, x, Fs, w_pos_sec=5, w_len=w_len)

plt.figure(figsize=(10, 2))
plt.subplot(1, 2, 1)
plt.plot(t, x, c='k')
plt.xlim([min(t), max(t)])
plt.xlabel('Time (seconds)')

plt.subplot(1, 2, 2)
X = np.abs(np.fft.fft(x)) / Fs
freq = np.fft.fftfreq(N, d=1/Fs)
X = X[:N//2]
freq = freq[:N//2]
plt.plot(freq, X, c='k')
plt.xlim([0, 7])
plt.ylim([0, 3])
plt.xlabel('Frequency (Hz)')
plt.tight_layout()
plt.show()
# Number of samplepoints
N = 1000
# sampling frequency (# of samples per second)
Fs = 256
# sample period; time spent per sample
T = 1.0 / Fs  # N*T (#samples x sample period) is the tmax, i.e., signal recording time 

x = np.linspace(0.0, N*T, N)
#generate fictitious samples with frequency 50 and 80
y = np.sin(50.0 * 2.0*np.pi*x) + 0.5*np.sin(120.0 * 2.0*np.pi*x)
#short time fourier transform
fft = signal.stft(y, Fs, window='hann', padded=True)
#fft[0] : array of sample frequencies.
#fft[1]: array of segment times.
#fft[2] : STFT of the input array
#plotting time freq analysis
plt.pcolormesh(fft[1], fft[0], np.abs(fft[2]), shading='gouraud')
plt.title('STFT Magnitude')
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.colorbar()
plt.show()

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

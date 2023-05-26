import numpy as np
import time
import os
import pathlib#paths and files
import matplotlib.pyplot as plt
from pylsl import resolve_stream#networking
from pylsl import StreamInlet
from scipy.signal import stft
from threading import Thread#custom thread class


#load model
channels = 16
recording_time = 5
recording_time = 5
sample_rate = 125


print(f"Waiting for connection to RAW Lsl Stream")
inlet = StreamInlet(resolve_stream('type', 'RAW')[0])#RAW = time series, FFT = ffts
                                                    #THIS MUST CORRESEPOND WITH OPENBCIGUI NETOWRKING
sample_rate = inlet.info().nominal_srate()                                                 

start_time = time.time()
segment_start_time = 0

data = np.zeros((int(channels), int(recording_time * sample_rate)))#data to store
for sample in range(int(recording_time * sample_rate)):#for every data point we want
    data_sample, timestamp = inlet.pull_sample()#get the saampl
    for channel in range(channels):
        data[channel][sample] = data_sample[channel]
    
print(f"Data : {data.shape}")
specs = []#store spectrograms here
for channel in range(channels):#go over every channel and create spectrograms
    time_series = data[channel]
    
    fft_data = np.fft.rfft(time_series)
    fft_freqs = np.fft.rfftfreq(len(time_series), d=1/sample_rate)
    unmodified_magnitude_spectrum = np.abs(fft_data)#get the magnitudes
    unmodified_normalized_magnitude_spectrum = unmodified_magnitude_spectrum / len(time_series)#normalize them to get correct amplitude

    window_size = 64   
    hop_length = 32
    original_frequencies, original_times, original_spectrogram = stft(time_series, window='hamming', nperseg=window_size, noverlap=window_size-hop_length, fs=sample_rate)
    
    specs.append((original_frequencies, original_times, original_spectrogram))
    debug = False
    if debug:
        plt.subplots(1,3, 1)
        t = np.linspace(0, recording_time, len(time_series))
        plt.plot(t, time_series)
        plt.xlabel('Time')
        plt.ylabel('Amplitude')
        plt.title('Time Series')
        
        plt.subplot(1,3,2)
        plt.plot(fft_freqs, np.abs(fft_data))
        plt.xlabel('Frequency')
        plt.ylabel('Amplitude')
        plt.title('Fourier Transform')
        
        plt.subplots(1,3,3)
        plt.pcolormesh(original_times, original_frequencies, np.abs(original_spectrogram), shading='auto')
        plt.colorbar()
        plt.xlabel('Time')
        plt.ylabel('Frequency')
        plt.title('Spectrogram')
        
    
    
    #plt.show()
# run trough model

specs = np.array(specs)#turn into numpy array

print(f"Spectrograms : {specs.shape}")

width = int(np.sqrt(len(specs)))
height = int(np.sqrt(len(specs)))
if (width * height) < len(specs):
    height += len(specs) - (width*height)

for index in range(len(specs)):
    
    channel_data = specs[index]
    
    freqs = channel_data[0]
    times = channel_data[1]
    spectrogram = channel_data[2]
    
    plt.subplot(width, height, int(index+1))
    plt.pcolormesh(times, freqs ,np.abs(spectrogram), shading ='auto')
    plt.title(f"Channel {index}")
    

plt.show()    

# results


# delete data
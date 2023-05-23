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
segment_duration = 5
segment_offset = 1

recording_time = 5
sample_rate = 125


print(f"Waiting for connection to RAW Lsl Stream")
inlet = StreamInlet(resolve_stream('type', 'RAW')[0])#RAW = time series, FFT = ffts
                                                    #THIS MUST CORRESEPOND WITH OPENBCIGUI NETOWRKING
                                                    

start_time = time.time()
segment_start_time = 0

data = np.zeros((channels, recording_time * sample_rate))
for sample in range(recording_time * sample_rate):
    data_sample, timestamp = inlet.pull_sample()
    for channel in range(channels):
        data[channel][sample] = data_sample[channel]
    
print(data.shape)

for channel in range(channels):
    time_series = data[channel]
    
    fft_data = np.fft.rfft(time_series)
    fft_freqs = np.fft.rfftfreq(len(time_series), d=1/sample_rate)
    unmodified_magnitude_spectrum = np.abs(fft_data)#get the magnitudes
    unmodified_normalized_magnitude_spectrum = unmodified_magnitude_spectrum / len(time_series)#normalize them to get correct amplitude

    window_size = 64   
    hop_length = 32
    original_frequencies, original_times, original_spectrogram = stft(time_series, window='hamming', nperseg=window_size, noverlap=window_size-hop_length, fs=sample_rate)
        
    plt.plot(fft_freqs, np.abs(fft_data))
    plt.show()
# run trough model



# results


# delete data
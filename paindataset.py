from pylsl import resolve_stream
from pylsl import StreamInlet
import time
import numpy as np
import asyncio
import matplotlib.pyplot as plt
from threading import Thread
from multiprocessing import Process

class CustomRecordingThread(Thread):
    def __init__(self, *args): #args for what inlet to use
        Thread.__init__(self)
        self.value = None #delcare value
        self.args = args #store args
    def run(self):
        inlet = self.args[0] #get argument
        target = self.args[1] #fucntion to run
        self.value = target(inlet) #record
        
def Connect(): #this function connects us to the lsl stream
    print('Connecting to LSL stream!')
    fft_inlet = StreamInlet(resolve_stream('type', 'FFT')[0])
    print('FFT Stream Connected')
    raw_inlet = StreamInlet(resolve_stream('type', 'RAW')[0])
    print('RAW Stream Connected')
    return fft_inlet, raw_inlet

def Record_FFT(inlet):
    print('FFT Recording Running')
    channels = 16
    recording_time = 5
    sample_rate = 125#inlet.info().nominal_srate()
    num_samples = int(recording_time * sample_rate)  
    
    print(f"FFT Channels : {channels:.1f}")
    print(f"FFT Recording Time : {recording_time:.1f}")
    print(f"FFT Sample Rate : {sample_rate:.1f}")
    print(f"FFT Sample Amount : {num_samples:.1f}") 
    
    channel_data = {}
    start_time = time.time()

    while time.time() - start_time < recording_time: #recording for recording_time
        for i in range(channels):
            sample, timestamp = inlet.pull_sample()
        if i not in channel_data:
            channel_data[i] = sample
        else:
            channel_data[i].append(sample)
        current_time = time.time() - start_time
        print(f"FFT Elapsed : {current_time}", end='\r')
    print(f"FFT Length of data : {len(channel_data):.1f}")
    data_points_amount = len(channel_data)
    
    data = np.zeros((channels, data_points_amount))
    for element in range(data_points_amount):
        for channel in range(channels):
            data[channel][element] = channel_data[element][channel]
    print(f"FFT TimeSeries Data is a {len(data)}x{len(data[0])} array")
    return data

def Record_Raw(inlet):
    print('RAW Recording Running')
    channels = 16
    recording_time = 5
    sample_rate = 125#inlet.info().nominal_srate()
    num_samples = int(recording_time * sample_rate)  
    
    print(f"RAW Channels : {channels:.1f}")
    print(f"RAW Recording Time : {recording_time:.1f}")
    print(f"RAW Sample Rate : {sample_rate:.1f}")
    print(f"RAW Sample Amount : {num_samples:.1f}") 
    
    channel_data = []
    start_time = time.time()

    while time.time() - start_time < recording_time: #recording for recording_time
        sample, timestamp = inlet.pull_sample() #each sample should contain 16 floats, 0th - 15th channel, microvoltage 
        if timestamp:#only record new samples
            channel_data.append(sample) #add to list
            current_time = time.time() - start_time
            print(f"RAW Elapsed : {current_time}", end='\r')
    print(f"RAW Length of data : {len(channel_data):.1f}")
    data_points_amount = len(channel_data)
    
    data = np.zeros((channels, data_points_amount))
    for element in range(data_points_amount):
        for channel in range(channels):
            data[channel][element] = channel_data[element][channel]
    print(f"RAW TimeSeries Data is a {len(data)}x{len(data[0])} array")
    return data
   
def Keep_Or_Discard_Recording():
    discard = input("Keep or discard this recording? [K/D]")
    if discard.lower == 'k':
        print('Saving Recording')
        return True
    elif discard.lower =='d':
        print('Discarding recording')
        return False
    else:
        print('Not recognized answer!')
        return Keep_Or_Discard_Recording()
 
if __name__ == '__main__':
    skip_connection = True

    fft_inlet, raw_inlet = Connect()

    fft_thread = CustomRecordingThread(fft_inlet, Record_FFT)#init threads
    raw_thread = CustomRecordingThread(raw_inlet, Record_Raw)

    fft_thread.start()#start both threads
    raw_thread.start()
    
    fft_thread.join()#wait for threads to complete
    raw_thread.join()
 
    fft_data = fft_thread.value#obtain values from functions they ran
    raw_data = raw_thread.value
    
    fft_channels = len(fft_data)
    fft_data_points_amount = len(fft_data[0])
    print(f"FFT Data is a {fft_channels}x{fft_data_points_amount} array")
    
    raw_channels = len(raw_data)
    raw_data_points_amount = len(raw_data[0])
    print(f"FFT Data is a {raw_channels}x{raw_data_points_amount} array")
    
    timing = input("At what second (0-5) did the pain occur?")#prompt user for when pain occured
    intensity = input("How intense was the pain (0-10)?")#prompt user for intensity
    
    keep = Keep_Or_Discard_Recording()

    #save
    #time = np.linspace(0, 5, len(raw_data))
    #plt.plot(time, raw_data)
    #plt.ylim(-200, 200)
    #plt.show()
    #print(fft_data)
    #print(raw_data)
    
    #transformed = Transform_FFT_Data(data)
    
    
    
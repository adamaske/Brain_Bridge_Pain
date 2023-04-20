from pylsl import resolve_stream
from pylsl import StreamInlet
import time
import numpy as np
import asyncio
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
    print('EEG Recording Ran')
    return 1
    print('Recording EEG')
    channels = 16
    recording_time = 5
    sample_rate = inlet.info().nominal_srate()
    num_samples = int(recording_time * sample_rate)    
    data = np.empty((num_samples, channels))#625, 16
    for i in range(num_samples):
        sample, timestamp = inlet.pull_sample()
        fft = sample[:channels]#the sample
        data[i] = fft
        remaining_time = recording_time - (i+1)/sample_rate
        print(f"Remaining recording time: {remaining_time:.1f} seconds", end='\r')#display how much time is left
        time.sleep(1 / sample_rate)
        
    return data
def Record_Raw(inlet):
    print('Raw Recording Ran')
    return 1
def Transform_FFT_Data(data):
    #the data comes in as 625 x 16, we want 16 x 625
    print('Transforming FFT Data')
    
if __name__ == '__main__':
    skip_connection = True

    fft_inlet, raw_inlet = Connect()

    fft_thread = CustomRecordingThread(fft_inlet, Record_FFT)#init threads
    raw_thread = CustomRecordingThread(fft_inlet, Record_Raw)
    
    raw_thread.start()#start both threads
    fft_thread.start()
    
    fft_thread.join()#wait for threads to complete
    raw_thread.join()
 
    fft_data = fft_thread.value#obtain values from functions they ran
    raw_data = raw_thread.value

    print(fft_data)
    print(raw_data)
    
    #transformed = Transform_FFT_Data(data)
    
    
    
#this script should run for x amount of time
from pylsl import resolve_stream#networking
from pylsl import StreamInlet
import numpy as np
import time
import os
import pathlib#paths and files
#THIS MUST CORRESEPOND WITH OPENBCIGUI NETOWRKING
inlet = StreamInlet(resolve_stream('type', 'RAW')[0])#RAW = time series, FFT = ffts

sample_time = 5

num_samples = 3

channels = 16
recording_time = 5
sample_rate = inlet.info().nominal_srate()
#num_samples = int(recording_time * sample_rate)  
    
print(f"Channels : {channels:.1f}")
print(f"Recording Time : {recording_time:.1f}")
print(f"Sample Rate : {sample_rate:.1f}")
print(f"Sample Amount : {num_samples:.1f}") 
samples = []#store all the 5 seconds recordings

for sample in range(num_samples):
    print(f"Starting recording {sample:.0f}!")
    recording = [[] for i in range(channels)]#save the 5 seconds of data here
    
    start_time = time.time()
    for re in range(int(recording_time * sample_rate)):
        data, timestamp = inlet.pull_sample()#for raw data, this should fire 16 data points 250 times per second
        if re == 0:
            print(f"Inlet data : {len(data)}")
        for channel in range(len(data)):
            recording[channel].append(data[channel])
        #recording.append(data)#add data to recording
    print(f"Finished recording {sample}")
    
    data = np.array(recording)
    
    print(f"Recorded data : {len(recording)} x {len(recording[0])}")
    samples.append(recording)

print(f"Recording samples is finished!")

current_dir = pathlib.Path(__file__).parent#get current folder
path = os.path.join(current_dir, "Datasets", "NormalData")#get directory to save recording
file_prefix = "normal_eeg_data_"
file_suffix = ".npy"

save_individually = False

file_index = 3
if save_individually == False:
    file_name = file_prefix + str(file_index) + file_suffix#file name
    file_path = os.path.join(path, file_name)#file path
    data = np.array(samples)#create np array from it
    np.save(file_path, data)#save it
    print(f"Saved data : {data.shape} at {file_path}!")    
    exit()

start_from = 100
for sample in range(len(samples)):
    data = np.array(samples[sample])
    if sample - start_from == 0:
        print(f"Saving data : {data.shape}")
        
    file_name = "normal_eeg_data_" + str(sample + start_from) + ".npy"
    file_path = os.path.join(path, file_name)
    #np.save(file_path, data)
    #save 
#what does 
data = np.array(samples)
print(f"Samples : {data.shape}")
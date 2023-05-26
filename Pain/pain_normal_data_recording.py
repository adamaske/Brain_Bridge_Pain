#this script should run for x amount of time
from pylsl import resolve_stream#networking
from pylsl import StreamInlet
import numpy as np
import time
import os
import pathlib#paths and files

#---- FILTERS MUST BE ON IN THE OPENBCI GUI -------
inlet = StreamInlet(resolve_stream('type', 'RAW')[0])#RAW = time series, FFT = ffts
                                                     #THIS MUST CORRESEPOND WITH OPENBCIGUI NETOWRKING

num_samples = 10#How many samples to record this session ?

channels = 16 #how many channels are there 
recording_time = 5#How long does one sample last ? 

sample_rate = inlet.info().nominal_srate()#how fast does the inlet output
    
print(f"Channels : {channels:.1f}")
print(f"Recording Time : {recording_time:.1f}")
print(f"Sample Rate : {sample_rate:.1f}")
print(f"Sample Amount : {num_samples:.1f}")
 
samples = np.zeros((0, int(channels), int(recording_time * sample_rate)))#array to hold all recordings

for sample in range(1, num_samples+1):
    print(f"Starting recording {sample:.0f}!")

    start_time = time.time()#cache the time
    
    recording = [[] for i in range(channels)]#Cache the incoming data
    
    for data_point in range(int(recording_time * sample_rate)):#
        raw_data, timestamp = inlet.pull_sample()#for raw data, this should fire 16 data points 250 times per second
        
        for channel in range(len(raw_data)):#for each channel
            recording[channel].append(raw_data[channel])#add each channel to the recording
    print(f"Finished recording {sample}")
    
    time_recroded = time.time() - start_time#How long did the recording last ? 
    print(f"Recorded for {time_recroded:.1f} seconds!")
    
    recorded_data = np.array(recording)#make to numpy array
    print(f"Recorded data : {recorded_data.shape}")
    print(f"Data : {samples.shape}")
    samples = np.vstack((samples, recorded_data))#Add recording to the samples
    print(f"Samples : {samples.shape}")

print(f"Recording is finished!")
print(f"Samples : {samples.shape}")

#-----------SAVE THE RECORDED DATA TO FILE----------------

current_dir = pathlib.Path(__file__).parent#get current folder
path = os.path.join(current_dir, "Datasets", "NormalData")#get directory to save recording

file_name = "normal_eeg_data.npy"#file name
file_path = os.path.join(path, file_name)#file path
old_data = 0

data = np.array(samples)#Create numpt array from the recordings

force_file_override = False#Enabling this will clear the previously existing file
#TODO implement file override
if force_file_override:
    if os.path.isfile(file_path):#does the file already exist ? 
        print(f"{file_name} exists and is being overwritten!")
        
    data = np.array(samples)#Create array from samples
    np.save(file_path, data)#Save the data
    print(f"Saved {data.shape} at {file_name}")
    exit()
    
if os.path.isfile(file_path): #If the file already exist we add to the file instead of overriding it
    print(f"{file_name} exists!")
    
    old_data = np.load(file_path)#Get the arrays that already exists
    print(f"Old data : {old_data.shape}")#check shape of old data
    
    data = np.array(samples)#create np array from the samples recorded
    new_data = np.vstack((old_data, data))#Add new data to old data
    print(f"New data : {new_data.shape}")
    
    np.save(file_path, new_data)#Save the new data
    
    print(f"Saved a {new_data.shape} numpy array to {file_name}")

else:#The files does not exist already
    print(f"{file_name} does not exist!")
    #Create array from samples
    np.save(file_path, data)#Save the data
    print(f"Saved {data.shape} at {file_name}")
    
    

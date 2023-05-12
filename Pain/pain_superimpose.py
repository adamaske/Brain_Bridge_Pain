import random
import numpy as np
import time
import os
import pathlib#paths and files
import matplotlib.pyplot as plt
#import data set of normal EEG data

channels = 16
recording_time = 5
sample_rate = 250

data = np.zeros((0, int(channels), int(recording_time * sample_rate)))#array to hold all recordings


current_dir = pathlib.Path(__file__).parent#get current folder
path = os.path.join(current_dir, "Datasets", "NormalData")#get directory to save recording

file_prefix = "normal_eeg_data_"
file_suffix = ".npy"
file_index = 0

file_name = file_prefix + str(file_index) + file_suffix
file_path = os.path.join(path, file_name)
while os.path.isfile(file_path):#continue until there is no more file
    samples = np.load(file_path)
    print(f"Loaded sample {samples.shape} at {file_name}!")

    data = np.vstack((data, samples))#add to data
    print(f"Data : {data.shape}")
    
    file_index = file_index + 1#iterate to next file
    file_name =  file_prefix + str(file_index) + file_suffix
    file_path = os.path.join(path, file_name)#set new file path
print(f"Found {file_index} files!")
print(f"All data : {data.shape}")
t = np.linspace(0, recording_time, int(recording_time * sample_rate))
plt.plot(t, data[0][14])
plt.plot(t, data[11][14])
plt.show()
samples = []
existing_recordings = 0#how many recordings already exists

num_samples = len(data)#how many samples of Normal EEG data do we have
num_generate_samples = 10000#how many samples shoulde we make?
sample_length = 5
max_intensity = 10
for sample in range(num_generate_samples):#loop to create
    pain = 1#random.randint(1,100)#pain or not
    timing = random.randint(0, sample_length)
    intensity = random.randint(0, max_intensity)
    
    
    print(f"Making sample {sample:.1f}", end='\r')
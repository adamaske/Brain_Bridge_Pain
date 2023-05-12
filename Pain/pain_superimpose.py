import random
import numpy as np
import time
import os
import pathlib#paths and files
import matplotlib.pyplot as plt
import json
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

samples = []
existing_recordings = 0#how many recordings already exists

num_samples = len(data)#how many samples of Normal EEG data do we have
num_generate_samples = num_samples#10000#how many samples shoulde we make?
max_intensity = 10
imposed_data = data#np.array((num_samples, channels, int(recording_time * sample_rate)))

labels = []
for sample in range(num_generate_samples):#loop to create
    pain = 1#random.randint(1,100)#pain or not
    timing = random.randint(1, recording_time-1)
    intensity = random.randint(1, max_intensity)
    for channel in range(channels):
        val = data[sample][channel]
    obj = {
        "pain" : pain,
        "timing" : timing,
        "intensity" : intensity
    }
    labels.append(obj)
    print(f"Making sample {sample:.1f}", end='\r')
print(f"Length of labels {len(labels)}")

#save imposed data
current_dir = pathlib.Path(__file__).parent#get current folder
path = os.path.join(current_dir, "Datasets", "PainData")#get directory to save recording

file_prefix = "imposed_eeg_data_"
file_suffix = ".npy"
file_index = 0

file_name = file_prefix + str(file_index) + file_suffix
file_path = os.path.join(path, file_name)
while os.path.isfile(file_path):#continue until there is no more file
    
    file_index = file_index + 1#iterate to next file
    file_name =  file_prefix + str(file_index) + file_suffix
    file_path = os.path.join(path, file_name)#set new file path
#there is no file with this file index
print(f"Saving at {file_index}")
np.save(file_path, imposed_data)#save it
print(f"Saved imposed data {imposed_data.shape} at {file_name}!")

#SAVE JSON FILE WITH LABELS
json_file_prefix = "imposed_eeg_data_label_"
json_file_suffix = ".json"
json_file_name = json_file_prefix + str(file_index) + json_file_suffix
json_file_path = os.path.join(path, json_file_name)
with open(json_file_path, "w") as file:
    json.dump(labels, file)#dump all the files 
print(f"Saved labels at {json_file_name}!")



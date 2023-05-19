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

file_name = "normal_eeg_data.npy"
file_path = os.path.join(path, file_name)
if os.path.isfile(file_path):
    print(f"{file_name} exists!")
    data = np.load(file_path)
    print(f"Loaded data : {data.shape}")
else:
    print(f"{file_name} does not exist, no data can be loaded!")
    exit()

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
        time_series = data[sample][channel]
        
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


#----------- SAVE EEG DATA IMPOSED WITH PAIN ARTIFACTS --------------
print(f"---STARTING EEG DATA SAVING---")
file_name = "imposed_eeg_data.npy"
file_path = os.path.join(path, file_name)
if os.path.isfile(file_path):#Does this file already exist ? 
    #Then we want to add to it
    print(f"{file_name} exists!")
    old_data = np.load(file_path)
    print(f"Loaded data : {old_data.shape} from {file_name}")
    print(f"Imposed data : {data.shape}")
    
    new_data = np.vstack((old_data, data))#STACK THE EXISTING DATA 
    np.save(file_path, new_data) #SAVE THE DATA TO FILE
    print(f"Saved new data : {new_data.shape} at {file_name}")
else:
    print(f"{file_name} does not exists!")
    saved_data = np.save(file_path, data)
    print(f"Saved data : {data.shape} at {file_name}")
    
#---------- SAVE JSON LABELS ---------------
print(f"---STARTING JSON SAVING---")
json_file_name = "imposed_eeg_data_labels.json"
json_file_path = os.path.join(path, json_file_name)

json_objs = labels
if os.path.isfile(json_file_path):#Does the Json file already exist ? 
    print(f"Json file already exists")
    
    loaded_json_objs = []
    with open(json_file_path, "r") as file:
        loaded_json_objs = json.load(file)
        print(f"Loaded json objs : {len(loaded_json_objs)}")
    #----- WE HAVE LOADED JSON OBJS, NOW WE MUST ADD TO THE END OF IT
    for label in range(len(loaded_json_objs)):
        json_objs.append(loaded_json_objs[label])
    print(f"Combined Json array is {len(json_objs)} long!")
    with open(json_file_path, "w") as file:
        json.dump(labels, file)#dump all the files 
    print(f"Saved {len(json_objs)} labels at {json_file_name}!")
else:
    print(f"{json_file_name} does not exist!")
    
    with open(json_file_path, "w") as file:
        json.dump(labels, file)#dump all the files 
    print(f"Saved {len(json_objs)} labels at {json_file_name}!")






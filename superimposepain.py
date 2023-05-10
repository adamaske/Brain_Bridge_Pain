import os#files
import json#files
import numpy as np#math
#load dataset
user = "Adam"#what person just recorded this
recording_count = 0#start at 0
file_prefix = "pain_recording_"#file name 
file_suffix = ".json"#suffix to look for when looking for existing files

path = os.path.join(os.getcwd(), "Datasets", user)#get directory to save recording
file_path = os.path.join(path, file_prefix + user + "_" + str(recording_count) + file_suffix)#while this file is found, iterate counter

while os.path.isfile(file_path):#find how many recording files there are
    recording_count = recording_count + 1#iterate counter because the file with this index exists
    file_path = os.path.join(path, file_prefix + user + "_" + str(recording_count) + file_suffix)#setnew file path

index = str(recording_count)
print(f"Loading files until index {index} at {path}!")

json_objects = []
for recording in range(recording_count):#loop trough all indicies
    #Load json file
    json_file_name = file_prefix + user + "_" + str(recording) + ".json"
    json_file_path = os.path.join(path, json_file_name)
    with open(json_file_path, "r") as file:#open file
       data = json.load(file)#load json object in file
    print(f"JSON File loaded : {json_file_name}")
    
    file_suffix = ".npy"#now loading numpy arrays
    #Load fft data
    fft_prefix = "pain_recoding_fft_"
    fft_file_name = fft_prefix + str(recording) + file_suffix
    fft_file_path = os.path.join(path, fft_file_name) 
    fft_data = np.load(fft_file_path)
    print(f"Loaded FFT data : {fft_file_name}!")

    #Load RAW data
    #raw data saving 
    raw_prefix = "pain_recoding_raw_"
    raw_file_name = raw_prefix + str(recording) + file_suffix
    raw_file_path = os.path.join(path, raw_file_name)  
    raw_data = np.load(raw_file_path)#save raw to file
    print(f"Loaded RAW data : {raw_file_name}!")

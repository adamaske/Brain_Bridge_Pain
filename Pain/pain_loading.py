import os#files
import json#files
import numpy as np#math
import pathlib

#load dataset
user = "Adam"#what person just recorded this
recording_count = 0#start at 0
file_prefix = "pain_recording_"#file name 
file_suffix = ".json"#suffix to look for when looking for existing files

current_dir = pathlib.Path(__file__).parent#get the current folder
path = os.path.join(current_dir, "Datasets", user)#get directory to save recording
if not os.path.exists(path):#if there is no folder for this user, then create one
    print(f"This directory does not exist : {path}!")
    exit()
    
file_path = os.path.join(path, file_prefix + user + "_" + str(recording_count) + file_suffix)#while this file is found, iterate counter
while os.path.isfile(file_path):#find how many recording files there are
    recording_count = recording_count + 1#iterate counter because the file with this index exists
    file_path = os.path.join(path, file_prefix + user + "_" + str(recording_count) + file_suffix)#setnew file path

index = str(recording_count)#
print(f"Loading files until index {index} at {path}!")

json_objects = []
fft_files = []
raw_files = []
for recording in range(recording_count):#loop trough all indicies
    data = 0
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
    
    json_objects.append(data)
    fft_files.append(fft_data)
    raw_files.append(raw_data)
    
print(f"JSON Files : {len(json_objects)}")
for user in range(len(json_objects)):
    data = json_objects[user]
    name = data["name"]
    pain = data["pain"]
    timing = data["timing"]
    intensity = data["intensity"]
    if pain == 1:
        print(f"User {name}, Pain : 1, Timing : {timing}, Intensty : {intensity}")
    else:
        print(f"User : {name}, Pain : 0")
print(f"FFT Files : {len(fft_files)}")
for index in range(len(fft_files)):
    print(f"Shape of FFT data {index} : {fft_files[index].shape}")
print(f"RAW Files : {len(raw_files)}")
for index in range(len(raw_files)):
    print(f"Shape of RAW data {index} : {raw_files[index].shape}")

exit() 
import tensorflow as tf
from tensorflow.keras.layers import Conv1D, Flatten, Dense

# Define the model
model = tf.keras.Sequential([
    Conv1D(32, 3, activation='relu', input_shape=(1000, 16)),
    Conv1D(64, 3, activation='relu'),
    Conv1D(128, 3, activation='relu'),
    Flatten(),
    Dense(64, activation='relu'),
    Dense(32, activation='relu'),
    Dense(3, activation='linear')
])

# Compile the model
model.compile(optimizer='adam',
              loss='mean_squared_error',
              metrics=['mae'])

# Train the model
model.fit(x_train, y_train, epochs=10, validation_data=(x_test, y_test))

# Make predictions
predictions = model.predict(test_data)
print(predictions)
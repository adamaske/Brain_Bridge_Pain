import random
import numpy as np
import time
import os
import pathlib#paths and files
import matplotlib.pyplot as plt
import json
from scipy.signal import stft 
import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten
from tensorflow.keras.layers import Conv1D, MaxPooling1D, BatchNormalization
#THIS SCRIPT LOADS EEG DATA THAT HAS BEEN IMPOSED WITH PAIN AND TRAINS A CNN WITH IT
channels = 16
recording_time = 5
sample_rate = 125# 125 FOR REAL, 250 FOR SYNTHETIC

data = np.zeros((0, int(channels), int(recording_time * sample_rate)))#array to hold all recordings

all_labels = []
current_dir = pathlib.Path(__file__).parent#get current folder
path = os.path.join(current_dir, "Datasets", "PainData")#get directory to save recording

#------ LOAD EEG DATA WITH PAIN IMPOSED -------------
file_name = "imposed_eeg_data.npy"
file_path = os.path.join(path, file_name)

if os.path.isfile(file_path):
    print(f"{file_name} exists!")
    loaded_data = np.load(file_path)
    print(f"Loaded data : {loaded_data.shape} from {file_name}")
    data = loaded_data
else:
    print(f"{file_path} does not exist, exiting!")
    exit()

#-------- LOAD JSON LABELS --------------
json_file_name = "imposed_eeg_data_labels.json"
json_file_path = os.path.join(path, json_file_name)

if os.path.isfile(json_file_path):
    print(f"{json_file_name} exists!")
    loaded_json = 0
    with open(json_file_path, "r") as file:
        loaded_json = json.load(file)
        print(f"Loaded json : {len(loaded_json)} from {json_file_name}")
        all_labels = loaded_json
else:
    print(f"{json_file_path} does not exist, exiting!")
    exit()
    
#------ LABELS -------------
labels = np.zeros((len(all_labels)))
for label in range(len(all_labels)): # CONVERT THE JSON OBJECTS INTO A USEABLE NUMPY ARRAY
    pain = all_labels[label]["pain"]
    timing = all_labels[label]["timing"]
    intensity = all_labels[label]["intensity"]
    #print(timing, intensity)
    #new_labels.append([timing / recording_time , intensity / 10])
    labels[label] = pain
    
print(f"Labels : {labels.shape}")


#------- CREATE SPECTROGRAMS FROM EEG DATA ------------
frequencies_spec = 0
times_spec = 0
spectrograms = np.zeros((len(data), channels, 65, 11))
for sample in range(0):#len(data)):
    print(f"Creating spectrogram for sample : {sample}")
    timing = labels[sample][0]
    intensity = labels[sample][1]
    for channel in range(len(data[sample])):
        #print(f"Channel : {channel}")
        
        time_series = data[sample][channel].copy()#the signal 
        num_points = len(time_series)#amount of points in this signal
        sample_rate = num_points / recording_time #sample rate of the signal
        
        #------ SPECTROGRAM --------
        window_size = 128
        hop_length = 64
        frequencies, times, spectrogram = stft(time_series, window='hamming', nperseg=window_size, noverlap=window_size-hop_length, fs=sample_rate)
        spectrograms[sample][channel] = spectrogram# set the spectrogram
        
        t = np.linspace(0, recording_time, num_points)
         #--- ORIGINAL TIME SERIES ------
        if sample != -1:
            continue
        if channel != -1:
            continue
        plt.subplot(2, 1, 1)
        plt.plot(t, time_series)
        plt.xlabel('Time')
        plt.ylabel('Amplitude')
        plt.title('Original Signal')
        plt.subplot(2,1,2)
        plt.pcolormesh(times, frequencies, np.abs(spectrogram), shading='auto')
        plt.colorbar()
        plt.xlabel('Time')
        plt.ylabel('Frequency')
        plt.title(f'Spectrogram - Timing : {timing} - Intensity : {intensity}')
        plt.show()

spectrograms_array = spectrograms
print(f"Spectrograms : {spectrograms_array.shape}")
for spectrogram in range(0):#len(spectrograms_array)):
    for channel in range(len(spectrograms_array[spectrogram])):
        if spectrogram != -1:
            continue
        if channel != -1:
            continue
        spec = spectrograms_array[spectrogram][channel]
        #print(f"{spec.shape}")
        plt.pcolormesh(spec[1], spec[0], np.abs(spec[2]) , shading='auto')
        plt.show()

#----- MACHINE LEARNING ------

# Preprocess the data
#expanded_data = np.expand_dims(data, axis=-1)
#data = data / 255.0  # Normalizing between 0 and 1
#print(f"Expanded data : {expanded_data.shape}")

#slice up data into training and validation
x_train, x_val, y_train, y_val = train_test_split(data, labels, test_size=0.2, random_state=42)
# Data normalization
x_train = x_train.reshape(-1, 16, 625)
x_val = x_val.reshape(-1, 16, 625)

x_train /= np.max(x_train)
x_val /= np.max(x_val)


batch_size = 128
epochs = 30

model = Sequential()


model.add(Conv1D(256, (2), input_shape=x_train.shape[1:]))
model.add(Activation('relu'))

model.add(Conv1D(256, (2)))
model.add(Activation('relu'))
model.add(MaxPooling1D(pool_size=(2)))

model.add(Conv1D(124, (2)))
model.add(Activation('relu'))
model.add(MaxPooling1D(pool_size=(2)))

model.add(Conv1D(64, (1)))
model.add(Activation('relu'))
model.add(MaxPooling1D(pool_size=(2)))
model.add(Flatten())

model.add(Dense(512, activation='relu'))
model.add(Dense(256, activation='relu'))
model.add(Dense(1, activation='sigmoid'))
model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])
# Train the model


model.fit(x_train, y_train, validation_data=(x_val, y_val), batch_size=batch_size, epochs=epochs)
# Evaluate the model on the validation data
loss, accuracy = model.evaluate(x_val, y_val, batch_size=batch_size)

print("Validation Loss: {:.4f}".format(loss))
print("Validation Accuracy: {:.2f}%".format(accuracy * 100))

#----- SAVE TF MODEL -----------
save_model = True
overwrite_model = True
if save_model:
    model_file_name = "pain_calibrated_model.tf"
    model_file_path = os.path.join(path, model_file_name)
    model.save(model_file_path, overwrite=overwrite_model)

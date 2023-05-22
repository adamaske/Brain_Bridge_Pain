import random
import numpy as np
import time
import os
import pathlib#paths and files
import matplotlib.pyplot as plt
import json
from scipy.signal import stft 


#THIS SCRIPT LOADS EEG DATA THAT HAS BEEN IMPOSED WITH PAIN AND TRAINS A CNN WITH IT
channels = 16
recording_time = 5
sample_rate = 250

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
    
#------ CREATE NUMPY ARRAY FROM LABELS -------------
new_labels = []
for label in range(len(all_labels)): # CONVERT THE JSON OBJECTS INTO A USEABLE NUMPY ARRAY
    timing = all_labels[label]["timing"]
    intensity = all_labels[label]["intensity"]
    #print(timing, intensity)
    new_labels.append([timing, intensity])
    
labels = np.array(new_labels)#usable labels
print(f"Labels : {labels.shape}")

frequencies_spec = 0
times_spec = 0
spectrograms = np.zeros((len(data), channels, 65, 21))
#------- CREATE SPECTROGRAMS FROM EEG DATA ------------
for sample in range(len(data)):
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
for spectrogram in range(len(spectrograms_array)):
    for channel in range(len(spectrograms_array[spectrogram])):
        if spectrogram != -1:
            continue
        if channel != -1:
            continue
        spec = spectrograms_array[spectrogram][channel]
        #print(f"{spec.shape}")
        plt.pcolormesh(spec[1], spec[0], np.abs(spec[2]) , shading='auto')
        plt.show()

import tensorflow as tf
from sklearn.model_selection import train_test_split

# Preprocess the data
expanded_data = data#np.expand_dims(data, axis=-1)
#data = data / 255.0  # Normalizing between 0 and 1
print(f"Expanded data : {expanded_data.shape}")

# Split the data into training and validation sets
validation_split = 0.2  # 20% for validation
num_validation_samples = int(validation_split * expanded_data.shape[0])
train_data = expanded_data[:-num_validation_samples]
train_labels = labels[:-num_validation_samples]
val_data = expanded_data[-num_validation_samples:]
val_labels = labels[-num_validation_samples:]

# Create the TensorFlow model
model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(16, 1250)),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(2, activation='linear')
])

# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])

# Train the model
batch_size = 16
epochs = 10
model.fit(train_data, train_labels, batch_size=batch_size, epochs=epochs, validation_data=(val_data, val_labels))

# Evaluate the model on the validation set
val_loss, val_mae = model.evaluate(val_data, val_labels)

# Print the evaluation results
print("Validation Loss:", val_loss)
print("Validation Mean Absolute Error:", val_mae)
# Assuming you have the trained model and new data ready for prediction
new_data = data[:2]  # Shape: (samples, channels, time_steps)

# Preprocess the new data (similar to the preprocessing for training)
new_data = np.expand_dims(new_data, axis=-1)


# Make predictions using the trained model
predictions = model.predict(new_data)

# Print the predictions
print(predictions)

#----- SAVE TF MODEL -----------
save_model = False
overwrite_model = True
if save_model:
    model_file_name = "pain_calibrated_model.tf"
    model_file_path = os.path.join(path, model_file_name)
    model.save(model_file_path, overwrite=overwrite_model)

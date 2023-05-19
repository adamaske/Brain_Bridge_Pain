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

#------- CREATE SPECTROGRAMS FROM EEG DATA ------------
for sample in range(0):
    for channel in range(len(data[sample])):
        signal = data[sample][channel]#the signal 
        num_points = len(data[sample][channel])#amount of points in this signal
        sample_rate = num_points / recording_time #sample rate of the signal
        
        #------ FOURIER TRANSFROM ------- #
        fft_data = np.fft.rfft(data[sample][channel])#FFT on the signal
        
        magnitude_spectrum = np.abs(fft_data)#the mangitudes of amplitudes for component frequencies
        magnitude_spectrum = magnitude_spectrum / num_points#normalize the amplutides
        
        phase_spectrum = np.angle(fft_data)#phases
        
        fft_freqs = np.fft.rfftfreq(num_points, d=1/sample_rate)#get the frequencies

        target_freq = 5  # Frequency to reduce, 5hz
        target_index = np.argmin(np.abs(fft_freqs - target_freq))#find the index of this frequuecny
        
        
        # Modify the magnitude spectrum to reduce the contribution of the target frequency
        reduced_spectrum = magnitude_spectrum.copy()
        reduced_spectrum = reduced_spectrum * num_points#denormalize the signal
        reduced_spectrum[target_index] /= 5  #Change the target frequencies
        phase_spectrum[target_index] = 2#Change the phase at this point
                                        #IDK WHAT THIS IS SUPPOSED TO BE BUT 2 SEEMS TO WORK ????? 
       
        reduced_fft_data = reduced_spectrum * np.exp(1j * phase_spectrum)# Reconstruct the modified FFT coefficients
                                                                         #the phase changes when altering the signal, so
      
        reconstructed_signal = np.fft.irfft(reduced_fft_data)# Inverse FFT to reconstrut the original signal
        

        t = np.linspace(0, recording_time, num_points)#time dimension
        plt.plot(t, reconstructed_signal)
        
        plt.subplot(2, 1, 1)
        plt.plot(t, data[sample][channel])
        plt.xlabel('Time')
        plt.ylabel('Amplitude')
        plt.title('Original Signal')

        plt.subplot(2, 1, 2)
        plt.plot(t, reconstructed_signal)
        plt.xlabel('Time')
        plt.ylabel('Amplitude')
        plt.title('Reduced 5 Hz Contribution')

        plt.tight_layout()
        plt.show()
        exit()
        
        fig1, axis1 = plt.subplots(figsize=(8,6))
        axis1.plot(fft_freqs, magnitude_spectrum)
        axis1.set_xlabel('Frequency (Hz)')
        axis1.set_ylabel('Magnitude')
        axis1.set_title('Magnitude Spectrum')
        
        #----- SHORT TIME FOURIER TRANSFORM ----- #
        window_size = 512
        hop_length = 64
        frequencies, times, spectrogram = stft(data[sample][channel], window='hamming', nperseg=window_size, noverlap=window_size-hop_length, fs=sample_rate)
        
        fig2, axis2 = plt.subplots(figsize=(8,6))
        # Plot the spectrogram
        axis2.pcolormesh(times, frequencies, np.abs(spectrogram), shading='auto')
        #plt.colorbar(label='Magnitude')
        axis2.set_xlabel('Time')
        axis2.set_ylabel('Frequency')
        axis2.set_title('Spectrogram')
        plt.tight_layout()
        plt.show()
        exit()    
    
# Preprocess the data
expanded_data = np.expand_dims(data, axis=-1)
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
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(16, 1250, 1)),
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

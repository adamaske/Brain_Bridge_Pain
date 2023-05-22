import random
import numpy as np
import time
import os
import pathlib#paths and files
import matplotlib.pyplot as plt
import json
from scipy.signal import stft
from scipy.signal import istft
#import data set of normal EEG data
channels = 16
recording_time = 5
sample_rate = 250
pain_impose_amount = 10 #how many pain imposed signals to create
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
    loaded_data = np.load(file_path)
    print(f"Loaded data : {loaded_data.shape}")
    data = loaded_data
else:
    print(f"{file_name} does not exist, no data can be loaded!")
    exit()

#---------- IMPOSE PAIN ON SIGNAL --------------
#------ LOAD ARTIFACTS -------------
import pain_artifacts
all_artifacts = pain_artifacts.pain_artifacts

modified_signals = []
labels = []#Created labels
for sample in range(pain_impose_amount):#loop to create
    sample %= len(data)
    print(f"Sample : {sample}")
    pain = 1#random.randint(1,100)#pain or not
    timing = random.randint(1, recording_time-1)
    intensity = random.randint(1, 10)
    print()
    print(f"Timing : {timing}")
    print(f"Intesnity : {intensity}")

    #-----CHOOSE RANDOM ARTIFACT -----------
    artifact_index = random.randrange(0, len(all_artifacts))#get a random index
    artifact = all_artifacts[artifact_index]#gets the artifact
    name, band_ranges, affected_channels, effect = pain_artifacts.ParseArtifact(artifact_index)#parse the artifact
    print(f"Choosen artifact : {name}")
    #----- APPLY ------
    for pa_channel in affected_channels:
        channel = pa_channel#Channel index that will be affected
        #----- UNMODIFIED ------
        time_series = data[sample][channel].copy()#get the time series at this channel
        num_samples = len(time_series)#length of time series
        sample_rate = num_samples / recording_time#how many samples per second is this recording for
        
        fft_data = np.fft.rfft(time_series)#get freqeuency spectrum from time series
        
        unmodified_magnitude_spectrum = np.abs(fft_data)#get the magnitudes
        unmodified_normalized_magnitude_spectrum = unmodified_magnitude_spectrum / len(time_series)#normalize them to get correct amplitude

        unmodified_fft_freqs = np.fft.rfftfreq(num_samples, d=1/sample_rate)#get the frequencies
        
        window_size = 128
        hop_length = 64
        original_frequencies, original_times, original_spectrogram = stft(time_series, window='hamming', nperseg=window_size, noverlap=window_size-hop_length, fs=sample_rate)
        
        #---- MODIFYING THE SPECTROGRAM ------
        at_time = int((timing / np.max(original_times)) * len(original_times))
        modified_spectrogram = original_spectrogram.copy()
        for band_range in band_ranges:
            from_freq = int((band_range[0] / np.max(original_frequencies)) * len(original_frequencies))
            to_freq = int((band_range[1] / np.max(original_frequencies)) * len(original_frequencies))
            modified_spectrogram[from_freq:to_freq, at_time] += effect * intensity
            
        #REMAKE THE SIGNAL FROM THE MODIFIED SPECTROGRAM
        reconstructed_time, reconstructed_time_series = istft(modified_spectrogram, window='hamming', nperseg=window_size, noverlap=window_size-hop_length, fs=sample_rate)
        difference_in_signal_length = len(reconstructed_time_series) - num_samples#the reconstruced signal gets some extras because of float inaccuracy I think
        reconstructed_time_series = reconstructed_time_series[:-difference_in_signal_length]#remove extras
        reconstructed_time = reconstructed_time[:-difference_in_signal_length]#remove extras
        
        modified_fft_data = np.fft.rfft(reconstructed_time_series)#FFT on the reconstructed signal
        modified_magnitude_spectrum = np.abs(modified_fft_data)#get the magnitudes
        modified_normalized_magnitude_spectrum = modified_magnitude_spectrum / len(reconstructed_time_series)#normalize them to get correct amplitude
        
        modified_fft_freqs = np.fft.rfftfreq(len(reconstructed_time_series), d=1/sample_rate)#should be the same, but just in case
        #reconstructed the time series
        modified_frequencies, modified_times, modified_spectrogram = stft(reconstructed_time_series, window='hamming', nperseg=window_size, noverlap=window_size-hop_length, fs=sample_rate)
       
        
        # Plot the spectrogram
        if True:
            t = np.linspace(0, recording_time, num_samples)#time dimension

            #--- ORIGINAL TIME SERIES ------
            plt.subplot(2, 3, 1)
            plt.plot(t, time_series)
            plt.xlabel('Time')
            plt.ylabel('Amplitude')
            plt.title('Original Signal')
            #-----  ORIGINAL FFT ------
            plt.subplot(2, 3, 2)
            plt.plot(unmodified_fft_freqs, unmodified_normalized_magnitude_spectrum)
            plt.xlabel('Frequency')
            plt.ylabel('Amplitude')
            plt.title('Unmodified FFT')
            #------ ORIGINAL SPECTROGRAM
            plt.subplot(2, 3, 3)
            plt.pcolormesh(original_times, original_frequencies, np.abs(original_spectrogram), shading='auto')
            plt.colorbar()
            plt.xlabel('Time')
            plt.ylabel('Frequency')
            plt.title('Unmodified Spectrogram')
            #------ MODIFINED TIME SERIES -------
            plt.subplot(2, 3, 4)
            plt.plot(reconstructed_time, reconstructed_time_series)
            plt.xlabel('Time')
            plt.ylabel('Amplitude')
            plt.title('Reconstructed Signal')
            plt.subplot(2, 3, 5)
            #------ MODFIFED FFT -------
            plt.plot(modified_fft_freqs, modified_normalized_magnitude_spectrum)
            plt.xlabel('Amplitude')
            plt.ylabel('Frequency')
            plt.title('Modified FFT')
            #------- MODIFIED SPECTROGRAM -------
            plt.subplot(2, 3, 6)
            plt.pcolormesh(modified_times, modified_frequencies, np.abs(modified_spectrogram), shading='auto')
            plt.colorbar()
            plt.xlabel('Time')
            plt.ylabel('Frequency')
            plt.title('Modified Spectrogram')
            plt.tight_layout()
            plt.show()
            
            
        
        #------ OVERWRITE OLD TIME SERIES WITH NEW -------
        data[sample][channel] = reconstructed_time_series#overwrite the previous data with the new data
        modified_signals.append(reconstructed_time_series)
    #---- CREATE LABEL ------
    obj = {
        "pain" : pain,
        "timing" : timing,
        "intensity" : intensity
    }
    labels.append(obj)#add label to labels

if True:
    modified_signals = np.array(modified_signals)
    for sig in range(0,2):
        t = np.linspace(0, recording_time, len(modified_signals[sig]))
        plt.plot(t, modified_signals[sig])
        plt.show()
    
#------- SAVE THE IMPOSED DATA -----------------

#----FILE PATHS---------
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
        
#------- SAVE JSON LABELS ---------------
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






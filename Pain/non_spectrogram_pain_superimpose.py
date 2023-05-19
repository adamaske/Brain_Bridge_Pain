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

name, band_ranges, effected_channels, effect = pain_artifacts.ParseArtifact(0) 
print(name, band_ranges, effected_channels, effect)

labels = []#Created labels
for sample in range(len(data)):#loop to create
    pain = 1#random.randint(1,100)#pain or not
    timing = random.randint(1, recording_time-1)
    intensity = random.randint(1, 10)
    
    #-----CHOOSE RANDOM ARTIFACT -----------
    artifact_index = random.randrange(0, len(all_artifacts))#get a random index
    artifact = all_artifacts[artifact_index]#gets the artifact
    name, band_ranges, affected_channels, effect = pain_artifacts.ParseArtifact(artifact_index)#parse the artifact
    print(f"Choosen artifact : {name}")
    #----- APPLY ------
    for pa_channel in affected_channels:
        channel = pa_channel#Channel index that will be affected
        
        time_series = data[sample][channel].copy()#get the time series at this channel
        num_samples = len(time_series)#length of time series
        sample_rate = num_samples / recording_time#how many samples per second is this recording for
        
        fft_data = np.fft.rfft(time_series)#get freqeuency spectrum from time series
        
        magnitude_spectrum = np.abs(fft_data)#get the magnitudes
        normalized_magnitude_spectrum = magnitude_spectrum / len(time_series)#normalize them to get correct amplitude
        unmodified_mangitude_spectrum = normalized_magnitude_spectrum.copy()#copy for testing
        phase_spectrum = np.angle(fft_data)#phases
        
        fft_freqs = np.fft.rfftfreq(num_samples, d=1/sample_rate)#get the frequencies

        for band_range in band_ranges:#go trough every band range this artifact affects
            start_frequency = band_range[0]#where does this band range start
            end_frequency = band_range[1]#where does it end
            
            for frequency in range(start_frequency, end_frequency):
                target_index = np.argmin(np.abs(fft_freqs - frequency))#index of the frequency
                
                #multiplier = (len(band_range) - frequency)#change based on how far into the frequencies we are, the goal is a Guassian filter
                change = effect * intensity#*multiplier#This change is effect * intensity, if effect is 1 and intensity is 10, then 8, then it will incrase 8
                
                normalized_magnitude_spectrum[target_index] += change#change the amplutides in the frequency domain
                
                phase_spectrum[target_index] *= 1#?????????#Change the phase at this point
                                        #IDK WHAT THIS IS SUPPOSED TO BE BUT 2 SEEMS TO WORK ????? 
       
        
        # Modify the magnitude spectrum to reduce the contribution of the target frequency
        unnormalized_magnitude_spectrum = normalized_magnitude_spectrum * num_samples
        
        modified_fft_data = unnormalized_magnitude_spectrum * np.exp(1j * phase_spectrum)# Reconstruct the modified FFT coefficients
                                                                         #the phase changes when altering the signal, so
      
        reconstructed_time_series = np.fft.irfft(modified_fft_data)# Inverse FFT to reconstrut the original signal
        
        if True:
            t = np.linspace(0, recording_time, num_samples)#time dimension

            #--- ORIGINAL TIME SERIES ------
            plt.subplot(2, 2, 1)
            plt.plot(t, time_series)
            plt.xlabel('Time')
            plt.ylabel('Amplitude')
            plt.title('Original Signal')
            #-----  ORIGINAL FFT ------
            plt.subplot(2, 2, 2)
            plt.plot(fft_freqs, unmodified_mangitude_spectrum)
            plt.xlabel('Amplitude')
            plt.ylabel('Frequency')
            plt.title('Unmodified FFT')
            #------ MODIFINED TIME SERIES -------
            plt.subplot(2, 2, 3)
            plt.plot(t, reconstructed_time_series)
            plt.xlabel('Time')
            plt.ylabel('Amplitude')
            plt.title('Reduced 5 Hz Contribution')
            plt.subplot(2, 2, 4)
            #------ MODFIFED FFT -------
            plt.plot(fft_freqs, normalized_magnitude_spectrum)
            plt.xlabel('Amplitude')
            plt.ylabel('Frequency')
            plt.title('Unmodified FFT')

            plt.tight_layout()
            plt.show()
            exit()
        data[sample][channel] = modified#overwrite the previous data with the new data
    #---- CREATE LABEL ------
    obj = {
        "pain" : pain,
        "timing" : timing,
        "intensity" : intensity
    }
    labels.append(obj)#add label to labels
    print(f"Making sample {sample:.1f}", end='\r')
print(f"Length of labels {len(labels)}")

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






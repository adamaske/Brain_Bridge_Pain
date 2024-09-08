from pylsl import resolve_stream#networking
from pylsl import StreamInlet

from scipy import signal#math
import numpy as np

import matplotlib.pyplot as plt#visuals

import os#files
import time#time
import json#files
import pathlib#paths and files
from threading import Thread#custom thread class

#--
recording_time = 5
class CustomRecordingThread(Thread):
    def __init__(self, *args): #args for what inlet to use
        Thread.__init__(self)
        self.value = None #delcare value
        self.args = args #store args
    def run(self):
        inlet = self.args[0] #get argument
        target = self.args[1] #fucntion to run
        self.value = target(inlet) #record
        
def Record_FFT(inlet):
    print('FFT Recording Running')
    channels = 16
    local_sample_rate = inlet.info().nominal_srate()
    num_samples = int(recording_time * local_sample_rate)  
    
    print(f"FFT Channels : {channels:.1f}")
    print(f"FFT Recording Time : {recording_time:.1f}")
    print(f"FFT Sample Rate : {local_sample_rate:.1f}")
    print(f"FFT Sample Amount : {num_samples:.1f}") 
    
    start_time = time.time()#cache the time
    
    recorded_data = [[] for i in range(channels)]#Cache the incoming data
    
    for data_point in range(int(recording_time * local_sample_rate)):#
        raw_data, timestamp = inlet.pull_sample()#for raw data, this should fire 16 data points 250 times per second
        
        for channel in range(len(raw_data)):#for each channel
            recorded_data[channel].append(raw_data[channel])#add each channel to the recording
    
    recording_duration = time.time() - start_time#How long did the recording last ? 
    print(f"Recorded for {recording_duration:.1f} seconds!")
    
    recorded_data = np.array(recorded_data)#make to numpy array
    print(f"FFT data : {recorded_data.shape}")
    
    fft_data = np.array(recorded_data)
    return fft_data

def Record_Raw(inlet):
    print('RAW Recording Running')
    channels = 16
    
    local_sample_rate = inlet.info().nominal_srate()
    num_samples = int(recording_time * local_sample_rate)  
    
    print(f"RAW Channels : {channels:.1f}")
    print(f"RAW Recording Time : {recording_time:.1f}")
    print(f"RAW Sample Rate : {local_sample_rate:.1f}")
    print(f"RAW Sample Amount : {num_samples:.1f}") 
    
    start_time = time.time()#cache the time
    
    recorded_data = [[] for i in range(channels)]#Cache the incoming data
    
    for data_point in range(int(recording_time * local_sample_rate)):#
        raw_data, timestamp = inlet.pull_sample()#for raw data, this should fire 16 data points 250 times per second
        
        for channel in range(len(raw_data)):#for each channel
            recorded_data[channel].append(raw_data[channel])#add each channel to the recording
    
    recording_duration = time.time() - start_time#How long did the recording last ? 
    print(f"Recorded for {recording_duration:.1f} seconds!")
    
    recorded_data = np.array(recorded_data)#make to numpy array
    print(f"RAW data : {recorded_data.shape}")
    
    raw_data = np.array(recorded_data)
    return raw_data
   
def Keep_Or_Discard_Recording():
    keep = str(input("Keep or discard this recording? [ K / D ]"))
    if keep.lower() == 'k':
        return 1
    elif keep.lower() == 'd':
        return 0
    else:
        print('Not recognized answer!')
        return Keep_Or_Discard_Recording()

print('Connecting to LSL stream!')
fft_inlet = StreamInlet(resolve_stream('type', 'FFT')[0])
fft_thread = CustomRecordingThread(fft_inlet, Record_FFT)#init threads
print('FFT Stream Connected')

raw_inlet = StreamInlet(resolve_stream('type', 'RAW')[0])
raw_thread = CustomRecordingThread(raw_inlet, Record_Raw)
print('RAW Stream Connected')
 
fft_thread.start()#start both threads
raw_thread.start()

fft_thread.join()#wait for threads to complete
raw_thread.join()

fft_data = fft_thread.value#obtain values from functions they ran
raw_data = raw_thread.value

print(f"FFT Data is a {fft_data.shape} array")
fft_channels = len(fft_data)
fft_data_points_amount = len(fft_data[0])
print(f"FFT Data is a {fft_channels}x{fft_data_points_amount} array")

raw_channels = len(raw_data)
raw_data_points_amount = len(raw_data[0])
print(f"RAW Data is a {raw_channels}x{raw_data_points_amount} array")

pain = 0#did pain happend during this recording ? 1 = yes, 0 = no
timing = 0#when did the pain happend
intensity = 0#how intense was the pain
keep = 0#keep this recording or not ? 1 = yes, 0 = no
if True:#do saving and such, skip for testing
    pain = int(input("Did pain happend during this recording? [ 1 / 0 ]"))
    if pain == 1:
        timing = input("At what second (0-5) did the pain occur?")#prompt user for when pain occured
        intensity = input("How intense was the pain (0-10)?")#prompt user for intensity
    keep = Keep_Or_Discard_Recording()

if keep == 0:#Exit if we dont keep the file
    exit()
    
user = "Adam"#what person just recorded this
recording_count = 0#start at 0
file_prefix = "pain_recording_"#file name 
file_suffix = ".json"#suffix to look for when looking for existing files

current_dir = pathlib.Path(__file__).parent#get current folder
path = os.path.join(current_dir, "Datasets", user)#get directory to save recording
if not os.path.exists(path):#if there is no folder for this user, then create one
    os.makedirs(path)
    
file_path = os.path.join(path, file_prefix + user + "_" + str(recording_count) + file_suffix)#while this file is found, iterate counter
while os.path.isfile(file_path):#find how many recording files there are
    recording_count = recording_count + 1#iterate counter because the file with this index exists
    file_path = os.path.join(path, file_prefix + user + "_" + str(recording_count) + file_suffix)#setnew file path

index = str(recording_count)
print(f"Saving files with index {index} at {path}!")

data = {#Json object for saving the data in this recording
    "name" : user,
    "pain" : pain,
    "timing" : timing,
    "intensity" : intensity
}
json_file_name = file_prefix + user + "_" + index + ".json"
json_file_path = os.path.join(path, json_file_name)
with open(json_file_path, "w") as file:#open file
    json.dump(data, file)#fill file with data object
print(f"JSON File saved : {json_file_name}")


file_suffix = ".npy"#now saving numpy arrays
#fft data saving
fft_prefix = "pain_recoding_fft_"
fft_file_name = fft_prefix + index + file_suffix
fft_file_path = os.path.join(path, fft_file_name) 
np.save(fft_file_path, fft_data)
print(f"Saved FFT data : {fft_file_name}!")

#raw data saving 
raw_prefix = "pain_recoding_raw_"
raw_file_name = raw_prefix + index + file_suffix
raw_file_path = os.path.join(path, raw_file_name)  
np.save(raw_file_path, raw_data)#save raw to file
print(f"Saved RAW data : {raw_file_name}!")

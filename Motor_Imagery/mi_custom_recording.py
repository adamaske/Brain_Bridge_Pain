from pylsl import resolve_stream
from pylsl import StreamInlet
import numpy as np
import time
import pathlib
import os
import random
from threading import Thread#custom thread class

#---- GLOBAL -------
channels = 16
recording_time = 5

markers = ['left', 'right']#, 'up', 'down', 'forward', 'backward'] #The marker being sent, this must correspond with targets in NeuroPype Pipline(found in "assign targets" module)
box_directions = [[-1, 0, 0], [1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]#What x direction does the box move per label

                                                             #If not the ML will learn the temporal features
def ChooseRandomClass():#function for choosing a random label
    return random.randrange(0, 100) % len(markers) #Is this a left or right trail? Left and Right trials must be in a random order for machine learning. 
   
def LabelingAndVisuals():
    warmup_trials = 5 #Amount of warmup trails. A warmup trial does not count in calibartion
    trials_per_class = 5 #Amount of trials per class (left / right) 
    cue_time = 0.5
    perform_time = 3.5 #How long does one trial last, in seconds
    wait_time = 0.5 #How long to wait between each trial
    pause_every = 100 #After x trails, give the user a break
    pause_duration = 15 #How long the trail last
    
    labels = []
    calibration_start_time = time.time()
    
    for trial in range(1, warmup_trials + int(trials_per_class * len(markers))+1):#loop of each trial
        print(f"Starting tiral {trial}")
        #Make choice before trial starts so that we can display next choice in waiting period
        choice = ChooseRandomClass() 
        label = markers[choice]#get the label
        direction = box_directions[choice]#get the direction
        print(f"This trial is for {label.capitalize()}!")
        print(f"The box will move {direction}!")
        
        trial_start_time = time.time() - calibration_start_time
        
        print(f"Trial started at {trial_start_time} of the calibration!")
        labels.append((choice, time.time() - calibration_start_time))

        
        
        
        if trial < warmup_trials:# is this a warmup ?
            print("This is a warmpup trial!")
        
        if trial == warmup_trials:#this is the last warmup
            print('This is the last warmup trial!')
        
        if trial > warmup_trials:#proper trial
            print('This is a proper trial!')
        
        #when do we send the que, 
       
        cue_start_time = time.time()
        while time.time() - cue_start_time < cue_time:
            print('CUE')
        
        perform_start_time = time.time()
        while time.time() - perform_start_time < perform_time:
            print("MI")
            
        wait_start_time = time.time()
        while time.time() - wait_start_time < wait_time:
            print("PAUSE")
            
            
    print('Trials complete!')
    
    label_data = np.array(labels)#this results (0, 0.456234), (1, 0.99993) (0, 4.5) etc, the chocie with a time stamp 
        

  
    
    
class CustomLabelingThread(Thread):
    def __init__(self, *args):
        Thread.__init__(self)
        self.value = None
    def run(self):
        self.value = LabelingAndVisuals()
        
        
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

print('Connecting to LSL stream!')#
print('Waiting for FFT connection!')
fft_inlet = StreamInlet(resolve_stream('type', 'FFT')[0])#resolve FFT type stream
fft_thread = CustomRecordingThread(fft_inlet, Record_FFT)#init threads
print('FFT Stream Connected')

print('Waiting for RAW connection!')
raw_inlet = StreamInlet(resolve_stream('type', 'RAW')[0])#resolve the RAW - time series stream
raw_thread = CustomRecordingThread(raw_inlet, Record_Raw)
print('RAW Stream Connected')

label_thread = CustomLabelingThread()


fft_thread.start()#Run recordings
raw_thread.start()

print('Recordings finished!')

#--- RECORDINGS ARE GOING UNTIL .JOIN-----
#how do we label the data ? 


fft_thread.join()#wait for threads to complete
raw_thread.join()

fft_data = fft_thread.value#obtain values from functions they ran
raw_data = raw_thread.value

#---- SAVE DATA TO FILE ------
file_index = 0

user = "Adam"
current_dir = pathlib.Path(__file__).parent#get current folder
path = os.path.join(current_dir, "Recordings", user)#get directory to save recording

raw_file_name = "raw_mi_data_" + file_index + ".npy"
raw_file_path = os.path.join(path, raw_file_name)#file path

fft_file_name = "fft_mi_data_" + file_index + ".npy"
fft_file_path = os.path.join(path, fft_file_name)

labels_file_name = "labels_mi_data_" + file_index + ".npy"
labels_file_path = os.path.join(path, labels_file_name)






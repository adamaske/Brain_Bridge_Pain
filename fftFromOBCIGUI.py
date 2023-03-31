import matplotlib.pyplot as plt

import pylsl as lsl
from pylsl import resolve_stream
from pylsl import StreamInlet

print("Waiting for FFT stream")
#The lsl is sent with type EEG, this can be changed in the openBCI gui
streams = resolve_stream('type', 'EEG')
#we're only sending eeg data at this time so we grab that
#we can send everything over this same stream, then just grab other elements from the stream
inlet  = StreamInlet(streams[0])
channel_data = {} #array with 16 arrays which store each datapoint over the time
#when using daisy we're getting 16 channels of 125 datapoints each frame
while(1):
    for i in range(16):
        #grabs the data and timestep
        sample, timestep = inlet.pull_sample()
        if i not in channel_data: #is there an element to put this in
            channel_data[i] = sample #the i'th channel of channel data's 0th element is sample
        else: #no, then make one
            channel_data[i].append(sample) #the i'th channel gets an additional element, sample

    for channel in channel_data: 
        #each element in channel data is an array of floats, so each of these elemtns are plotted, easy
        #info above 62.5hz is uselesss garbage because 125 hz is the sampling rate
        plt.plot(channel_data[channel][:60]) 
    plt.show() 
        
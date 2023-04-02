import pylsl as lsl
from pylsl import resolve_stream
from pylsl import StreamInlet 
import numpy as np
import os

array = np.array([])

array = np.append(array, 1)
print(array)
#def User_label_index_filename(user, label, index, suffix):
#    filename =  user+'_'+label+'_'+str(index)+suffix
#    filename = filename.lower()
#    return filename
#directory = 'C:/Datasets'
#user = 'Adam'
#label = 'right'
#index = 0
#directory = 'C:/Datasets'
#foldername = user.lower()
#folder = os.path.join(directory, foldername)
#if os.path.exists(folder):
#    print(folder, 'exists!')#  
#    file = User_label_index_filename(user, label, index, '.npy')
#    k = os.path.join(folder, file)
#    while os.path.isfile(k):
#        print('Found', index)
#        index +=1 
#       
#        k = os.path.join(folder,  User_label_index_filename(user, label, index,'.npy'))
#    data = [[0.123,322]]
#    np.save(k, data)
        
        
            
#inlet = lsl.StreamInlet(lsl.resolve_stream('type', 'EEG')[0])
#channels = 16 #how many channels are we reciving, chagne to 8 if not using Daisy
#recording_time = 5 #how many seconds do we want to record for ? 
#sample_rate = inlet.info().nominal_srate() #how many datapoints do we get each second ?
#num_samples = int(2) #How many samples will record ? 
#data = []
#for i in range(num_samples): #we have decided how many samples we wil get, so from 
#    sample, timestamp = inlet.pull_sample() 
#    fft = sample[:channels]
#    data.append(fft)
#
#for i in range(len(data)):
#    for channel in range(channels):
#        print(i, channel, data[i][channel])
#
#np.save('Adam_right.npy', data)
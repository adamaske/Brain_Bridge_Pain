import pylsl as lsl
from pylsl import resolve_stream
from pylsl import StreamInlet
import numpy as np
import time
import pickle
import os



def Connect(): #this function connects us to the lsl stream
    print('Connecting to LSL stream!')
    inlet = lsl.StreamInlet(lsl.resolve_stream('type', 'EEG')[0])
    print('Connected!')

    return inlet

def Info(): #we need info about this recording
    user = input('Who is training? : ')
    label = input('What command are you training for? : ')
    return user, label
    
def Pre_Recording(): #before the recording starts
    countdown = input('How many seconds of countdown do you want? : ')
    countdown = int(countdown)

    print('Input "Start/1" to start countdown. Input "Return/0" to terminate. ')
    response = input('Start/Return : ') #chance to cancel the recording

    if response.lower() == 'start' or response == '1':
        print('Starting Countdown!')
    else:
        print('Terminating operation!')
        return False

    for i in range(countdown, 0, -1):
        print(i) 
        time.sleep(1)

    print('Countdown Complete!')
    return True

def Record(inlet): #
    print('Recording Started with Inlet!')
    channels = 16 #how many channels are we reciving, chagne to 8 if not using Daisy
    recording_time = 5 #how many seconds do we want to record for ? 
    sample_rate = inlet.info().nominal_srate() #how many datapoints do we get each second ?
    num_samples = int(recording_time * sample_rate) #How many samples will record ? 
    data = np.empty((num_samples, channels))
    print('Sample_rate', sample_rate, ' - Num_Samples', num_samples)

    for i in range(num_samples): #we have decided how many samples we wil get, so from 
        sample, timestamp = inlet.pull_sample() 
        fft = sample[:channels]
        data[i] = fft
        remaining_time = recording_time - (i+1)/sample_rate
        print(f"Remaining recording time: {remaining_time:.1f} seconds", end='\r')#display how much time is left
        time.sleep(1 / sample_rate)#the script runs insanly much faster than the sample_rate, so we wait
    return data

#def Record(): #for testing 
#    print('Recording Started without Inlet!')
#    data = np.array([])
#    num_arrays = 5  # specify the number of arrays you want
#    num_channels = 16  # specify the number of channels per array
#
#    my_array = np.zeros((num_arrays, num_channels))  # create the array
#    for i in range(num_arrays):
#        for channel in range(num_channels):
#            my_array[i][channel] = 1
#    print(my_array)
#    return data

def User_label_index_filename(user, label, index, suffix):
    filename =  user+'_'+label+'_'+str(index)+suffix
    filename = filename.lower()
    return filename

def Save(user, label, data):
    directory = 'C:/Datasets' #folder where datasets are saved
    folder = os.path.join(directory, user.lower())#create path from these
    if not os.path.exists(folder): #check if the folder exists
        os.mkdir(folder) #if not, make one
    #we must find how many files there are of this type, each is idnexed
    index = 0 #start at 0th index
    file = os.path.join(folder, User_label_index_filename(user, label, index, '.npy'))#start at user_label_0
    while os.path.isfile(file):#is there a file here
        index = index + 1#iterate index
        file = os.path.join(folder, User_label_index_filename(user, label, index, '.npy'))#set new filepath with new index
    np.save(file, data)#the file location, then data. it doesnt matter if the filename contains .npy at the end
    return True

if __name__ == '__main__':
    skip_connection = False
    if skip_connection:
        print('No Connection Needed for this session')
    else:
        inlet = Connect() #we want to make sure we're connected to the lsl stream before the rest
    user, label = Info() #ask the user for name and what command we're about to train
    record = Pre_Recording() #ask for and the exectue countdown
    data = [] #to store the data recorded
    if record: #if the user terminated the we dont record
        if skip_connection:
            #data = Record()
            print('Skipped Recording!')
        else:
            data = Record(inlet) #this start recording 
    else:
        print('Not Recording!') 
    saved = Save(user, label, data)
    if saved:
        print('Training Saved!')  
    
       
    print('Exiting!') #exit program

   
    
import numpy as np
import os
import tensorflow as tf
from tensorflow     import keras
from keras.models   import Sequential
from keras.layers   import Dense, Dropout, Activation, Flatten, Conv2D, Conv1D, MaxPooling2D

user = 'Adam'
labels = ['right', 'left']

def Filter_Channels(all_fft):#this functions removes the channels which are not used for Motor Imagery
    print('Filtering Channels')
    print('Amount of FFTs - ', len(all_fft))
    all_channels = len(all_fft[0][0])
    print('Each FFT has', all_channels, ' channels' )
    motor_cortex_channels = np.array([3, 4, 5, 11,12,13])#channels used for Mi
    print('The MotorCortex channels -', motor_cortex_channels)
    
    new_ffts = np.array((0, len(motor_cortex_channels)))#we're gonna have all new ffts, without the other channels
    for fft in range(len(all_fft)): #go trough every fft 
        
        new_fft = np.array(0) #a new fft
        for fft_channel in range(len(motor_cortex_channels)):
            new_fft = np.append(new_fft, all_fft[fft][motor_cortex_channels[fft_channel]])
        new_ffts = np.append(new_ffts, new_fft)   
        
    print('Elements in new_ffts - ', len(new_ffts))
    #print('Elements in new_ffts[0] - ', len(new_ffts[0]))
    #print('Elements in new_ffts[0][0] - ', len(new_ffts[0][0]))
    #print('Value    at new_ffts[0][0][0] - ', new_ffts[0][0][0])
    return new_ffts #return the new FFTs with removed channels
    
def User_label_index_filename(user, label, index, suffix):
    filename =  user+'_'+label+'_'+str(index)+suffix
    filename = filename.lower()
    return filename
def Load_Training_Data():
    
    directory = 'C:\\Datasets' #folder where datasets are saved
    folder = os.path.join(directory, user.lower())#path to this user's dir
    if not os.path.exists(folder): #does the folder exist ?
        print('No folder for this user exists!')#the folder doesnt exits, return
        return 0,0
    
    files_per_label = np.empty(0, dtype=int)#array to store how many files there is per label
    for label in labels: #we want to find all files for each label we're training for
        #we must find how many files there are of this type, each is indexed
        index = 0 #start at 0th index
        while True:#is there a file here
            file = os.path.join(folder, User_label_index_filename(user, label, index, '.npy'))#set new filepath with new index
            if os.path.isfile(file):
                 index = index + 1#next file, iterate index
            else:
                break #the file doesnt exits, so no more files to find of this label
        files_per_label = np.append( files_per_label, index)
        
    total_files = 0
    for file in range(len(files_per_label)):
        print('File Amount : ', files_per_label[file])  
        for index in range(files_per_label[file]):
            total_files = total_files + 1
    print('Total file amount -', total_files)
    
    #we now know how many files we need
    x = np.empty((total_files, 625, 16)) #we have 4 arrays with 625 datapoints for 16 channels
    y = np.array([]) #this array holds the label to each array
    
    for file in range(len(files_per_label)):
        #print('File Amount : ', files_per_label[file])  
        for index in range(files_per_label[file]):
            print('Reading index ', index, ' from file ', file)
            #print('User - ', user, ' label -', labels[file], 'index - ', index)

            data = np.load(os.path.join(folder, User_label_index_filename(user, labels[file], index, '.npy')))
            print('Info about file : ')
            print('Elements in data - ', len(data))
            print('Elements in data[0]', len(data[0]))

    return x,y
    
if __name__ == '__main__':
    x_train, y_train= Load_Training_Data() #train is the FFT data, y train is the label. If the 0th xtrain is a right command, then the 0th y_train is 'right'
    print('Elements in x_train - ', len(x_train))
    print('Elements in x_train[0] - ', len(x_train[0]))
    print('Elements in x_train[0][0] - ', len(x_train[0][0]))
    print('Value    at x_train[0][0][0] - ', x_train[0][0][0])
    t7 = np.zeros(len(x_train[0]))
    for fft in range(len(x_train[0])):
        t7[fft] = x_train[0][fft][2]
    print(t7)
    #print('Labels - ', y_train)
    #Filter_Channels(x_train)
    exit()
    
#motor_cortex_electrode_indices = np.array([0, 3,4,5,2])
#
#new_data = [] #array to save only motorcortex electrode data
#for i in range(len(motor_cortex_electrode_indices)): #filter out all the non-motor cortex electrodes
#    #new_data.append(motor_cortex_electrode_indices[i])
#    print(motor_cortex_electrode_indices[i])
#    if i not in new_data:
#        new_data[i] = motor_cortex_electrode_indices[i]
#    else:
#        new_data[i].append(motor_cortex_electrode_indices[i])
#    
#model = keras.models.Sequential([
#    Conv2D(32, (3,3), activation='relu', input_shape=(10,12, 1))
#    
#])

#we need a bunch of data to train the model on

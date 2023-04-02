import numpy as np
import os
import tensorflow as tf
from tensorflow     import keras
from keras.models   import Sequential
from keras.layers   import Dense, Dropout, Activation, Flatten, Conv2D, Conv1D, MaxPooling2D

user = 'Adam'
labels = ['right', 'left']

def Filter_Channels():#this functions removes the channels which are not used for Motor Imagery
    channels = 16
    motor_cortex_channels = np.array([3, 4, 5, 11,12,13])
    new_data = []
    for i in range(len(data)):
        for channel in range(len(motor_cortex_channels)):
            print(i, channel, data[i][channel])

    print(new_data)

def User_label_index_filename(user, label, index, suffix):
    filename =  user+'_'+label+'_'+str(index)+suffix
    filename = filename.lower()
    return filename
def Load_Training_Data():
    x = np.array([]) #this array holds arrays
    y = np.array([]) #this array holds the label to each array
    directory = 'C:/Datasets' #folder where datasets are saved
    folder = os.path.join(directory, user.lower())#path to this user's dir
    if not os.path.exists(folder): #does the folder exist ?
        print('No folder for this user exists!')#the folder doesnt exits, return
        return 0
    for label in labels: #we want to find all files for each label we're training for
        #we must find how many files there are of this type, each is indexed
        index = 0 #start at 0th index
        file = os.path.join(folder, User_label_index_filename(user, label, index, '.npy'))#start at user_label_0
        while os.path.isfile(file):#is there a file here
            x_train, y_train = (np.load(file), label)#this file exists, so add the array saved to data!
            np.append(x, x_train)
            np.append(y, y_train)
            
            index = index + 1#next file, iterate index
            file = os.path.join(folder, User_label_index_filename(user, label, index, '.npy'))#set new filepath with new index
        data = np.load(file)#the file location, then data. it doesnt matter if the filename contains .npy at the end
    print(x)
    print(y)
    
if __name__ == '__main__':
    data = Load_Training_Data()
    
    if data == 0:
        print('Exiting!')
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

import random
import numpy as np
import time
import os
import pathlib#paths and files
import matplotlib.pyplot as plt
import json

channels = 16
recording_time = 5
sample_rate = 250

data = np.zeros((0, int(channels), int(recording_time * sample_rate)))#array to hold all recordings
all_labels = []
current_dir = pathlib.Path(__file__).parent#get current folder
path = os.path.join(current_dir, "Datasets", "PainData")#get directory to save recording
json_file_prefix = "imposed_eeg_data_label_"
json_file_suffix = ".json"

file_prefix = "imposed_eeg_data_"
file_suffix = ".npy"
file_index = 0

file_name = file_prefix + str(file_index) + file_suffix
file_path = os.path.join(path, file_name)
while os.path.isfile(file_path):#continue until there is no more file
    samples = np.load(file_path)
    print(f"Loaded sample {samples.shape} at {file_name}!")

    data = np.vstack((data, samples))#add to data
    print(f"Data : {data.shape}")
    
    #LOAD JSON
    
    json_file_name = json_file_prefix + str(file_index) + json_file_suffix
    json_file_path = os.path.join(path, json_file_name)
    with open(json_file_path, "r") as file:
        labels = json.load(file)
    for label in range(len(labels)):
        all_labels.append(labels[label])
    print(f"Labels : {len(labels)}")
    
    file_index = file_index + 1#iterate to next file
    file_name =  file_prefix + str(file_index) + file_suffix
    file_path = os.path.join(path, file_name)#set new file path
print(f"Found {file_index} files!")
print(f"All data : {data.shape}")
print(f"All labels : {len(all_labels)}")

exit()
import tensorflow as tf
from sklearn.model_selection import train_test_split

X_train_val, X_test, y_train_val, y_test = train_test_split(data, labels, test_size=0.2, random_state=42)
X_train, X_val, y_train, y_val = train_test_split(X_train_val, y_train_val, test_size=0.2, random_state=42)

model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(filters=32, kernel_size=(3, 3), activation='relu', input_shape=(16, 1250, 1)),
    tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
    tf.keras.layers.Conv2D(filters=64, kernel_size=(3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(units=128, activation='relu'),
    tf.keras.layers.Dense(units=1, activation='sigmoid')
])
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_val, y_val))
loss, accuracy = model.evaluate(X_test, y_test)

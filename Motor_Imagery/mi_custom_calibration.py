import numpy as np
import time
import pathlib
import os


#----- LOAD THE DATA -----

load_file_index = 0

current_dir = pathlib.Path(__file__).parent#get current folder
path = os.path.join(current_dir, "Recordings",)#get directory to save recording

raw_file_name = "raw_mi_data_" + load_file_index + ".npy"
raw_file_path = os.path.join(path, raw_file_name)#file path

if os.path.isfile(raw_file_path):
    raw_data = np.load(raw_file_path)
else:
    print("No raw data found, exit!")
    exit()

fft_file_name = "fft_mi_data_" + load_file_index + ".npy"
fft_file_path = os.path.join(path, fft_file_name)

if os.path.isfile(fft_file_path):
    fft_file_path = np.load(fft_file_path)
else:
    print("No fft data found, exit!")
    exit()
    
    


from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten
from tensorflow.keras.layers import Conv1D, MaxPooling1D, BatchNormalization


#slice up data into training and validation
x_train, x_val, y_train, y_val = train_test_split(data, labels, test_size=0.2, random_state=42)
# Data normalization
x_train = x_train.reshape(-1, 16, 625)
x_val = x_val.reshape(-1, 16, 625)

x_train /= np.max(x_train)
x_val /= np.max(x_val)


batch_size = 128
epochs = 30

model = Sequential()


model.add(Conv1D(256, (2), input_shape=x_train.shape[1:]))
model.add(Activation('relu'))

model.add(Conv1D(256, (2)))
model.add(Activation('relu'))
model.add(MaxPooling1D(pool_size=(2)))

model.add(Conv1D(124, (2)))
model.add(Activation('relu'))
model.add(MaxPooling1D(pool_size=(2)))

model.add(Conv1D(64, (1)))
model.add(Activation('relu'))
model.add(MaxPooling1D(pool_size=(2)))
model.add(Flatten())

model.add(Dense(512, activation='relu'))
model.add(Dense(256, activation='relu'))
model.add(Dense(1, activation='sigmoid'))
model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])
# Train the model


model.fit(x_train, y_train, validation_data=(x_val, y_val), batch_size=batch_size, epochs=epochs)
# Evaluate the model on the validation data
loss, accuracy = model.evaluate(x_val, y_val, batch_size=batch_size)

print("Validation Loss: {:.4f}".format(loss))
print("Validation Accuracy: {:.2f}%".format(accuracy * 100))

#----- SAVE TF MODEL -----------
model_index = 0
save_model = True
overwrite_model = True
if save_model:
    model_file_name = "mi_calibrated_model_" + model_index + ".tf"
    model_file_path = os.path.join(path, model_file_name)
    model.save(model_file_path, overwrite=overwrite_model)
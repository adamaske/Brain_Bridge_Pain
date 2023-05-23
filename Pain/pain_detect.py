import tensorflow as tf
import random
import numpy as np
import time
import os
import pathlib#paths and files
import matplotlib.pyplot as plt
import json
from scipy.signal import stft 

current_dir = pathlib.Path(__file__).parent#get current folder
path = os.path.join(current_dir, "Datasets", "PainData")#get directory to save recording
file_name ="pain_calibrated_model.tf"
file_path = os.path.join(path, file_name)
# Load the saved model
model = tf.keras.models.load_model(file_path)

# Evaluate the model on the validation set
#------ LOAD NORMAL EEG DATA -------------
current_dir = pathlib.Path(__file__).parent#get current folder
path = os.path.join(current_dir, "Datasets", "PainData")#get directory to save recording

file_name = "imposed_eeg_data.npy"
file_path = os.path.join(path, file_name)
if os.path.isfile(file_path):
    print(f"{file_name} exists!")
    test_data = np.load(file_path)
    print(f"Loaded data : {test_data.shape} from {file_name}")
else:
    print(f"{file_path} does not exist, exiting!")
    exit()
    #-------- LOAD JSON LABELS --------------
json_file_name = "imposed_eeg_data_labels.json"
json_file_path = os.path.join(path, json_file_name)

if os.path.isfile(json_file_path):
    print(f"{json_file_name} exists!")
    loaded_json = 0
    with open(json_file_path, "r") as file:
        loaded_json = json.load(file)
        print(f"Loaded json : {len(loaded_json)} from {json_file_name}")
        all_labels = loaded_json
else:
    print(f"{json_file_path} does not exist, exiting!")
    exit()

amount = 100
x_test = test_data[:amount]
print(f"X_test {x_test.shape}")

x_test = x_test.reshape(-1, 16, 625)
x_test /= np.max(x_test)#normalize

labels = all_labels[:amount]#
y_test = np.zeros((amount ))
for label in range(len(labels)):
    y_test[label] = labels[label]["pain"]

for test in range(amount):
    sample = np.expand_dims(x_test[test], axis=0)
    sample /= np.max(sample)
    id = y_test[test]
    prediction = model.predict(sample)
    print(f"Prediction : {prediction[0][0]:.1f}")
    print(f"Correct : {id}")
    print()
   

loss, accuracy = model.evaluate(x_test, y_test)

print(f"Test Loss : {loss}")
print(f"Test Accuracy : {accuracy}")

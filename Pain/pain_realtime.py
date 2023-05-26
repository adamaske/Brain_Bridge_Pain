import time
import os
import pathlib#paths and files
import random 

import numpy as np
from scipy.signal import stft
import matplotlib.pyplot as plt

from pylsl import resolve_stream#networking
from pylsl import StreamInlet

import tensorflow as tf

#load model
channels = 16
recording_time = 5
segment_duration = 5
segment_offset = 1

recording_time = 5
sample_rate = 125


current_dir = pathlib.Path(__file__).parent#get current folder
path = os.path.join(current_dir, "Datasets", "PainData")#get directory to save recording
file_name ="pain_calibrated_model.tf"
file_path = os.path.join(path, file_name)
if not os.path.isdir(file_path):
    print(f"Model was not found! Exiting...")
    exit()
# Load the saved model
model = tf.keras.models.load_model(file_path)

                                  
segment_start_time = 0

data = np.zeros((channels, recording_time * sample_rate))


amount = 10
predictions = np.zeros(amount)
pains = np.zeros(amount)
for run in range(amount):
    print(f"Run : {run}")
    do_pain = random.randrange(0, 100) % 2#CHOOSE WHETER TO DO PAIN OR NOT
    pains[run] = do_pain
    if do_pain:
        print(f"DO PAIN THIS RECORDING!")
    else:
        print(f"NO PAIN!")
    
    use_input_to_start = True
    if use_input_to_start:
        start = input("Enter to Start!")
    else:    
        wait_time = 1
        start_time = time.time()
        while time.time() - start_time < wait_time:
            id_X = 0
    print(f"Waiting for connection to RAW Lsl Stream")
    inlet = StreamInlet(resolve_stream('type', 'RAW')[0])#RAW = time series, FFT = ffts
                                                    #THIS MUST CORRESEPOND WITH OPENBCIGUI NETOWRKING
                     
    print("RECORDING STARTED!!")
    
    start_time = time.time()
    for sample in range(recording_time * sample_rate):
        data_sample, timestamp = inlet.pull_sample()
        for channel in range(channels):
            data[channel][sample] = data_sample[channel]
    print(f"RECORDING COMPLETE")
    print(f"Recorded : {data.shape}")
    print()
    print()
    
    #---- DO PREDICTION
    sample = np.expand_dims(data, axis=0)
    sample /= np.max(sample)
    prediction = model.predict(sample)
    predictions[run] = prediction[0][0]#add to predictions
    print(f"Prediction : {prediction[0][0]:.3f}")
    print(f"Correct : {do_pain}")

#--- VISUALIZE RESULTS-----

t = np.linspace(0, amount, amount)
errors = np.zeros((amount))
for pred in range(len(predictions)):
    print(f"Prediction {predictions[pred]}, Pain {pains[pred]}")
    error = predictions[pred] - pains[pred] 
    print(f"Error {error}")
    print(f"Error Squared {np.square(error)}")
    errors[pred] = np.square(error)#sqaure the error
    
plt.scatter(t, errors)

coeff = np.polyfit(t, errors, 1)
x_reg = np.linspace(min(t), max(t), 100)
y_reg = np.polyval(coeff, x_reg)
plt.plot(x_reg, y_reg, color='red', label='Best fit')
plt.xlabel("Runs")
#plt.ylim((0, 1))
plt.ylabel("Prediction")
plt.show()
exit()
    
start_time = time.time()
for sample in range(recording_time * sample_rate):
    data_sample, timestamp = inlet.pull_sample()
    for channel in range(channels):
        data[channel][sample] = data_sample[channel]
    
print(data.shape)



for channel in range(channels):
    time_series = data[channel]
    
    fft_data = np.fft.rfft(time_series)
    fft_freqs = np.fft.rfftfreq(len(time_series), d=1/sample_rate)
    unmodified_magnitude_spectrum = np.abs(fft_data)#get the magnitudes
    unmodified_normalized_magnitude_spectrum = unmodified_magnitude_spectrum / len(time_series)#normalize them to get correct amplitude

    window_size = 64   
    hop_length = 32
    original_frequencies, original_times, original_spectrogram = stft(time_series, window='hamming', nperseg=window_size, noverlap=window_size-hop_length, fs=sample_rate)
    
    if not False:
        continue
    plt.subplot(1, 3, 1)
    t = np.linspace(0, recording_time, len(time_series))
    plt.plot(t, time_series)
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.title('Time Series')
    
    plt.subplot(1,3, 2)
    plt.plot(fft_freqs, unmodified_normalized_magnitude_spectrum)
    plt.xlabel('Frequency')
    plt.ylabel('Amplitude')
    plt.title('Fourier Transform')
    
    plt.subplot(1,3,3)
    plt.pcolormesh(original_times, original_frequencies, np.abs(original_spectrogram), shading='auto')
    plt.xlabel('Time')
    plt.ylabel('Frequency')
    plt.title('Spectrogram')
    
    plt.show()
    
# run trough model

sample = np.expand_dims(data, axis=0)
sample /= np.max(sample)
id = 0
prediction = model.predict(sample)
print(f"Prediction : {prediction[0][0]:.1f}")
print(f"Correct : {id}")

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

# results


# delete data
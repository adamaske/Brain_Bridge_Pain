from pylsl import StreamInlet, resolve_stream
import numpy as np
import time
import matplotlib.pyplot as plt
from matplotlib import style
from collections import deque


last_print = time.time()
fps_counter = deque(maxlen=150)
duration = 5

# first resolve an EEG stream on the lab network
print("looking for an EEG stream...")
streams = resolve_stream('type', 'FFT')
# create a new inlet to read from the stream
inlet = StreamInlet(streams[0])

channel_data = {}
recording_time = 5
start_time = time.time()

channels = 16
while time.time() - start_time < recording_time:
    for i in range(channels):
        sample, timestamp = inlet.pull_sample()
        if timestamp:
            if i not in channel_data:
                channel_data[i] = sample
            else:
                channel_data[i].append(sample)
    current_time = time.time() - start_time
    print(f"Elapsed {current_time:.1f}", end='\r')


print(f"Channel data length {len(channel_data)}")
print(f"Channel data 0 length {len(channel_data[i])}")

for chan in channel_data:
    plt.plot(channel_data[chan][:60])
plt.show()
from pylsl import resolve_stream
from pylsl import StreamInlet

from pythonosc.udp_client import SimpleUDPClient

import time

if __name__ == "__main__":
  ip = "127.0.0.1"#local computer ip 
  port = 5800#port - THIS MUST CORRESPOND WITH UNREAL ENGINE OSC SERVER PORT
  client = SimpleUDPClient(ip, port)  # Create client
  print(f"OSC Client {ip} : {port}")
  sendOSC = True#should we send over OSC
  
  fakeMessages = False#do fake messages 
  fake_msg_time = 10#how long
  fake_msg_firerate = 2
  if fakeMessages:
    start_time = time.time()
    while time.time() - start_time < fake_msg_time:
      msg = "/neuropype/left"
      value = 5
      client.send_message(msg, float(value))#send it over OSC
      print(f"Sent fake OSC Msg {msg} : {value}")
      time.sleep(1/fake_msg_firerate)
    print("Finsihed fake messages")
    exit()
  
  print("Waiting for connection to MI LSL Stream!")
  streams = resolve_stream('name', 'mi_lsl')
  inlet  = StreamInlet(streams[0])
  print("Connected to MI LSL Stream")
  
  
  
  markers = ['left', 'right'] #, 'up', 'down', 'forward', 'backward'] #The marker being sent, 
                              #this must correspond with targets in NeuroPype Pipline(found in "assign targets" module) 
                              #AND UNREAL ENGINE
  predictions = [0, 0]#, 0, 0, 0, 0]#caching the predictions
                      #this must be same length as markers

  while True:#main loop, add some way to stop the app
    sample, timestamp = inlet.pull_sample()#get the data from LSL stream
    
    highest_prediction = 0
    highest_prediction_index = 0
    for marker in range(len(markers)):#each sample gives us the prediction for every marker
      label = markers[marker]
      value = sample[marker]
      print(f"{label.capitalize()} : {value:.1f}")#prints the predctions
      
      predictions[marker] = value#cache the prediction
      
      if value > highest_prediction:#is this the highest score prediction?
        highest_prediction = value#then this is the new highest value
        highest_prediction_index = marker#cache the current marker
      
    
    if sendOSC:#send highest prediction over OSC
      msg = f"/nueropype/{markers[highest_prediction_index]}" #store message, this must correspond to the ReceiveMentalCommand function in Unreal Engine
      strength = predictions[highest_prediction_index] #how strong is the prediction, get from cached prediction
      client.send_message(msg, float(strength))#send it over OSC
       
import time
import matplotlib
import matplotlib.pyplot as plt
import random
from pylsl import StreamInfo, StreamOutlet

#VISUALS
fontsize = 30 #fontsize
matplotlib.rcParams.update({'font.size': fontsize})
fig, ax = plt.subplots() #figure and axes
fig.set_facecolor('black')#black background color
ax.set_xlim(-1, 1)#axis goes from -1 to 1
ax.set_ylim(-1, 1)
ax.axvline(0, color='red')#red lines
ax.axhline(0, color='red')

box_x_size = 0.4#box size
box_y_size = 0.4
box = plt.Rectangle((-box_x_size / 2, -box_y_size / 2), box_x_size, box_y_size, facecolor='blue', edgecolor='white')#Box moved
ax.add_patch(box)#add box to axe

trial_text = ax.text(0, 1, 'Direction', ha='center', va='bottom', color='white')#text object, shows what direction


#trial_type_text = ax.text(0, 1, 'Direction', ha='center', va='bottom', color='white')

plt.ion()
plt.draw()
plt.show()
#END VISUALS

#Welcome to Motor Imagery Calibartion Marker Injection
warmup_trials = 2 #Amount of warmup trails. A warmup trial does not count in calibartion
trails_per_class = 60 #Amount of trials per class (left / right) 
perform_time = 3.5 #How long does one trial last, in seconds
wait_time = 1 #How long to wait between each trial
pause_every =30 #After x trails, give the user a break
pause_duration = 10 #How long the trail last

labels = ['L', 'R'] #The labels is the name of the "class" being calibarted, for example Left and right
markers = ['left', 'right'] #The marker being sent, this must correspond with targets in NeuroPype Pipline(found in "assign targets" module)
box_directions = [-1, 1]#What x direction does the box move per label

info = StreamInfo(name='MotorImagery-Markers', #Stream name
                  type='Markers', #type
                  channel_count=1, #how many channels. This only need to send one marker at a time
                  nominal_srate=0, #this is an outlet, so the Input HZ is set to 0
                  channel_format='string', #What data type is being sent. This sends "left", "right", "calib-begin" etc.
                  source_id='123dsasd') #Uniqie identifier for this stream, 

outlet = StreamOutlet(info) #LSL outlet stream, with info as its settings


print('Welcome to Motor Imagery Calibartion!')
#name = input('Enter your name / indentifier :') #ask for indentifer, not used atm
start = input('Press any button to start trials!')#press anybutton to start

trial_amount = warmup_trials + (trails_per_class * len(labels)) #total amount of trails to run. Warmups + 60 left + 60 right

for trial in range(1, trial_amount + 1): #Trial loop. Starts at 1
    trial_text.set_text(f"Trail : {trial}")#update trial text to correct trial
    
    choice = random.choice(range(len(labels))) #Is this a left or right trail? Left and Right trials must be in a random order for machine learning. If not the ML will learn the temporal features
    if trial < warmup_trials: #Warmump trial
        print('This is warump trail')
        trial_text.set_text(f"Trial (Warmup) : {trial}")#update trial text to correct trial
    
    if trial == warmup_trials: #Warmups are finsihed 
        print('Warmups are finsihed!')
        print('Starting calibration trials now!')
        outlet.push_sample(['calib-begin']) #Send "Start calibration marker". This string must correspond to the "Begin Calibration" marker in NeuroPype
        
    if trial > warmup_trials: #Trial for calibration
        marker = markers[choice]#The marker to send / What class is this trial (right / left)
        outlet.push_sample([marker])#Send the string through outlet
        print(f"Trial {marker.capitalize()} started!")
        
    start_time = time.time() #time the trial started
    while time.time() - start_time < perform_time: #current trial loop
        time_percentage =  (time.time() - start_time) / perform_time#how much of the trial time has gone
        box_x = time_percentage * box_directions[choice]#Box X. 0 is middle, all left is -1. If choice is left, then we go to negative percentage
        box.set_xy((box_x - (box_x_size/ 2), -box_y_size / 2)) #set new box position, minus half box size to align on axis properly
        fig.canvas.draw_idle() 
        fig.canvas.flush_events()
        
        print(f"Performing : {time.time()-start_time:.1f}", end='\r')
        
    start_time = time.time() #what time the waiting starts
    while time.time() - start_time < wait_time:#waiting loop
        
        print(f"Waiting : {time.time()-start_time:.1f}", end='\r')

    if trial % pause_every == 0: #Check if we should pause
        start_time = time.time()
        while time.time() - start_time < pause_duration:
            
            print(f"Paused : {time.time()-start_time:.1f}", end='\r')

outlet.push_sample(['calib-end'])#End calibration


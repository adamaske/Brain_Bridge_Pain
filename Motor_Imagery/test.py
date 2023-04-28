import time
import matplotlib
import matplotlib.pyplot as plt
import random
from pylsl import StreamInfo, StreamOutlet

# function to move box
def move_box(dx, dy):
    x, y = box.get_xy()
    box.set_xy((x+dx, y+dy))
    fig.canvas.draw_idle()

# register key press event handlers
def on_press(event):
    if event.key == 'left':
        move_box(-0.1, 0)
    elif event.key == 'right':
        move_box(0.1, 0)
    elif event.key == 'up':
       
        move_box(0, 0.1)
        trail_text.set_text(f"Trail : {1}")
        
    elif event.key == 'down':
        move_box(0, -0.1)
        
if __name__ == '__main__':
    fontsize = 30 #fontsize
    matplotlib.rcParams.update({'font.size': fontsize})

    fig, ax = plt.subplots(figsize=(7,7)) #figure and axes
    
    fig.set_facecolor('black')#black background color
    ax.set_xlim(-1, 1)#axis goes from -1 to 1
    ax.set_ylim(-1, 1)

    ax.axvline(0, color='red')#red lines
    ax.axhline(0, color='red')

    box = plt.Rectangle((0,0), 0.2, 0.2, facecolor='blue', edgecolor='white')
    ax.add_patch(box)
    # create text object at top of plot
    text = ax.text(0, 1, 'Right', ha='center', va='bottom', color='white')
    trail_text = ax.text(-1, -1, f"Trail : {0}", ha='left', va='bottom', color='black')

    fig.canvas.mpl_connect('key_press_event', on_press)
    plt.xlim(xmin=-1.5, xmax=1.5)
    plt.ylim(ymin=-1.5, ymax=1.5)
    plt.show()
    
    
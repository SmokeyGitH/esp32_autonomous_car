'''
import cv2
import numpy as np
import socket
from log import key_check
import os
import time
s = socket.socket()         # Create a socket object
host = '192.168.228.100'            
port = 12345                # Reserve a port for your service.
s.connect((host, port))


cap = cv2.VideoCapture('http://192.168.228.251:81/stream') #esp32cam ip stream. Check on esp32cam serial for ip
time.sleep(5)               #wait for 5 sec
print('start')

#creating file store data
file_name = 'training_data.npy'
if os.path.isfile(file_name):
    print("File exists , loading previous data")
    training_data = list(np.load(file_name, allow_pickle=True))
else:
    print('file does not exist, starting fresh')
    training_data = []

def key_out(key):
    output = [0, 0, 0, 0]
    if 'A' in key:
        output[0] = 1
    if 'D' in key:
        output[2] = 1
    if 'W' in key:
        output[1] = 1
    if 'S' in key:
        output[3] = 1
    return output
    


while(True):
    key = key_check()
    a = key_out(key)
    
    #create a serialized dict
    x = '{"a":'
    x += str(a[0])
    x += ',"d":'
    x += str(a[2])
    x += ',"w":'
    x += str(a[1])
    x += ',"s":'
    x += str(a[3])
    x += "}"
    msg = str.encode(x, 'utf-8')
    #print(msg)
    s.send(msg)
    data1 = s.recv(1024)
    ret, frame = cap.read()
    rotate = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE) #align the video feed 
    screen = cv2.cvtColor(rotate, cv2.COLOR_BGR2GRAY)
    screen = cv2.resize(screen, (80, 60))
    a.pop()
    #print(a)
    training_data.append([screen, a])
    cv2.imshow('rotate', rotate)
    cv2.imshow('screen', screen)
    #save data to file after every 500 data point collection
    if len(training_data) % 500 == 0:
        print(len(training_data))
        np.save(file_name, training_data)
    
   
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
'''
'''
import cv2
import numpy as np
import socket
from log import key_check
import os
import time

# Set up the socket connection
s = socket.socket()
host = '192.168.228.100'
port = 12345
try:
    s.connect((host, port))
    print(f"Connected to {host}:{port}")
except Exception as e:
    print(f"Socket connection failed: {e}")
    exit(1)

# Set up the video capture
cap = cv2.VideoCapture('http://192.168.228.251:81/stream')
time.sleep(5)
print('Starting video capture')

# Load or initialize the training data
file_name = 'training_data.npy'
if os.path.isfile(file_name):
    print("File exists, loading previous data")
    try:
        training_data = list(np.load(file_name, allow_pickle=True))
    except Exception as e:
        print(f"Error loading training data: {e}")
        training_data = []
else:
    print('File does not exist, starting fresh')
    training_data = []

# Define a function to map keys to outputs
def key_out(key):
    output = [0, 0, 0, 0]
    if 'A' in key:
        output[0] = 1
    if 'D' in key:
        output[2] = 1
    if 'W' in key:
        output[1] = 1
    if 'S' in key:
        output[3] = 1
    return output

# Main loop
while True:
    key = key_check()
    a = key_out(key)
    
    # Serialize control data
    x = '{"a":' + str(a[0]) + ',"d":' + str(a[2]) + ',"w":' + str(a[1]) + ',"s":' + str(a[3]) + '}'
    msg = str.encode(x, 'utf-8')

    try:
        s.send(msg)
        data1 = s.recv(1024)
    except Exception as e:
        print(f"Socket error: {e}")
        break

    # Capture and process the video frame
    ret, frame = cap.read()
    if not ret:
        print("Failed to read frame from video stream.")
        continue

    try:
        rotate = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)  # Rotate video feed
        screen = cv2.cvtColor(rotate, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
        screen = cv2.resize(screen, (80, 60))  # Resize to (80, 60)

        # Add data to training dataset
        training_data.append([screen, a.copy()])

        # Display the processed frames
        cv2.imshow('rotate', rotate)
        cv2.imshow('screen', screen)

    except Exception as e:
        print(f"Error processing frame: {e}")
        continue

    # Save data after every 500 entries
    if len(training_data) % 500 == 0:
        print(f"Saving {len(training_data)} data points...")
        try:
            np.save(file_name, training_data)
            print("Data saved successfully.")
        except Exception as e:
            print(f"Error saving training data: {e}")

    # Exit condition
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Exiting...")
        break

# Clean up
cap.release()
cv2.destroyAllWindows()
'''


import cv2
import numpy as np
import socket
from log import key_check
import os
import time

# Socket setup
s = socket.socket()
host = '192.168.228.100'
port = 12345
s.connect((host, port))

# Video capture setup
cap = cv2.VideoCapture('http://192.168.228.251:81/stream')
time.sleep(5)
print('start')

# Create or load training data file
file_name = 'training_data.npy'
if os.path.isfile(file_name):
    print("File exists, loading previous data")
    training_data = list(np.load(file_name, allow_pickle=True))
else:
    print('File does not exist, starting fresh')
    training_data = []

# Key output mapping
def key_out(key):
    output = [0, 0, 0, 0]
    if 'A' in key:
        output[0] = 1
    if 'D' in key:
        output[2] = 1
    if 'W' in key:
        output[1] = 1
    if 'S' in key:
        output[3] = 1
    return output

# Main loop
while True:
    key = key_check()
    a = key_out(key)
    
    # Create a serialized dict for sending
    x = '{"a":' + str(a[0]) + ',"d":' + str(a[2]) + ',"w":' + str(a[1]) + ',"s":' + str(a[3]) + '}'
    msg = str.encode(x, 'utf-8')
    s.send(msg)
    data1 = s.recv(1024)
    
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame")
        break
    
    # Process frame
    rotate = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
    screen = cv2.cvtColor(rotate, cv2.COLOR_BGR2GRAY)
    screen = cv2.resize(screen, (80, 60))
    
    # Debugging
    print(f"Screen shape: {screen.shape}, Key output: {a}")
    
    # Append to training_data
    try:
        training_data.append([screen, a.copy()])
    except Exception as e:
        print(f"Error appending to training_data: {e}")
        break
    
    # Display frames
    cv2.imshow('rotate', rotate)
    cv2.imshow('screen', screen)
    
    # Save training data every 500 samples
    if len(training_data) % 500 == 0:
        try:
            print(f"Saved {len(training_data)} data points")
            np.save(file_name, training_data)
        except Exception as e:
            print(f"Error saving training_data: {e}")
            break
    
    # Exit condition
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()



import cv2
import numpy as np
import time
import os 
import socket

s = socket.socket()         # Create a socket object
host = '192.168.228.100'      # Get local machine name
port = 12345                # Reserve a port for your service.
s.connect((host, port))

print('start')
file_name = 'training_data.npy'
if os.path.isfile(file_name):
    print("File exists , loading previous data")
    training_data = list(np.load(file_name, allow_pickle=True))
else:
    print('file does not exist, starting fresh')
    training_data = []

speed = 1000              #range 0 to 1000

last_pos = 0
w = 0
KP = 2
KD = 1.4
KI = .5
max_correction = 1000

def convert(x, i_m, i_M, o_m, o_M):
    return max(min(o_M, (x - i_m) * (o_M - o_m) // (i_M - i_m) + o_m), o_m)

def correction(angle):
    if angle > 0:
        if angle > max_correction:
            angle = max_correction
        else:
            angle = angle
    else:
        if angle < -max_correction:
            angle = -max_correction
        else:
            angle = angle 
    return angle

def servo_angle(z):
    if z > 0:
        steer_angle = convert(z, 0, 1000, 75, 89)
    else:
        steer_angle = convert(z, -1000, 0, 59, 75)
    return steer_angle


cap = cv2.VideoCapture('http://192.168.228.251:81/stream')

while True:
    l = 0
    r = 0
    ret, frame = cap.read()
    #rotate = cv2.rotate(frame, cv2.ROTATE_180)
    #rotate = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)

    screen = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    screen = cv2.resize(screen, (80, 60))
    kernel = np.ones((15,15), np.float32)/225
    smoothed = cv2.filter2D(frame, -1, kernel)
    edges = cv2.Canny(screen,100,200)
    low_b = np.uint8([55, 55, 55])
    high_b = np.uint8([0, 0, 0])
    mask = cv2.inRange(smoothed, high_b, low_b)
    contours, hierarchy = cv2.findContours(mask, 1, cv2.CHAIN_APPROX_NONE)
    if len(contours)> 0:
        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c)
        if M["m00"] !=0 :
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            #print("CX : "+str(cx)+"  CY : "+str(cy))
            w = convert(cx, 0, 300, -500, 500)
            propotional_angle = int(w)
            derivative_angle = propotional_angle - last_pos
            integral_angle = propotional_angle + last_pos
            steer = (propotional_angle*KP + derivative_angle*KD + integral_angle*KI)
            z = int(correction(steer))
            st = servo_angle(z)
            x = '{"a":'
            x += str(st)
            x += ',"w":'
            x += str(speed)
            x += "}"
            msg = str.encode(x, 'utf-8')
            #print(msg)
            s.send(msg)
            data1 = s.recv(1024)
            last_pos = propotional_angle
            a = [0, 0, 0]
            if st > 78:
                a = [0, 1, 1]
            if st < 72:
                a = [1, 1, 0]
            if st>72 and st<78:
                a = [0, 1, 0]
            training_data.append([screen, a])
            #cv2.circle(mask, (cx,cy), 5, (0 , 0, 255), -1)
            #print(st, a)
            if len(training_data) % 500 == 0:
                print(len(training_data))
                np.save(file_name, training_data)
    else :
        print("I don't see the line")
        x = '{"a":'
        x += str(75)
        x += ',"w":'
        x += str(0)
        x += "}"
        msg = str.encode(x, 'utf-8')
        #print(msg)
        s.send(msg)
        data1 = s.recv(1024)
    cv2.drawContours(frame, contours, -1, (0,255,0), 1)
    cv2.imshow("gray", screen)
    #cv2.imshow('frame2', rotate)
    #cv2.imshow('mask', mask)
    #cv2.imshow('smooth', smoothed)
    #cv2.imshow("canny", edges)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("QUIT")
        x = '{"a":'
        x += str(75)
        x += ',"w":'
        x += str(0)
        x += "}"
        msg = str.encode(x, 'utf-8')
        #print(msg)
        s.send(msg)
        data1 = s.recv(1024)
        break

cap.release()
cv2.destroyAllWindows()


'''
import cv2
import numpy as np
import time
import os 
import socket

s = socket.socket()         # Create a socket object
host = '192.168.228.100'      # Get local machine name
port = 12345                # Reserve a port for your service.
s.connect((host, port))

print('start')

file_name = 'training_data.npy'
if os.path.isfile(file_name):
    print("File exists, loading previous data")
    training_data = list(np.load(file_name, allow_pickle=True))
else:
    print('File does not exist, starting fresh')
    training_data = []

speed = 500         # Range 0 to 1000

last_pos = 0
w = 0
KP = 2
KD = 1.4
KI = .5
max_correction = 1000

def convert(x, i_m, i_M, o_m, o_M):
    return max(min(o_M, (x - i_m) * (o_M - o_m) // (i_M - i_m) + o_m), o_m)

def correction(angle):
    if angle > 0:
        if angle > max_correction:
            angle = max_correction
    else:
        if angle < -max_correction:
            angle = -max_correction
    return angle

def servo_angle(z):
    if z > 0:
        steer_angle = convert(z, 0, 1000, 75, 89)
    else:
        steer_angle = convert(z, -1000, 0, 59, 75)
    return steer_angle

cap = cv2.VideoCapture('http://192.168.228.251:81/stream')

while True:
    l = 0
    r = 0
    ret, frame = cap.read()
    # Rotate the frame if necessary
    #rotate = cv2.rotate(frame, cv2.ROTATE_180)
  #rotate = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)


    screen = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #screen = cv2.resize(screen, (80, 60))  # Ensure consistent size
    
    kernel = np.ones((15,15), np.float32)/225
    smoothed = cv2.filter2D(frame, -1, kernel)
    
    low_b = np.uint8([55, 55, 55])
    high_b = np.uint8([0, 0, 0])
    mask = cv2.inRange(smoothed, high_b, low_b)
    
    contours, hierarchy = cv2.findContours(mask, 1, cv2.CHAIN_APPROX_NONE)
    
    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c)
        
        if M["m00"] != 0:
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            w = convert(cx, 0, 300, -500, 500)
            
            proportional_angle = int(w)
            derivative_angle = proportional_angle - last_pos
            integral_angle = proportional_angle + last_pos
            
            steer = (proportional_angle * KP + derivative_angle * KD + integral_angle * KI)
            z = int(correction(steer))
            st = servo_angle(z)
            
            # Construct message for sending via socket
            x = '{"a":' + str(st) + ',"w":' + str(speed) + "}"
            msg = str.encode(x, 'utf-8')
            s.send(msg)
            data1 = s.recv(1024)  # Receive response
            
            last_pos = proportional_angle
            
            # Label creation based on steering angle
            a = [0, 0, 0]
            if st > 78:
                a = [0, 1, 1]
            if st < 72:
                a = [1, 1, 0]
            if 72 <= st <= 78:
                a = [0, 1, 0]

            # Ensure that the screen and label are consistent
            if len(a) != 3:
                print(f"Label mismatch before appending: {a}")
                continue  # Skip appending this iteration if label is inconsistent

            training_data.append([screen, a])

            # Save data to file after every 500 data points
            if len(training_data) % 500 == 0:
                print(f"Saving {len(training_data)} data points...")
                try:
                    np.save(file_name, training_data)
                except Exception as e:
                    print(f"Error saving training data: {e}")
                    break

    else:
        print("I don't see the line")
        x = '{"a":' + str(75) + ',"w":' + str(0) + "}"
        msg = str.encode(x, 'utf-8')
        s.send(msg)
        data1 = s.recv(1024)

    # Show processed frames for debugging
    cv2.imshow("gray", screen)
    # cv2.imshow('frame2', rotate)
    #cv2.imshow('mask', mask)
    #cv2.imshow('smooth', smoothed)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("QUIT")
        x = '{"a":' + str(75) + ',"w":' + str(0) + "}"
        msg = str.encode(x, 'utf-8')
        s.send(msg)
        data1 = s.recv(1024)
        break

cap.release()
cv2.destroyAllWindows()
'''

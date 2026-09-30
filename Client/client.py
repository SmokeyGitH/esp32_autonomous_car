

import socket               # Import socket module
import time
from pynput.keyboard import Listener
import json
from log import key_check



s = socket.socket()         # Create a socket object
host = '192.168.228.100'    # esp32 ip
port = 12345             # Reserve a port for your service.
s.connect((host, port))
#a = 'b'

try:
    print(f"Connecting to {host}:{port}...")
    s.connect((host, port))
    print("Connection established!")
except Exception as e:
    print(f"Connection error: {e}")


def key_out(key):
    output = [0, 0, 0, 0]
    if 'A' in key:
        output[0] = 1
    if 'D' in key:
        output[3] = 1
    if 'W' in key:
        output[1] = 1
    if 'S' in key:
        output[2] = 1
    return output

try:
    while True:
        key = key_check()
        a = key_out(key)
        x = '{"a":'
        x += str(a[0])
        x += ',"d":'
        x += str(a[3])
        x += ',"w":'
        x += str(a[1])
        x += ',"s":'
        x += str(a[2])
        x += "}"
        msg = str.encode(x, 'utf-8')
        print(msg)
        s.send(msg)
        data1 = s.recv(1024)

except KeyboardInterrupt:
    print('exit')
    pass



'''
import socket  # Import socket module
import json
import time
from pynput.keyboard import Listener, Key

# Keep track of pressed keys
pressed_keys = set()

# Function to handle key presses
def on_press(key):
    try:
        pressed_keys.add(key.char.upper())  # Add key to the set
    except AttributeError:
        if key == Key.space:
            pressed_keys.add("SPACE")

# Function to handle key releases
def on_release(key):
    try:
        pressed_keys.discard(key.char.upper())  # Remove key from the set
    except AttributeError:
        if key == Key.space:
            pressed_keys.discard("SPACE")

# Map key presses to control commands
def key_out():
    output = {"a": 0, "d": 0, "w": 0, "s": 0}
    if "W" in pressed_keys:
        output["w"] = 1
    if "A" in pressed_keys:
        output["a"] = 1
    if "S" in pressed_keys:
        output["s"] = 1
    if "D" in pressed_keys:
        output["d"] = 1
    return output

# Initialize socket connection
s = socket.socket()  # Create a socket object
host = '192.168.29.222'  # ESP32 IP address
port = 12345  # ESP32 Port
s.connect((host, port))  # Connect to ESP32 server

#s.setblocking(0)

try:
    # Start listening to the keyboard in a separate thread
    with Listener(on_press=on_press, on_release=on_release) as listener:
        print("Client running. Use WASD to send commands.")
        while True:
            # Generate commands from key states
            commands = key_out()
            command_json = json.dumps(commands)
            msg = str.encode(command_json, 'utf-8')
            print(f"Sending: {msg}")  # For debugging
            s.send(msg)  # Send command to the server
            
            # Receive acknowledgment or data from the server
            data = s.recv(1024)
            print(f"Received: {data.decode('utf-8')}")  # Print server response
            
            # Small delay to prevent flooding the server
            time.sleep(0.1)
except KeyboardInterrupt:
    print("Exiting...")
    s.close()
except Exception as e:
    print(f"Error: {e}")
    s.close()
'''
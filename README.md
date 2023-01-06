# Realtime Human Skeleton Interaction in ArenaXR

This repository contains the code for the realtime human skeleton 3d interaction in ArenaXR using a single camera as input started for Individual Study under Prof. Elahe Soltanaghai at University of Illinois Urbana-Champaign. This project demonstrates a human skeleton interacting(body movements, walking, waving) in a 3D Space using ArenaXR and iOS Aapplication which uses camera OR PC's front camera based on preference as user input and sends it to server making it easy to plugin at any location. 

# Getting Started
There two ways to run this project, we can use a iOS mobile device or PC camera as input to our system. You should follow Input Method: 1 approach if you want to user your mobile application as input or Input Method: 2 if you want PC as your input. Make sure to host server if you're using iOS device approach. 

Follow these steps to install and run the test app:

Clone the repository:
`git clone https://github.com/shhr3y/arena-project.git`

## Input Method 1
### iOS App
This app acts as a input medium using front camera for our system. It uses Googles Mediapipe Pose Detection with Heavy Model for realtime pose detection on camera input. If need to change model complexity in order to work with different FPS, it needs to be initialised in variable `tracker` inside `PoseController.swift`. The extracted landmarks are then emitted to socket server hosted on PC after some threshing and smoothening. The variable `REF_SERVER` in `SocketService.swift` needs to be updated with latest IP-Address whenever the server is hosted.

**Prerequisites**  
Xcode

### Installation
* `cd arena-project/arena-app`

* Run `pod install`

* Now, open arena-app.xcworkspace file in the Xcode

* Pass your App-ID in the AppDelegate file, and run the app.

* Tap on connect and accept permission to access camera.

* You can adjust your orientation based on your preference to cover maximum area. You can also use fish eye lens to gain maximum coverage.

### Server
This server acts as receiver to the iOS application for the landmarks. It receives and re-write the landmarks on `landmarks.txt`. It also republishes the received landmarks to html landmarks renderer, which can be used to visualise landmarks in 3D Space. The variables `host` and `port` can be updated based on available ports but make sure to update the same in variable `REF_SERVER` in `SocketService.swift` to make sure server communicates with the clients succesfully.

**Prerequisites**   
python  
socketio  
npm (comes with Node.js)

### Running the server

* `cd arena-project`

* Run `python main.py`

* `cd renderer`

* Open `renderer.html` in any browser. Google Chrome preffered.


## Input Method 2
###  PC's Front Camera
In this method, PC acts as a input medium using front camera for our system. It uses Googles Mediapipe Pose Detection with Heavy Model for realtime pose detection on camera input. If need to change model complexity in order to work with different FPS, it needs to be initialised  in variable `min_detection_confidence` and `min_tracking_confidence` inside `mp.py`. The extracted landmarks are then re-written on file `landmarks.txt`. This approach doesn't need socket server to be hosted.

**Prerequisites**  
python  
mediapipe

### Installation
* `cd arena-project`

* Run `python mp.py`

* Accept permission to access camera.

* You can also use fish eye lens to gain maximum coverage.
    
## Arena Script
This script reads latest landmarks from file `landmarks.txt` and updates position of body part objects initialised in 'ar_objects.py' on the Arena Server. You can change the update rate of landmarks on server using the variable `animation_key` declared in `ar_objects.py`, it uses milliseconds data type. The script can be used to update landmark positions using smooth animations or without them, which can be manually changed using the variable `is_animation_on` inside the same file.  

**Prerequisites**      
python   
arena-py

### Running the server

* `cd arena-project`

* Run `python xr.py`

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

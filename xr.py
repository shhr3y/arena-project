from arena import *
import cv2
import mediapipe as mp
import time
import pickle
from ar_objects import *

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

scene = Scene(host="mqtt.arenaxr.org", scene="myfirstscene")

animation_key = 200

landmarkFile = 'landmarks.txt' 

@scene.run_once
def init():
    print('arena run_once')
    add_shapes()
    

@scene.run_forever(interval_ms=300)
def update():

    with open(landmarkFile, "r+") as f:
        data = f.read()
        try: 
            landmarks = json.loads(data)
            update_skeleton(landmarks)   
        except:
            print('Exception Occured')
            
    # print('arena run_forever')
    # start_time = time.time()

def add_shapes():
    scene.add_object(right_wrist_shape)
    scene.add_object(left_wrist_shape)
    scene.add_object(head_shape)
    scene.add_object(left_shoulder_shape)
    scene.add_object(right_shoulder_shape)
    scene.add_object(left_elbow_shape)
    scene.add_object(right_elbow_shape)
    
def update_skeleton(landmarks):
    if len(landmarks) != 0:
        update_head(landmarks[0])
        update_right_wrist(landmarks[15])
        update_left_wrist(landmarks[16])
        update_right_shoulder(landmarks[11])
        update_left_shoulder(landmarks[12])
        update_right_elbow(landmarks[13])
        update_left_elbow(landmarks[14])

        scene.run_animations(head_shape)
        scene.run_animations(right_wrist_shape)
        scene.run_animations(left_wrist_shape)
        scene.run_animations(left_shoulder_shape)
        scene.run_animations(right_shoulder_shape)
        scene.run_animations(left_elbow_shape)
        scene.run_animations(right_elbow_shape)
        # scene.update_objects([
        #     head_shape, 
        #     right_wrist_shape,
        #     left_wrist_shape,
        #     left_shoulder_shape,
        #     right_shoulder_shape,
        #     left_elbow_shape,
        #     right_elbow_shape,
        # ])

    

if __name__ == "__main__":
    scene.run_tasks()





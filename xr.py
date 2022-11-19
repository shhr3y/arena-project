from arena import *
import mediapipe as mp
from ar_objects import *
import time

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

scene = Scene(host="mqtt.arenaxr.org", scene="myfirstscene")

landmarkFile = 'landmarks.txt' 

@scene.run_once
def init():
    print('arena run_once')
    add_shapes()
    

@scene.run_forever(interval_ms = animation_key)
def update():
    print('arena run_forever')
    start_time = time.time()
    with open(landmarkFile, "r+") as f:
        data = f.read()
        try: 
            landmarks = json.loads(data)
            # print(time.time() - start_times)
            update_skeleton(landmarks)   
        except:
            print('Exception Occured')
            

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
        update_right_hip(landmarks[23])
        update_left_hip(landmarks[24])
        update_right_knee(landmarks[25])
        update_left_knee(landmarks[26])
        update_right_ankle(landmarks[27])
        update_left_ankle(landmarks[28])

        if is_animation_on:
            scene.run_animations(head_shape)
            scene.run_animations(right_wrist_shape)
            scene.run_animations(left_wrist_shape)
            scene.run_animations(left_shoulder_shape)
            scene.run_animations(right_shoulder_shape)
            scene.run_animations(left_elbow_shape)
            scene.run_animations(right_elbow_shape)
            scene.run_animations(right_hip_shape)
            scene.run_animations(left_hip_shape)
            scene.run_animations(right_knee_shape)
            scene.run_animations(left_knee_shape)
            scene.run_animations(right_ankle_shape)
            scene.run_animations(left_ankle_shape)
        else:
            scene.update_objects([
                head_shape, 
            head_shape, 
                head_shape, 
            head_shape, 
                head_shape, 
                right_wrist_shape,
                left_wrist_shape,
                left_shoulder_shape,
                right_shoulder_shape,
                left_elbow_shape,
                right_elbow_shape,
                right_hip_shape,
                left_hip_shape,
                right_knee_shape,
                left_knee_shape,
                right_ankle_shape,
                left_ankle_shape
            ])

    

if __name__ == "__main__":
    scene.run_tasks()





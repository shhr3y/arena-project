import glob
from turtle import pos
from arena import *
from numpy import object_
import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

# pose_model = None
camera = None

scene = Scene(host="mqtt.arenaxr.org", scene="myfirstscene")

# parent_object = Object(object_id='parent')
right_wrist_shape = Sphere(
        object_id="right_wrist",
        scale=(0.2,0.2,0.2),
        color=(30,20,10),
        position=(0,0,0),
        persist=True,
        # parent = parent_object        
    )

left_wrist_shape = Sphere(
        object_id="left_wrist",
        scale=(0.2,0.2,0.2),
        color=(70,0,100),
        position=(0,0,0),
        persist=True,
        # parent = parent_object
    )

left_shoulder_shape = Sphere(
        object_id="left_shoulder",
        scale=(0.1,0.1,0.1),
        color=(0,180,55),
        position=(0,0,0),
        persist=True,
    )

right_shoulder_shape = Sphere(
        object_id="right_shoulder",
        scale=(0.1,0.1,0.1),
        color=(0,180,55),
        position=(0,0,0),
        persist=True,
    )

left_elbow_shape = Sphere(
        object_id="left_elbow",
        scale=(0.1,0.1,0.1),
        color=(0,180,55),
        position=(0,0,0),
        persist=True,
    )

right_elbow_shape = Sphere(
        object_id="right_elbow",
        scale=(0.1,0.1,0.1),
        color=(0,180,55),
        position=(0,0,0),
        persist=True,
    )


head_shape = Sphere(
        object_id="head",
        scale=(0.4,0.4,0.4),
        color=(0,255,255),
        position=(0,0,0),
        persist=True,
    )

global_landmarks = []

animation_key = 200

# update_box(landmarks[0])

@scene.run_once
def init():
    print('run_once')
    global camera
    global pose_model
    camera = cv2.VideoCapture(0)
    # cv2.imshow('MediaPipe Pose', cv2.flip(camera.read()[1], 1))
    # with mp_pose.Pose(
    #     min_detection_confidence=0.5,
    #     min_tracking_confidence=0.5) as pose:
    #         pose_model = pose
            
    add_shapes()
    

@scene.run_forever(interval_ms=animation_key)
def update():
    # print('run_forever')
    # global mp_pose
    global camera
    # global pose_model
    if camera is not None and camera.isOpened():
        success, image = camera.read()
        # print(image)
        if image is not None and success:
            with mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as pose:
                # To improve performance, optionally mark the image as not writeable to
                # pass by reference.
                image.flags.writeable = False
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

                results = pose.process(image)

                # Draw the pose annotation on the image.
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                mp_drawing.draw_landmarks(
                    image,
                    results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS,
                    landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

                landmarks = []
                # print('received landmarks')
                for data_point in results.pose_world_landmarks.landmark:
                    landmarks.append((data_point.x, data_point.y, data_point.z))
                
            update_skeleton(landmarks)

            # Flip the image horizontally for a selfie-view display.
            # cv2.imshow('MediaPipe Pose', image)
        else:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            
        # camera.release()

    if len(global_landmarks) != 0:
        update_head(global_landmarks[0])
        update_right_wrist(global_landmarks[15])
        update_left_wrist(global_landmarks[16])
        update_right_shoulder(global_landmarks[11])
        update_left_shoulder(global_landmarks[12])
        update_right_elbow(global_landmarks[13])
        update_left_elbow(global_landmarks[14])

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
        #     right_shoulder_shape
        # ])
    pass

def add_shapes():
    scene.add_object(right_wrist_shape)
    scene.add_object(left_wrist_shape)
    scene.add_object(head_shape)
    scene.add_object(left_shoulder_shape)
    scene.add_object(right_shoulder_shape)
    scene.add_object(left_elbow_shape)
    scene.add_object(right_elbow_shape)
    
def update_skeleton(landmarks):
    global global_landmarks
    global_landmarks = landmarks

def update_head(coordinates):
    obj = head_shape
    curr_pos = obj.data.position
    obj.dispatch_animation(
        Animation(
                    property="position",
                    start=curr_pos,
                    end=get_position(coordinates),
                    easing="linear",
                    dur=animation_key
                )
    )
    obj.update_attributes(position=get_position(coordinates))

def update_right_wrist(coordinates):
    curr_pos = right_wrist_shape.data.position
    right_wrist_shape.dispatch_animation(
        Animation(
                    property="position",
                    start=curr_pos,
                    end=get_position(coordinates),
                    easing="linear",
                    dur=animation_key
                )
    )
    right_wrist_shape.update_attributes(position=get_position(coordinates))

def update_left_wrist(coordinates):
    curr_pos = left_wrist_shape.data.position
    left_wrist_shape.dispatch_animation(
        Animation(
                    property="position",
                    start=curr_pos,
                    end=get_position(coordinates),
                    easing="linear",
                    dur=animation_key
                )
    )
    left_wrist_shape.update_attributes(position=get_position(coordinates))

def update_left_shoulder(coordinates):
    curr_pos = left_shoulder_shape.data.position
    left_shoulder_shape.dispatch_animation(
        Animation(
                    property="position",
                    start=curr_pos,
                    end=get_position(coordinates),
                    easing="linear",
                    dur=animation_key
                )
    )
    left_shoulder_shape.update_attributes(position=get_position(coordinates))

def update_right_shoulder(coordinates):
    curr_pos = right_shoulder_shape.data.position
    right_shoulder_shape.dispatch_animation(
        Animation(
                    property="position",
                    start=curr_pos,
                    end=get_position(coordinates),
                    easing="linear",
                    dur=animation_key
                )
    )
    right_shoulder_shape.update_attributes(position=get_position(coordinates))

def update_right_elbow(coordinates):
    curr_pos = right_elbow_shape.data.position
    right_elbow_shape.dispatch_animation(
        Animation(
                    property="position",
                    start=curr_pos,
                    end=get_position(coordinates),
                    easing="linear",
                    dur=animation_key
                )
    )
    right_elbow_shape.update_attributes(position=get_position(coordinates))

def update_left_elbow(coordinates):
    curr_pos = left_elbow_shape.data.position
    left_elbow_shape.dispatch_animation(
        Animation(
                    property="position",
                    start=curr_pos,
                    end=get_position(coordinates),
                    easing="linear",
                    dur=animation_key
                )
    )
    left_elbow_shape.update_attributes(position=get_position(coordinates))

multplier = 3
def get_position(coordinates):
    return Position(multplier*coordinates[0], -multplier*coordinates[1], multplier*coordinates[2])

    

if __name__ == "__main__":
    scene.run_tasks()





from arena import *

scene = Scene(host="mqtt.arenaxr.org", scene="myfirstscene")

skeleton = Object(object_id)

right_wrist_shape = Sphere(
        object_id="right_wrist",
        scale=(0.2,0.2,0.2),
        color=(30,20,10),
    )
left_wrist_shape = Sphere(
        object_id="left_wrist",
        scale=(0.2,0.2,0.2),
        color=(70,0,100),
    )

head_shape = Sphere(
        object_id="head",
        scale=(0.4,0.4,0.4),
        color=(0,255,255),
    )



# update_box(landmarks[0])

@scene.run_once
def add_shapes():
    scene.add_object(right_wrist_shape)
    scene.add_object(left_wrist_shape)
    scene.add_object(head_shape)

def update_skeleton(landmarks):
    update_head(landmarks[0])
    update_right_wrist(landmarks[15])
    update_left_wrist(landmarks[16])

def update_head(coordinates):
    head_shape.update_attributes(position=get_position(coordinates))
    scene.update_object(head_shape)

def update_right_wrist(coordinates):
    right_wrist_shape.update_attributes(position=get_position(coordinates))
    scene.update_object(right_wrist_shape)

def update_left_wrist(coordinates):
    left_wrist_shape.update_attributes(position=get_position(coordinates))
    scene.update_object(left_wrist_shape)

multplier = 3
def get_position(coordinates):
    return Position(multplier*coordinates[0], -multplier*coordinates[1], multplier*coordinates[2])

    

if __name__ == "__main__":
    scene.run_tasks()





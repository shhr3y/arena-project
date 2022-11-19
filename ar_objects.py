from arena import *

animation_key = 250
is_animation_on = False

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
right_hip_shape = Sphere(object_id="right_hip", scale=(0.1,0.1,0.1), color=(0,180,55), position=(0,0,0), persist=True)
left_hip_shape = Sphere(object_id="left_hip", scale=(0.1,0.1,0.1), color=(0,180,55), position=(0,0,0), persist=True)

left_knee_shape = Sphere(object_id="left_knee", scale=(0.1,0.1,0.1), color=(0,180,55), position=(0,0,0), persist=True)
right_knee_shape = Sphere(object_id="right_knee", scale=(0.1,0.1,0.1), color=(0,180,55), position=(0,0,0), persist=True)

left_ankle_shape = Sphere(object_id="left_ankle", scale=(0.1,0.1,0.1), color=(0,180,55), position=(0,0,0), persist=True)
right_ankle_shape = Sphere(object_id="right_ankle", scale=(0.1,0.1,0.1), color=(0,180,55), position=(0,0,0), persist=True)


multplier = 3
def get_position(coordinates):
    return Position(multplier*coordinates[0], -multplier*coordinates[1], multplier*coordinates[2])


def update_head(coordinates):
    if is_animation_on:
        curr_pos = head_shape.data.position
        head_shape.dispatch_animation(
            Animation(
                        property="position",
                        start=curr_pos,
                        end=get_position(coordinates),
                        easing="linear",
                        dur=animation_key
                    )
        )

    head_shape.update_attributes(position=get_position(coordinates))

def update_right_wrist(coordinates):
    if is_animation_on:
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
    if is_animation_on:
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
    if is_animation_on:
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
    if is_animation_on:
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
    if is_animation_on:
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
    if is_animation_on:
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


def update_right_knee(coordinates):
    if is_animation_on:
        curr_pos = right_knee_shape.data.position
        right_knee_shape.dispatch_animation(
            Animation(
                        property="position",
                        start=curr_pos,
                        end=get_position(coordinates),
                        easing="linear",
                        dur=animation_key
                    )
        )

    right_knee_shape.update_attributes(position=get_position(coordinates))

def update_left_knee(coordinates):
    if is_animation_on:
        curr_pos = left_knee_shape.data.position
        left_knee_shape.dispatch_animation(
            Animation(
                        property="position",
                        start=curr_pos,
                        end=get_position(coordinates),
                        easing="linear",
                        dur=animation_key
                    )
        )

    left_knee_shape.update_attributes(position=get_position(coordinates))

def update_right_ankle(coordinates):
    if is_animation_on:
        curr_pos = right_ankle_shape.data.position
        right_ankle_shape.dispatch_animation(
            Animation(
                        property="position",
                        start=curr_pos,
                        end=get_position(coordinates),
                        easing="linear",
                        dur=animation_key
                    )
        )

    right_ankle_shape.update_attributes(position=get_position(coordinates))

def update_left_ankle(coordinates):
    if is_animation_on:
        curr_pos = left_ankle_shape.data.position
        left_ankle_shape.dispatch_animation(
            Animation(
                        property="position",
                        start=curr_pos,
                        end=get_position(coordinates),
                        easing="linear",
                        dur=animation_key
                    )
        )

    left_ankle_shape.update_attributes(position=get_position(coordinates))

def update_right_hip(coordinates):
    if is_animation_on:
        curr_pos = right_hip_shape.data.position
        right_hip_shape.dispatch_animation(
            Animation(
                        property="position",
                        start=curr_pos,
                        end=get_position(coordinates),
                        easing="linear",
                        dur=animation_key
                    )
        )

    right_hip_shape.update_attributes(position=get_position(coordinates))

def update_left_hip(coordinates):
    if is_animation_on:
        curr_pos = left_hip_shape.data.position
        left_hip_shape.dispatch_animation(
            Animation(
                        property="position",
                        start=curr_pos,
                        end=get_position(coordinates),
                        easing="linear",
                        dur=animation_key
                    )
        )

    left_hip_shape.update_attributes(position=get_position(coordinates))


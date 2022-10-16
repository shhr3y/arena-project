import eventlet
import socketio
import json
import mediapipe as mp
from arena import *

host = '192.168.0.106'
port = 9876	

mp_pose = mp.solutions.pose

scene = Scene(host="mqtt.arenaxr.org", scene="myfirstscene")

# sio = socketio.Server(cors_allowed_origins="*", async_mode='eventlet')
sio = socketio.AsyncServer()
# app = socketio.WSGIApp(sio)
app = socketio.ASGIApp(sio)

@sio.on('connect')
def connect(*args):
    print('SERVER CONNECTED TO', args[0])

@sio.on('landmarks')
def ping(*args):
    landmarks = args[1]
    json_list = []
    for landmark in landmarks:
        json_object = json.loads(landmark)
        json_object.pop("index", None)
        json_object.pop("isRemoved", None)
        json_object.pop("presence", None)
        json_list.append(json_object)

    sio.emit('render', {'data': json_list})
    update_box(landmarks[0])

box = Box(object_id="my_box")

@scene.run_once
def make_box():
    scene.add_object(box)


def update_box(coordinates):
    pos = Position((coordinates))
    box.update_attributes(position=pos)

    scene.update_object(box)



if __name__ == '__main__':
    scene.run_tasks()
    eventlet.wsgi.server(eventlet.listen((host, port)), app)

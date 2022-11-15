import eventlet
import socketio
import json
import mediapipe as mp


host = '192.168.0.108'
port = 9876	

mp_pose = mp.solutions.pose


sio = socketio.Server(cors_allowed_origins="*", async_mode='eventlet')
app = socketio.WSGIApp(sio)

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


if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen((host, port)), app)

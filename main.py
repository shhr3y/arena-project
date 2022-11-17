import eventlet
import socketio
import json
import mediapipe as mp


host = '192.168.0.108'
port = 9876	

mp_pose = mp.solutions.pose

landmarkFile = 'landmarks.txt' 

sio = socketio.Server(cors_allowed_origins="*", async_mode='eventlet')
app = socketio.WSGIApp(sio)

@sio.on('connect')
def connect(*args):
    print('SERVER CONNECTED TO', args[0])

@sio.on('landmarks')
def ping(*args):
    landmarks = args[1]
    json_list = []
    arena_list = []
    for landmark in landmarks:
        json_object = json.loads(landmark)
        json_object.pop("index", None)
        json_object.pop("isRemoved", None)
        json_object.pop("presence", None)

        arena_obj = [json_object['x'], json_object['y'], json_object['z']]

        json_list.append(json_object)
        arena_list.append(arena_obj)

    sio.emit('render', {'data': json_list})

    with open(landmarkFile, 'w') as filetowrite:
      filetowrite.write(json.dumps(arena_list))


if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen((host, port)), app)

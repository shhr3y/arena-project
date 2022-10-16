import socketio

sio = socketio.Client()
print('Created socketio client')

@sio.event
def connect():
    print('connected to server')

@sio.event
def disconnect():
    print('disconnected from server')

@sio.on('render')
def render(*args):
    # landmarks = args[1]
    print(args)

sio.connect('ws://192.168.0.106:9876/')
sio.wait()











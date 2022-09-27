import eventlet
import socketio
import socket
import threading

host = '192.168.0.103'
port = 9876	

sio = socketio.Server(cors_allowed_origins="*", async_mode='eventlet')
app = socketio.WSGIApp(sio)


# def ping_in_intervals():
#     threading.Timer(5.0, ping_in_intervals).start()
#     print("send ping")
#     sio.emit('ping')


@sio.on('ping')
def ping(*args):
    print("received ping - send pong")
    sio.emit('pong')


# ping_in_intervals()
eventlet.wsgi.server(eventlet.listen((host, port)), app)




# import numpy as np
# import socket

# import sys

# host = socket.gethostbyname(socket.gethostname())
# port = 9876		


# class VideoStreamingTest(object):
#     def __init__(self, host, port):
#         print('Trying socket on', host, port)
#         try:
#             self.server_socket = socket.socket()
#         except socket.error as message:
#             print('Bind failed. Error Code : ' + str(message[0]) + ' Message ' + message[1])
#             sys.exit()
#         print('Bind successful on socket', host, port)
#         self.server_socket.bind((host, port))
#         self.server_socket.listen(0)
#         self.connection, self.client_address = self.server_socket.accept()

#         # self.connection = self.connection.makefile('rb')
#         self.host_name = socket.gethostname()
#         self.host_ip = socket.gethostbyname(self.host_name)


#         # self.streaming()

#     @socket.on('ping')
#     def ping(*args):
#         print("received ping - send pong")
#         socket.emit('pong')

#     def streaming(self):
#         try:
#             print("Host: ", self.host_name + ' ' + self.host_ip)
#             print("Connection from: ", self.client_address)
#             print("Streaming...")
#             print("Press 'q' to exit")

#             # need bytes here
#             stream_bytes = b' '
#             while True:
#                 stream_bytes += self.connection.read(1024)
#                 first = stream_bytes.find(b'\xff\xd8')
#                 last = stream_bytes.find(b'\xff\xd9')
#                 if first != -1 and last != -1:
#                     jpg = stream_bytes[first:last + 2]
#                     stream_bytes = stream_bytes[last + 2:]
#                     image = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
#                     cv2.imshow('image', image)

#                     if cv2.waitKey(1) & 0xFF == ord('q'):
#                         break
#         finally:
#             self.connection.close()
#             self.server_socket.close()


# if __name__ == '__main__':
#     # host, port
#     VideoStreamingTest(host, port)
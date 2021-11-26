from utils import request
import socket
req = request.Request(url='http://localhost:5001', text='Hello there...')
s = socket.socket()
host = '127.0.0.1'
port = 5001
s.connect((host, port))
print(req.to_raw())
s.sendall(bytes(req.to_raw(), 'utf-8'))
print(s.recv(1024))
s.close()

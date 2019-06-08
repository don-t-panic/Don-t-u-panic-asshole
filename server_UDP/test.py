import socket
import time
import json
import pickle
import random

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(6)
auth_key = random.randrange(5, 100)
nick = random.randrange(5, 100)
message = {
    "auth_key": str(auth_key),
    "type": "1",
    "data": [str(nick)]
}
msg = pickle.dumps(json.dumps(message))
addr = ("127.0.0.1", 7070)

client_socket.sendto(msg, addr)
data, server = client_socket.recvfrom(4096)
print(f"Data received after login: {data}")
time.sleep(1)
message = {
    "auth_key": str(auth_key),
    "type": "2",
    "data": [4000, 100]
}
msg = pickle.dumps(json.dumps(message))
client_socket.sendto(msg, addr)
data, server = client_socket.recvfrom(4096)
print(f"Data received after position change: {data}")

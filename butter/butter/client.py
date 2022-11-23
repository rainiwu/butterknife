import zmq
from manifest import manifest
import time

context = zmq.Context()

#  Socket to talk to server
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

#  Do 10 requests, waiting each time for a response
for request in range(10):
    print(f"Sending request {request} ...")
    socket.send("Get manifest")
    m_received = socket.recv()
    print(f"Received reply {request} [ {m_received} ]")
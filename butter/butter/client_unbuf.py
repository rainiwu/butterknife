from asyncio.windows_events import NULL
import zmq
from manifest import manifest
import time

context = zmq.Context()

#  Socket to talk to server
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

print(f"Sending manifest request ...")
socket.send("GET manifest 0")
m_received = socket.recv()
start = time.time()
print(f"Received reply [ {m_received} ]")

stall_time = 0
qoe = 100

while 1:
    socket.send("GET unbuffered ", qoe)
    frame_received = socket.recv()

    if(frame_received == NULL):
        stall_start = time.time()
    else: stall_end = time.time()
                                                                                                                                                                                                                                        
    stall_time = stall_time + (stall_end - stall_start)

    end = time.time()
    total_time = end - start

    qoe = (1 - (stall_time/total_time)) * 100
    socket.send(qoe)
    
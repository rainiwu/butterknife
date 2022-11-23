#
#   Video Server
#

import time
import string
import os
import zmq
from manifest import manifest
import re

MAN_REQ_BUFF = "GET manifest buffered"
MAN_REQ_UNBUFF = "GET manifest 0"
BUFF_REQ = "GET buffered"
UNBUFF_REQ = "GET unbuffered"

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")


# Dummy values for 100 second video. 
chunks = 25
framesPerChunk = 120
framesPerSecond = 30
# Average bytes per frame to be 10e3.
bytesPerFrame = 10


# QoE 
QoEunbuff = 100
QoEbuff = 100


while True:
    #  Wait for next request from client
    message = socket.recv()
    print(f"Message Received: {message}")

    if message.decode("utf-8") == MAN_REQ_UNBUFF:
        # For buffered video, send the buffered manifest. 
        mani = manifest(chunks, 1, framesPerSecond, 0)
        socket.send_pyobj(mani)
        print(f"Unbuffered Manifest Sent")
    elif message.decode("utf-8") == MAN_REQ_BUFF:
        # For buffered video, send the buffered manifest. 
        mani = manifest(chunks, framesPerChunk, framesPerSecond, 1)
        socket.send_pyobj(mani)
        print(f"Buffered Manifest Sent")
    elif UNBUFF_REQ in message.decode("utf-8") :
        socket.send(os.urandom(1*bytesPerFrame))
        QoEunbuff = message.decode("utf-8").split()[-1]
        print(f"Unbuffered Chunk Sent, QoE = {QoEunbuff}")
    elif BUFF_REQ in message.decode("utf-8") :
        socket.send(os.urandom(framesPerChunk*bytesPerFrame))
        QoEbuff = message.decode("utf-8").split()[-1]
        print(f"Buffered Chunk Sent, QoE = {QoEbuff}")

    


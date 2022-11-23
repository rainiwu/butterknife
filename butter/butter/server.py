#
#   Video Server
#

import time
import string
import os
import zmq
import manifest
import re

MAN_REQ_BUFF = "GET manifest buffered"
MAN_REQ_UNBUFF = "GET manifest unbuffered"
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
bytesPerFrame = 10000


# QoE 
QoEunbuff = 100
QoEbuff = 100


while True:
    #  Wait for next request from client
    message = socket.recv()

    if message == MAN_REQ_UNBUFF:
        # For buffered video, send the buffered manifest. 
        mani = manifest(chunks, 1, framesPerSecond, 0)
        socket.send_pyobj(mani)
    elif message == MAN_REQ_BUFF:
        # For buffered video, send the buffered manifest. 
        mani = manifest(chunks, framesPerChunk, framesPerSecond, 1)
        socket.send_pyobj(mani)
    elif UNBUFF_REQ in message:
        socket.send(os.urandom(1*bytesPerFrame))
        QoEunbuff = re.findall("\d+", message)[0]
    elif BUFF_REQ in message:
        socket.send(os.urandom(framesPerChunk*bytesPerFrame))
        QoEunbuff = re.findall("\d+", message)[0]

#
#   Video Server
#

import time
import numpy
import string
import os
import zmq
import manifest
import re

MAN_REQ = "GET manifest"
INIT_REQ = "GET init"

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")


# Dummy values for 100 second video. 
chunks = 25
framesPerChunk = 120
frames = 30
# Average bytes per frame to be 10e3.
bytesPerFrame = 10000


# QoE 
QoE = 0


while True:
    #  Wait for next request from client
    message = socket.recv()

    if message == MAN_REQ:
        mani = manifest(chunks, framesPerChunk, frames)
        socket.send_pyobj(mani)
    elif INIT_REQ in message:
        socket.send(os.urandom(framesPerChunk*bytesPerFrame))
        QoE = re.findall("\d+", message)[0]
        
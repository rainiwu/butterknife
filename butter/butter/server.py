#
#   Video Server
#

import time
import string
import os
import zmq.asyncio
import asyncio
from manifest import manifest
import re


MAN_REQ_BUFF = "GET manifest buffered"
MAN_REQ_UNBUFF = "GET manifest unbuffered"
BUFF_REQ = "GET buffered"
UNBUFF_REQ = "GET unbuffered"

CHUNKS = 25
FRAMESPERCHUNK = 120
FRAMESPERSECOND = 30
BYTESPERFRAME = 10e3


class VideoServer:

    def __init__(self, address="tcp://*:5555", chunks = 25, framesPerChunk = 120, framesPerSecond = 30, bytesPerFrame = 10e3):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind(address)
        
        self.myChunks = chunks
        self.myFramesPerChunk = framesPerChunk
        self.myFramesPerSecond = framesPerSecond
        self.myBytesPerFrame = bytesPerFrame
        
        self.QoEbuff = 100
        self.QoEunbuff = 100
    
    async def run(self):
        while True:
            #  Wait for next request from client
            message = await self.socket.recv()
            print(f"Message Received: {message}")

            if message.decode("utf-8") == MAN_REQ_UNBUFF:
                #print(f"im not stupid!")
                # For buffered video, send the buffered manifest. 
                mani = manifest(self.myChunks, 1, self.myFramesPerSecond, 0)
                self.socket.send_pyobj(mani)
                print(f"Unbuffered Manifest Sent")
            elif message.decode("utf-8") == MAN_REQ_BUFF:
                # For buffered video, send the buffered manifest. 
                mani = manifest(self.mChunks, self.myFramesPerChunk, self.myFramesPerSecond, 1)
                self.socket.send_pyobj(mani)
                print(f"Buffered Manifest Sent")
            elif UNBUFF_REQ in message.decode("utf-8") :
                self.socket.send(os.urandom(1*self.bytesPerFrame))
                self.QoEunbuff = message.decode("utf-8").split()[-1]
                print(f"Unbuffered Chunk Sent, QoE = {self.QoEunbuff}")
            elif BUFF_REQ in message.decode("utf-8") :
                self.socket.send(os.urandom(self.framesPerChunk*self.bytesPerFrame))
                QoEbuff = message.decode("utf-8").split()[-1]
                print(f"Buffered Chunk Sent, QoE = {QoEbuff}")

    async def getQoE(self):
        return [self.QoEbuff , self.QoEunbuff]
        
        
if __name__ == '__main__':
    vidServ = VideoServer("tcp://*:5555", CHUNKS, FRAMESPERCHUNK, FRAMESPERSECOND, BYTESPERFRAME)
    vidServ.run()
   

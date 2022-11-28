#
#   Video Server
#

import time
import string
import os
import zmq.asyncio
import asyncio
from manifest import Manifest
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
        
        self.QoEdict = {}

        self.running = True
    
    async def streamer(self):
        while self.running:
            #  Wait for next request from client
            message = self.socket.recv()
            print(f"Message Received: {message}")

            if message.decode("utf-8") == MAN_REQ_UNBUFF:
                #print(f"im not stupid!")
                # For buffered video, send the buffered manifest. 
                mani = Manifest(self.myChunks, 1, self.myFramesPerSecond, 0)
                self.socket.send_pyobj(mani)
                print(f"Unbuffered Manifest Sent")
            elif message.decode("utf-8") == MAN_REQ_BUFF:
                # For buffered video, send the buffered manifest. 
                mani = Manifest(self.myChunks, self.myFramesPerChunk, self.myFramesPerSecond, 1)
                self.socket.send_pyobj(mani)
                print(f"Buffered Manifest Sent")
            elif UNBUFF_REQ in message.decode("utf-8") :
                self.socket.send(os.urandom(int(1*self.myBytesPerFrame)))
                self.QoEdict.update({"70": message.decode("utf-8").split()[-1]})
                print(f"Unbuffered Chunk Sent.")
            elif BUFF_REQ in message.decode("utf-8") :
                self.socket.send(os.urandom(int(self.myFramesPerChunk*self.myBytesPerFrame)))
                self.QoEdict.update({"71": message.decode("utf-8").split()[-1]})
                print(f"Buffered Chunk Sent.")
            else:
                print(f"Malformed request received.")

            print(f"Dictionary of QoEs:")
            print(self.QoEdict)

    async def getQoE(self):
        return self.QoEdict

    def run(self):
        loop = asyncio.new_event_loop()
        loop.create_task(self.streamer())
        try:
            loop.run_forever()
        finally: 
            self.running = False
        
        
if __name__ == '__main__':
    vidServ = VideoServer("tcp://*:5555", CHUNKS, FRAMESPERCHUNK, FRAMESPERSECOND, BYTESPERFRAME)
    vidServ.run()
   

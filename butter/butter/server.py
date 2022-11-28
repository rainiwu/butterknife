#
#   Video Server
#

import time
import string
import os
import zmq
import zmq.asyncio
import asyncio
from manifest import Manifest


MAN_REQ_BUFF = "GET manifest buffered"
MAN_REQ_UNBUFF = "GET manifest unbuffered"
BUFF_REQ = "GET buffered"
UNBUFF_REQ = "GET unbuffered"

QOE_DICT_REQ = "GET qoedict"

CHUNKS = 25
FRAMESPERCHUNK = 120
FRAMESPERSECOND = 30
BYTESPERFRAME = 10e3


class VideoServer:

    def __init__(self, address="tcp://*:5555", chunks = 25, framesPerChunk = 120, framesPerSecond = 30, bytesPerFrame = 10e3):
        # Create socket for clients
        self.context = zmq.asyncio.Context(1)
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind(address)

        # Create socket for talking to RL
        self.socketRL = self.context.socket(zmq.REP)
        self.socketRL.bind("tcp://*:5556")
        
        self.myChunks = chunks
        self.myFramesPerChunk = framesPerChunk
        self.myFramesPerSecond = framesPerSecond
        self.myBytesPerFrame = bytesPerFrame
        
        self.QoEdict = {}

        self.running = True

        print(f"Server Started")
    
    async def streamer(self) -> None:
        while self.running:
            #  Wait for next request from client
            message = await self.socket.recv()
            #print(f"Message Received: {message}")

            if message.decode("utf-8") == MAN_REQ_UNBUFF:
                #print(f"im not stupid!")
                # For buffered video, send the buffered manifest. 
                mani = Manifest(self.myChunks, 1, self.myFramesPerSecond, 0)
                await self.socket.send_pyobj(mani)
                print(f"Client Connected, Unbuffered Manifest Sent. ")
            elif message.decode("utf-8") == MAN_REQ_BUFF:
                # For buffered video, send the buffered manifest. 
                mani = Manifest(self.myChunks, self.myFramesPerChunk, self.myFramesPerSecond, 1)
                await self.socket.send_pyobj(mani)
                print(f"Client Connected, Buffered Manifest Sent")
            elif UNBUFF_REQ in message.decode("utf-8") :
                await self.socket.send(os.urandom(int(1*self.myBytesPerFrame)))
                self.QoEdict.update({"70": message.decode("utf-8").split()[-1]})
                #print(f"Unbuffered Chunk Sent.")
            elif BUFF_REQ in message.decode("utf-8") :
                await self.socket.send(os.urandom(int(self.myFramesPerChunk*self.myBytesPerFrame)))
                self.QoEdict.update({"71": message.decode("utf-8").split()[-1]})
                #print(f"Buffered Chunk Sent.")
            else:
                print(f"Malformed request received.")

            #print(f"Dictionary of QoEs:")
            #print(self.QoEdict)


    async def sendQoE(self) -> None:
        while self.running:
            #  Wait for next request from client
            message = await self.socketRL.recv()

            if message.decode("utf-8") == QOE_DICT_REQ:
                # Send the QoE dictionary
                await self.socketRL.send_pyobj(self.QoEdict)
                print(f"Dictionary Sent to Model:")
                print(self.QoEdict)
        

    def run(self):
        loop = asyncio.new_event_loop()
        loop.create_task(self.streamer())
        loop.create_task(self.sendQoE())
        try:
            loop.run_forever()
        finally: 
            self.running = False
        
        
if __name__ == '__main__':
    vidServ = VideoServer("tcp://*:5555", CHUNKS, FRAMESPERCHUNK, FRAMESPERSECOND, BYTESPERFRAME)
    vidServ.run()
   

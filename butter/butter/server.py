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
import csv
import datetime
import argparse


class VideoServer:

    MAN_REQ_BUFF = "GET manifest buffered"
    MAN_REQ_UNBUFF = "GET manifest unbuffered"
    BUFF_REQ = "GET buffered"
    UNBUFF_REQ = "GET unbuffered"

    QOE_DICT_REQ = "GET qoedict"
    QOE_GET_NUM = "GET quantity"

    ADDRESS = "tcp://*:5555"
    CHUNKS = 25
    FRAMESPERCHUNK = 120
    FRAMESPERSECOND = 30
    BYTESPERFRAME = 10e3

    NUMBER_OF_CLIENTS = 2

    def __init__(self, address = ADDRESS, chunks = CHUNKS, framesPerChunk = FRAMESPERCHUNK, framesPerSecond = FRAMESPERSECOND, bytesPerFrame = BYTESPERFRAME, numClients = NUMBER_OF_CLIENTS):
        # Create socket for clients
        self.context = zmq.asyncio.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind(address)

        # Create socket for talking to RL
        self.socketRL = self.context.socket(zmq.REP)
        self.socketRL.bind("tcp://*:5556")
        
        self.myChunks = chunks
        self.myFramesPerChunk = framesPerChunk
        self.myFramesPerSecond = framesPerSecond
        self.myBytesPerFrame = bytesPerFrame
        self.myNumClients = numClients
        
        self.QoEdict = {}

        self.running = True

        self.csvName = "QoEcsv_" + datetime.datetime.today().strftime('%Y-%m-%d_%H-%M-%S') + ".csv"
        self.QoEcsv = open(self.csvName,'a')
        self.QoEcsvWriter = csv.writer(self.QoEcsv)
        self.StartingTime = time.time()
        self.firstTimeDictReq = True

        print(f"Server Started")

    
    async def streamer(self) -> None:
        while self.running:
            #  Wait for next request from client
            message = await self.socket.recv()
            #print(f"Message Received: {message}")
            messageDecoded = message.decode("utf-8")

            # Manifest sending depending on request
            if self.MAN_REQ_UNBUFF in messageDecoded:
                #print(f"im not stupid!")
                # For buffered video, send the buffered manifest. 
                mani = Manifest(self.myChunks, 1, self.myFramesPerSecond, 0)
                await self.socket.send_pyobj(mani)
                print(f"Client Connected, Unbuffered Manifest Sent. ")
            elif self.MAN_REQ_BUFF in messageDecoded:
                # For buffered video, send the buffered manifest. 
                mani = Manifest(self.myChunks, self.myFramesPerChunk, self.myFramesPerSecond, 1)
                await self.socket.send_pyobj(mani)
                print(f"Client Connected, Buffered Manifest Sent")

            # Sending video depending on request
            elif self.UNBUFF_REQ in messageDecoded:
                await self.socket.send(os.urandom(int(1*self.myBytesPerFrame)))
                splitMessage = messageDecoded.split()
                self.QoEdict.update({splitMessage[-2]: splitMessage[-1]})
                #print(f"Unbuffered Chunk Sent.")
            elif self.BUFF_REQ in messageDecoded:
                await self.socket.send(os.urandom(int(self.myFramesPerChunk*self.myBytesPerFrame)))
                splitMessage = messageDecoded.split()
                self.QoEdict.update({splitMessage[-2]: splitMessage[-1]})
                #print(f"Buffered Chunk Sent.")

            # If the request doesn't match any of the expected forms, don't use.
            else:
                print(f"Malformed request received.")

            #print(f"Dictionary of QoEs:")
            #print(self.QoEdict)


    async def sendQoE(self) -> None:
        while self.running:
            #  Wait for next request from client
            message = await self.socketRL.recv()
            messageDecoded = message.decode("utf-8")

            #print("QoE Request Received")

            if messageDecoded == self.QOE_GET_NUM:
                if len(self.QoEdict) == self.myNumClients:
                    await self.socketRL.send_string(str(self.myNumClients))
                else:
                    await self.socketRL.send_string("-1")
            
            if messageDecoded == self.QOE_DICT_REQ:
                # Write QoE data to CSV
                if self.firstTimeDictReq:
                    self.QoEcsvWriter.writerow(["Time"] + list(self.QoEdict.keys()))
                    self.StartingTime = time.time()
                    self.firstTimeDictReq = False
                self.QoEcsvWriter.writerow([time.time() - self.StartingTime] + list(self.QoEdict.values()))

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
    parser = argparse.ArgumentParser(
        prog="VideoServer",
        description="Simulates a video serving application",
    )
    parser.add_argument("--ip", default="*")
    parser.add_argument("--ch", default="25")
    parser.add_argument("--fpc", default="120")
    parser.add_argument("--fps", default="30")
    parser.add_argument("--bpf", default="10000")
    parser.add_argument("--nc", default="4")
    args = parser.parse_args()

    """
    vidServ = VideoServer(
        address = "tcp://" + args.ip + ":5555",
        chunks = int(args.ch),
        framesPerChunk = int(args.fpc),
        framesPerSecond = int(args.fps),
        bytesPerFrame = int(args.bpf),
        numClients = int(args.nc)
    )
    """
    vidServ = VideoServer()
    
    try:
        vidServ.run()
    except:
        vidServ.QoEcsv.close()


   

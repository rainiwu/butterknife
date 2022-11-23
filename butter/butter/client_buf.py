import zmq
from manifest import manifest
import time
import asyncio
from multiprocessing import Process
BUFFER_SIZE = 100

class client_buffer():
    def __init__(self, address="tcp://localhost:5555", buffer_size=100):
        self.context = zmq.Context()
        #  Socket to talk to server
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect(address)
        print("Client connected to address: %s" % address)
        self.current_buffer = 0
        self.consume_index = 0
        self.occupied_buffer = 0
        self.max_buffer = buffer_size
        self.my_buffer = [buffer_size]
        self.stall_timer = 0
        self.BUFF_REQ = "GET buffered"
        self.MAN_REQ = "GET manifest"
    
    def start(self):
        self.socket.send_string(self.MAN_REQ)
        self.my_manifest = self.socket.recv()
        print("Received manifest from server")

    def run(self):
        while True:
            if self.occupied_buffer == self.max_buffer:
                self.stall_timer = 0
                print("Stalling: Too full")
                self.stall_run()

            self.socket.send_string(self.BUFF_REQ)
            reply = self.socket.recv()
            self.my_buffer[self.current_buffer] = reply
            print(f"Received reply {self.BUFF_REQ} [ {reply} ]")
            self.occupied_buffer += 1
            self.current_buffer = (self.current_buffer + 1) % self.max_buffer

    def consume(self):
        while True:
            if self.occupied_buffer == 0:
                self.stall_timer = 0
                print("Stalling: Starving")
                self.stall()

            consumed_info = self.my_buffer[self.consume_index]
            self.occupied_buffer -= 1
            print(f"Consume info {consumed_info}")
            time.sleep(1/self.my_manifest.frameRate)
            self.consume_index = (self.consume_index + 1) % self.max_buffer
            

    def stall_consume(self):
        while self.occupied_buffer == 0:
            self.stall_timer += 1
        print("Recover from stalling (consume) - Stall timer %d" % self.stall_timer)


    def stall_run(self):
        while self.occupied_buffer == self.max_buffer:
            self.stall_timer += 1
        print("Recover from stalling (run) - Stall timer %d" % self.stall_timer)

if __name__ == '__main__':
    cb = client_buffer("tcp://localhost:5555", BUFFER_SIZE)
    cb.start()

    # Create two processes
    run = Process(target=cb.run)
    consume = Process(target=cb.consume())

    run.start()
    consume.start()

    run.join()
    consume.join()

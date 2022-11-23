import zmq
from manifest import manifest
import time

BUFFER_SIZE = 100

class client_buffer():
    def __init__(self, address="tcp://localhost:5555", buffer_size=100):
        self.context = zmq.Context()
        #  Socket to talk to server
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect(address)
        print("Client connected to address: %s" % address)
        self.current_buffer = 1
        self.max_buffer = buffer_size
        self.my_buffer = [buffer_size]
        self.BUFF_REQ = "GET buffered"
        self.MAN_req = "GET manifest"
    
    def start(self):
        self.socket.send_string(self.MAN_REQ)
        self.my_manifest = self.socket.recv()
        print("Received manifest from server")

    def run(self):
        self.start()
        while True:
            self.socket.send_string(self.BUFF_REQ)
            reply = self.socket.recv()
            self.my_buffer[self.current_buffer] = reply
            print(f"Received reply {self.BUFF_REQ} [ {reply} ]")
            self.current_buffer = (self.current_buffer + 1) % self.max_buffer





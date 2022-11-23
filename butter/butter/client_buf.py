import zmq
from manifest import manifest
import time

MAN_REQ = "GET manifest"
BUFF_REQ = "GET buffered"
BUFFER_SIZE = 100

#  Do 10 requests, waiting each time for a response
#for request in range(10):
#    print(f"Sending request {request} ...")
#    socket.send_string("Get manifest")
#    m_received = socket.recv()
#    print(f"Received reply {request} [ {m_received} ]")



class client_buffer():
    def __init__(self, address="tcp://localhost:5555", buffer_size=BUFFER_SIZE):
        self.context = zmq.Context()
        #  Socket to talk to server
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect(address)
        print("Client connected to address: %s" % address)
        self.current_buffer = 1
        self.max_buffer = buffer_size
        self.my_buffer = [buffer_size]
    
    def start(self):
        self.socket.send_string(MAN_REQ)
        self.my_manifest = self.socket.recv()
        print("Received manifest from server")

    def run(self):
        self.start()
        while True:
            self.socket.send_string(BUFF_REQ)
            reply = self.socket.recv()
            self.my_buffer[self.current_buffer] = reply
            self.current_buffer = (self.current_buffer + 1) % self.max_buffer





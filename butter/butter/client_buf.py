import zmq
from manifest import manifest
from threading import Thread
import time
BUFFER_SIZE = 500
CONSUME_WAIT = 0.0001
class client_buffer():
    def __init__(self, address="tcp://localhost:5555", buffer_size=500, consume_wait=0.0001):
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
        self.BUFF_REQ = "GET buffered "
        self.MAN_REQ = "GET manifest buffered"
        self.client_timer = time.time()
        self.stall_timer = 0
        self.my_manifest = manifest()
        self.my_consume_wait = consume_wait
    
    def start(self):
        self.socket.send_string(self.MAN_REQ)
        self.my_manifest = self.socket.recv()
        print("Received manifest from server")

    def run(self):
        while True:
            if self.occupied_buffer == self.max_buffer:
                self.stall_run()
            self.socket.send_string(self.BUFF_REQ + str(self.calculate_QoE()))
            reply = self.socket.recv()
            self.my_buffer[self.current_buffer] = reply
            print(f"Received reply ")#{self.BUFF_REQ} [ {reply} ]")
            self.occupied_buffer += 1
            self.current_buffer = (self.current_buffer + 1) % len(self.my_buffer)

    def consume(self):
        while True:
            if self.occupied_buffer == 0:
                self.stall_consume()
            consumed_info = self.my_buffer[self.consume_index]
            self.occupied_buffer -= 1
            time.sleep(self.my_consume_wait)
            print(f"Consume info ")#{consumed_info}")
            self.consume_index = (self.consume_index + 1) % len(self.my_buffer)

    def stall_consume(self):
        print("Stalling due too empty buffer for consume")
        start = time.time()
        while self.occupied_buffer == 0:
            continue
        end = time.time()
        self.stall_timer += end - start
        print("Recover from stalling (consume) - Stall timer %d" % self.stall_timer)


    def stall_run(self):
        start = time.time()
        print("Stalling due too full buffer for load")
        while self.occupied_buffer == self.max_buffer:
            continue
        end = time.time()
        print("Recover from stalling (run) - Stall timer %d" % self.stall_timer)
        self.stall_timer += end - start

    def calculate_QoE(self):
        total_time = time.time() - self.client_timer
        stall_time = self.stall_timer
        QoE = (1 - stall_time /total_time) * 100
        return QoE

if __name__ == '__main__':
    cb = client_buffer("tcp://localhost:5555", BUFFER_SIZE, CONSUME_WAIT)
    cb.start()
    a = Thread(target=cb.run)
    b = Thread(target=cb.consume)
    a.start()
    b.start()
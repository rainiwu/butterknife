import time
class client_simulation:
    def __init__(self, buffer=True, FRAME_TIME=0.016):
        if buffer:
            self.buffer_size = 500
        else:
            self.buffer_size = 1
        self.buffer = [self.buffer_size]
        self.entry_num = 0
        self.begin_time = time.time()
        self.stall_time = 0
        self.frame_time = FRAME_TIME
        self.recovery_time = FRAME_TIME
        self.counter_for_consume = 0
        self.counter_for_fill = 0
        self.consumed = 0
        self.last_timestamp_consume = time.time()
        self.last_timestamp_fill = time.time()
        

    def fill_buffer(self):
        if len(self.buffer) < self.buffer_size:
            self.buffer.append(1)

    def consume_buffer(self):
        if self.consumed > 0 and len(self.buffer) == 0:
            self.stall_time += time.time() - self.last_timestamp_consume
        self.counter_for_consume += 0.001
        while self.counter_for_consume >= self.frame_time and len(self.buffer) != 0:
            self.buffer.pop()
            self.consumed += 1
            self.counter_for_consume = 0
        self.last_timestamp_consume = time.time()

    def calculate_QoE(self):
        return (1 - self.stall_time/self.return_current_time()) * 100

    def return_current_time(self):
        return time.time() - self.begin_time
        
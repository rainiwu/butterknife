import zmq
import zmq.asyncio
import asyncio

RUN_INDEFINITE = False
class rl_interface:
    def __init__(self, address: str = "tcp://localhost:5557"):
        # Initialize socket
        self.context: zmq.asyncio.Context = zmq.asyncio.Context(1)
        self.socket: zmq.asyncio.Socket = self.context.socket(zmq.REQ)
        self.socket.connect(address)
        self.prioritized_id = "Undecided"

    async def get_priority(self):
        await self.socket.send_string("GET priority")
        print("Priority request sent")
        reply = await self.socket.recv_string()
        if reply != "Unrecognize request":
            self.prioritized_id = reply
            print(self.prioritized_id)
        else:
            print("Request unrecognized")

    def run(self):
        l1 = asyncio.new_event_loop()
        l1.run_until_complete(self.get_priority())
        l1.close()

rli = rl_interface("tcp://localhost:5557")
rli.run()

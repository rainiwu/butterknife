import zmq
import zmq.asyncio
import asyncio

ADDR = "ipc:///dev/shm/priorities"


class rl_interface:
    def __init__(
        self,
        address: str = "tcp://localhost:5557",
        address_srs="ipc:///dev/shm/priorities",
    ):
        # Initialize socket
        self.context: zmq.asyncio.Context = zmq.asyncio.Context(1)
        self.socket: zmq.asyncio.Socket = self.context.socket(zmq.REQ)
        self.socket_srs: zmq.asyncio.Socket = self.context.socket(zmq.PUB)
        self.socket.connect(address)
        self.socket_srs.bind(address_srs)

        self.prioritized_id = "70"

    async def get_priority(self):
        while True:
            await self.socket.send_string("GET priority")
            print("Priority request sent")
            reply = await self.socket.recv_string()
            if reply != "Unrecognize request":
                self.prioritized_id = reply
                print(self.prioritized_id)
            else:
                print("Request unrecognized")

    async def report_prioirty(self):
        while True:
            await self.socket_srs.send(int(self.prioritized_id).to_bytes(4, "little"))
            await asyncio.sleep(0.001)
            print("Priority sent to srsRAN: " + self.prioritized_id)
            print(int(self.prioritized_id).to_bytes(4, "little"))

    def run(self):
        loop = asyncio.new_event_loop()
        loop.create_task(self.get_priority())
        loop.create_task(self.report_prioirty())
        loop.run_forever()


rli = rl_interface("tcp://localhost:5557", "ipc:///dev/shm/priorities")
rli.run()

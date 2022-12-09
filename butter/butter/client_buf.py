from manifest import Manifest

import zmq
import zmq.asyncio
import asyncio
import time

import logging
import argparse
from typing import List


class BufferedClient:
    LOGGER = logging.getLogger(name="BufferedClient")
    FRAME_TIME: float = 0.016  # seconds
    RECOVERY_TIME: float = FRAME_TIME  # seconds
    BUFFER_SIZE: int = 500  # number of chunks

    def __init__(
        self,
        address: str = "tcp://localhost:5555",
        frame_time: float = FRAME_TIME,
        recovery_time: float = RECOVERY_TIME,
        buffer_size: int = BUFFER_SIZE,
        unbuffer: bool = True,
        id: str = "70"
    ) -> None:
        self.context: zmq.asyncio.Context = zmq.asyncio.Context(1)
        #  Socket to talk to server
        self.socket: zmq.asyncio.Socket = self.context.socket(zmq.REQ)
        self.socket.connect(address)
        self.LOGGER.info(f"connected to {address}")
        self.unbuffer = unbuffer
        self.id = id
        self.max_buffer: int = buffer_size
        self.buffer: List[bytes] = []

        if self.unbuffer:
            self.BUFF_REQ: str = "GET unbuffered " + self.id + " "
            self.MAN_REQ: str = "GET manifest unbuffered"
        else:
            self.BUFF_REQ: str = "GET buffered " + self.id + " "
            self.MAN_REQ: str = "GET manifest buffered"
        self.manifest: Manifest = Manifest()

        # metrics for qoe calculation
        self.stall_events: int = 0
        self.consume_events: int = 0
        self.frame_time = frame_time
        self.recovery_time = recovery_time

        self.stay_alive: bool = True
        
        self.LOGGER.info("created new client")
        self.LOGGER.info(f"frame time: {frame_time} ms")
        self.LOGGER.info(f"recovery time: {recovery_time} ms")
        self.LOGGER.info(
            f"buffer size: {buffer_size} chunks; {buffer_size * frame_time * 1e3} ms"
        )

    async def setup(self) -> None:
        """
        obtains the video manifest from the server
        """
        await self.socket.send_string(self.MAN_REQ)
        self.manifest = await self.socket.recv_pyobj()
        if not isinstance(self.manifest, Manifest):
            self.LOGGER.critical("received malformed Manifest from server")
            raise TypeError
        # TODO: frame time can be derived from manifest information
        self.LOGGER.info("received Manifest from server")

    def run(self) -> None:
        asyncio.run(self.setup())
        loop = asyncio.new_event_loop()
        loop.create_task(self.fill_buffer())
        loop.create_task(self.consume_buffer())
        try:
            loop.run_forever()
        finally:
            self.stay_alive = False

    async def fill_buffer(self) -> None:
        """
        increases the buffer incrementally through a network request
        also sends qoe
        """

        while self.stay_alive:
            if len(self.buffer) == self.max_buffer or self.consume_events == 0:
                # wait for some time before next request if buffer is full
                await asyncio.sleep(self.frame_time)
                continue

            # request for a buffer, alongside current qoe
            await self.socket.send_string(self.BUFF_REQ + str(self.__calculate_qoe()))
            reply: bytes = await self.socket.recv(copy=True)
            self.buffer.append(reply)
            self.LOGGER.debug(f"received chunk of size {len(reply)}")

    async def consume_buffer(self) -> None:
        """
        decreases the buffer incrementally every frame_time
        """
        while self.stay_alive:
            self.consume_events += 1
            if len(self.buffer) == 0:
                self.__stall()
                # allow the application to recover from the stall
                await asyncio.sleep(self.recovery_time)
                self.LOGGER.info(f"done waiting for {self.recovery_time*1e3} ms")
                continue

            self.buffer.pop()
            await asyncio.sleep(self.frame_time)

    def __stall(self) -> None:
        self.stall_events += 1
        self.LOGGER.info(f"stall event {self.stall_events} detected")

    def __calculate_qoe(self) -> float:
        total_time: float = self.consume_events * self.frame_time
        stall_time: float = self.stall_events * self.recovery_time
        result: float = (1 - stall_time / total_time) * 100
        return result


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(
        prog="BufferedClient",
        description="Simulates a buffered video streaming application",
    )
    parser.add_argument("--ip", default="localhost")
    parser.add_argument("--ft", default="0.016")
    parser.add_argument("--rt", default="0.016")
    parser.add_argument("--bs", default="500")
    #parser.add_argument("--ub", default="False")
    parser.add_argument('--buffer', action='store_false')
    parser.add_argument('--unbuffer', dest='buffer', action='store_true')
    parser.set_defaults(buffer=False)
    parser.add_argument("--id", default="70")
    args = parser.parse_args()


    client = BufferedClient(
        address="tcp://" + args.ip + ":5555",
        frame_time=float(args.ft),
        recovery_time=float(args.rt),
        buffer_size=int(args.bs),
        unbuffer=bool(args.buffer),
        id=args.id
    )
    client.run()


if __name__ == "__main__":
    main()

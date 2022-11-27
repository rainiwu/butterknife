from manifest import Manifest

import zmq
import zmq.asyncio
import asyncio
import time
import logging
from contextlib import suppress

from typing import List

logging.basicConfig(level=logging.INFO)


class BufferedClient:
    BUFF_REQ: str = "GET buffered "
    MAN_REQ: str = "GET manifest buffered"
    LOGGER = logging.getLogger(name="BufferedClient")
    FRAME_TIME: float = 0.016  # seconds
    RECOVERY_TIME: float = FRAME_TIME  # seconds
    BUFFER_SIZE: int = 500  # number of chunks

    def __init__(
        self,
        address: str = "tcp://localhost:5555",
    ) -> None:
        self.context: zmq.asyncio.Context = zmq.asyncio.Context(1)
        #  Socket to talk to server
        self.socket: zmq.asyncio.Socket = self.context.socket(zmq.REQ)
        self.socket.connect(address)
        self.LOGGER.info(f"connected to {address}")

        self.max_buffer: int = self.BUFFER_SIZE
        self.buffer: List[bytes] = []

        self.manifest: Manifest = Manifest()

        # metrics for qoe calculation
        self.stall_events: int = 0
        self.consume_events: int = 0

        self.stay_alive: bool = True

    async def setup(self) -> None:
        """
        obtains the video manifest from the server
        """
        await self.socket.send_string(self.MAN_REQ)
        self.manifest = await self.socket.recv_pyobj()
        if not isinstance(self.manifest, Manifest):
            self.LOGGER.critical("received malformed Manifest from server")
            raise TypeError
        self.LOGGER.info("received Manifest from server")

    def run(self) -> None:
        asyncio.run(client.setup())
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
                await asyncio.sleep(self.FRAME_TIME)
                continue

            # request for a buffer, alongside current qoe
            await self.socket.send_string(self.BUFF_REQ + str(self.__calculate_qoe()))
            reply: bytes = await self.socket.recv(copy=True)
            self.buffer.append(reply)
            self.LOGGER.info(f"received chunk of size {len(reply)}")

    async def consume_buffer(self) -> None:
        """
        decreases the buffer incrementally every frame_time
        """
        while self.stay_alive:
            self.consume_events += 1
            if len(self.buffer) == 0:
                self.__stall()
                # allow the application to recover from the stall
                await asyncio.sleep(self.RECOVERY_TIME)
                self.LOGGER.info(f"done waiting for {self.RECOVERY_TIME*1e3} ms")
                continue

            self.buffer.pop()
            await asyncio.sleep(self.FRAME_TIME)

    def __stall(self) -> None:
        self.stall_events += 1
        self.LOGGER.info(f"stall event {self.stall_events} detected")

    def __calculate_qoe(self) -> float:
        total_time: float = self.consume_events * self.FRAME_TIME
        stall_time: float = self.stall_events * self.RECOVERY_TIME
        result: float = (1 - stall_time / total_time) * 100
        return result


if __name__ == "__main__":
    client = BufferedClient("tcp://localhost:5555")
    try:
        client.run()
    finally:
        pass

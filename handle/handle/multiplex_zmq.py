import zmq.asyncio
import numpy

import asyncio
import struct
import array

import logging
from typing import List


class ZmqMultiplexer:
    """
    given multiple zmq publishers, this class merges all into one
    the merge process is done by summation
    """

    LOGGER = logging.getLogger("ZmqMultiplexer")

    def __init__(self, output_address: str) -> None:
        self.context = zmq.asyncio.Context(1)
        self.out_socket = self.context.socket(zmq.REP)
        self.out_socket.bind(output_address)
        self.LOGGER.info(f"connected to {output_address}")

        self.input_sockets: List[zmq.asyncio.Socket] = []

        self.stay_alive: bool = True

    def setup(self, input_addresses: List[str]) -> None:
        for addr in input_addresses:
            new_socket = self.context.socket(zmq.REQ)
            new_socket.connect(addr)
            # new_socket.setsockopt_string(zmq.SUBSCRIBE, "")
            self.input_sockets.append(new_socket)
            self.LOGGER.info(f"connected to {addr}")

    def run(self) -> None:
        loop = asyncio.new_event_loop()

        async def process_forever():
            while self.stay_alive:
                await self.__process_sample()

        loop.create_task(process_forever())

        self.LOGGER.info("starting event loop")
        try:
            loop.run_forever()
        finally:
            loop.close()

    async def __process_sample(self) -> None:
        packets = numpy.array([], dtype=numpy.single)
        for socket in self.input_sockets:
            await socket.send_string("hello")
            val: bytes = await socket.recv(copy=True)  # type: ignore
            samples = numpy.frombuffer(val, dtype=numpy.single)
            if len(packets) == 0:
                packets = numpy.copy(samples)
                continue
            for index, sample in enumerate(samples):
                packets[index] += sample

        # self.LOGGER.info("waiting on out_socket")
        await self.out_socket.recv()
        await self.out_socket.send(packets.tobytes())
        # self.LOGGER.info(f"processed {len(packets.tobytes())} samples")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    input_addrs: List[str] = [
        "ipc:///dev/shm/srsue1_tx"
    ]  # , "ipc:///dev/shm/srsue2_tx"]
    mp = ZmqMultiplexer("ipc:///dev/shm/srsenb_rx")
    mp.setup(input_addrs)
    mp.run()

import zmq.asyncio

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
        self.out_socket = self.context.socket(zmq.PUB)
        self.out_socket.connect(output_address)
        self.LOGGER.info(f"connected to {output_address}")

        self.input_sockets: List[zmq.asyncio.Socket] = []

        self.stay_alive: bool = True

    def setup(self, input_addresses: List[str]) -> None:
        for addr in input_addresses:
            new_socket = self.context.socket(zmq.SUB)
            new_socket.connect(addr)
            new_socket.setsockopt_string(zmq.SUBSCRIBE, "")
            self.input_sockets.append(new_socket)
            self.LOGGER.info(f"connected to {addr}")

    def run(self) -> None:
        loop = asyncio.new_event_loop()

        async def process_forever():
            while self.stay_alive:
                await self.__process_sample()

        loop.create_task(process_forever())

        try:
            loop.run_forever()
        finally:
            loop.close()

    async def __process_sample(self) -> None:
        packets: List[float] = []
        result = array.array("f")
        for socket in self.input_sockets:
            self.LOGGER.info("receiving")
            val: List[bytes] = await socket.recv_multipart(copy=True)  # type: ignore
            self.LOGGER.info("converting")
            # convert to float
            result.frombytes(val[1])
            samples: List[float] = result.tolist()

            if len(packets) == 0:
                packets = samples
                continue
            for index, sample in enumerate(samples):
                packets[index] += sample

        result.fromlist(packets)
        await self.out_socket.send(result.tobytes())
        self.LOGGER.info("processed samples sent")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    input_addrs: List[str] = ["ipc:///dev/shm/srsue1_tx"]
    mp = ZmqMultiplexer("ipc:///dev/shm/srsenb_rx")
    mp.setup(input_addrs)
    mp.run()

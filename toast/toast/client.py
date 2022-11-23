import pytun
import zmq
import zmq.asyncio

import asyncio

from typing import List


class Client:
    """
    lightweight Client-side of a toast tunnel
    """

    IPC_PREFIX: str = "ipc:///dev/shm/"
    HANDSHAKE_ADDR: str = IPC_PREFIX + "toast_hs"
    MTU: int = 1500

    def __init__(self, name: str = "toast_ue") -> None:
        self.name = name

        self.context = zmq.asyncio.Context(1)
        self.ip: str = asyncio.run(self.__get_ip(self.context))

        self.tun = pytun.TunTapDevice(name=name)
        self.tun.addr = self.ip
        self.tun.netmask = "255.255.255.0"
        self.tun.mtu = self.MTU
        self.tun.up()

        self.payload_queue: List[str] = []

    def process_outgoing(self) -> None:
        """
        reads a packet from the interface and sends it to the server
        """
        payload = self.tun.read(self.tun.mtu)
        self.send_sock: zmq.Socket = self.context.socket(zmq.REQ)
        self.send_sock.connect(self.IPC_PREFIX + self.ip + "_fromcli")

        async def push_payload():
            await self.send_sock.send_string(str(payload))
            await self.send_sock.recv()  # reset the socket

        asyncio.get_running_loop().create_task(push_payload())

    async def process_incoming(self) -> None:
        """
        gets a packet from the server and sends it to the interface
        """
        self.recv_sock: zmq.Socket = self.context.socket(zmq.REP)
        self.recv_sock.connect(self.IPC_PREFIX + self.ip + "_tocli")
        payload = await self.recv_sock.recv_string()
        print("received payload")
        self.payload_queue.append(str(payload))
        await self.recv_sock.send_string("done")  # reset the socket
        self.recv_sock.close()
        print("done")

    def write_to_tun(self) -> None:
        if len(self.payload_queue) > 0:
            self.tun.write(self.payload_queue.pop(0))
            print("wrote to tun")

    async def __get_ip(self, context: zmq.asyncio.Context) -> str:
        """
        obtains an IP address from the server

        :param context: a ZMQ context used to connect to the server
        :return: an ip address obtained from the server
        """
        socket: zmq.Socket = context.socket(zmq.REQ)
        print(f"connecting to {self.HANDSHAKE_ADDR}")
        socket.connect(self.HANDSHAKE_ADDR)
        await socket.send_string("handshake")
        print("sent handshake request, awaiting")
        result: str = await socket.recv_string()
        socket.close()
        print(f"received ip {result}")
        return result


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    client = Client()
    loop.add_reader(client.tun, client.process_outgoing)
    loop.add_writer(client.tun, client.write_to_tun)

    async def proc_incoming_forever(client: Client):
        while True:
            print("awaiting proc incoming")
            await client.process_incoming()

    loop.create_task(proc_incoming_forever(client))
    loop.run_forever()

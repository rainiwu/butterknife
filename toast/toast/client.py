import pytun
import zmq
import zmq.asyncio

import asyncio


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
        ip: str = asyncio.run(self.__get_ip(self.context))

        self.tun = pytun.TunTapDevice(name=name)
        self.tun.addr = ip
        self.tun.netmask = "255.255.255.0"
        self.tun.mtu = self.MTU
        self.tun.up()

        self.recv_sock: zmq.Socket = self.context.socket(zmq.REP)
        self.send_sock: zmq.Socket = self.context.socket(zmq.REQ)

        self.recv_sock.connect(self.IPC_PREFIX + ip + "_tocli")
        self.send_sock.connect(self.IPC_PREFIX + ip + "_fromcli")

    def process_outgoing(self) -> None:
        """
        reads a packet from the interface and sends it to the server
        """
        payload = self.tun.read(self.tun.mtu)
        self.send_sock.send_string(payload)
        self.send_sock.recv()  # reset the socket

    async def process_incoming(self) -> None:
        """
        gets a packet from the server and sends it to the interface
        """
        payload = await self.recv_sock.recv_string()
        self.tun.write(payload)
        self.recv_sock.send()  # reset the socket

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
    client = Client()
    loop = asyncio.new_event_loop()
    loop.add_reader(client.tun, client.process_outgoing)

    async def proc_incoming_forever(client: Client):
        while True:
            await client.process_incoming()

    loop.create_task(proc_incoming_forever(client))
    loop.run_forever()

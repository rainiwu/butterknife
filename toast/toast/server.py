import pytun
import zmq
import zmq.asyncio

import asyncio

from typing import Dict, Tuple


class Server:
    """
    configurable Server-side of a toast tunnel
    """

    IPC_PREFIX: str = "ipc:///dev/shm/"
    HANDSHAKE_ADDR: str = IPC_PREFIX + "toast_hs"
    MTU: int = 1500
    CLIENT_IP_PREFIX: str = "172.16.0."

    def __init__(
        self, ip: str = "172.16.0.1", name: str = "toast_ran"
    ) -> None:
        self.context = zmq.asyncio.Context(1)

        self.tun = pytun.TunTapDevice(name=name)
        self.tun.addr = ip
        self.tun.netmask = "255.255.255.0"
        self.tun.mtu = self.MTU
        self.tun.up()

        self.client_ip: int = 2

        # dict with key of client_ip, and value of (to_sock, from_sock)
        self.client_sockets: Dict[str, Tuple[zmq.Socket, zmq.Socket]] = {}

        self.payload_queue: List[str] = []

    # def handle_handshake(self) -> None:
    #     print("awaiting handshake")
    #     ctx = zmq.Context(1)
    #     sock = ctx.socket(zmq.REP)
    #     sock.bind(self.HANDSHAKE_ADDR)
    #     sock.recv()
    #     sock.send_string(self.CLIENT_IP_PREFIX + str(self.client_ip))
    #     print("done")

    async def handle_handshake(self) -> None:
        """
        handle a handshake request
        """
        self.handshake_sock: zmq.asyncio.Socket = self.context.socket(zmq.REP)
        print(f"binding to {self.HANDSHAKE_ADDR}")
        self.handshake_sock.bind(self.HANDSHAKE_ADDR)
        print("awaiting handshake")
        await self.handshake_sock.recv()  # get some empty request
        print("received handshake")
        self.__initialize_client(self.client_ip)
        await self.handshake_sock.send_string(
            self.CLIENT_IP_PREFIX + str(self.client_ip)
        )
        self.client_ip += 1

    def process_outgoing(self) -> None:
        """
        reads a packet from the interface and sends it to the appropriate client
        """
        payload = self.tun.read(self.tun.mtu)
        temp = bytearray(payload)
        # strip the ipv4 packet to get dest addr
        dest: str = "".join(str(val) + "." for val in temp[20:24])[0:-1]
        print(f"processing outgoing {dest}")
        if dest in self.client_sockets.keys():
            print(f"sending to {dest}")
            self.client_sockets[dest][0].send_string(str(payload))
            self.client_sockets[dest][0].recv()
            print("sent")

    async def process_incoming(self) -> None:
        """
        gets all packets from all clients, and sends it to the interface
        """
        for addr, val in self.client_sockets.items():
            has_val = await val[1].poll(timeout=0.01)
            if has_val != 0:
                print(f"processing incoming from {addr}")
                payload = await val[1].recv_string()
                self.payload_queue.append(str(payload))
                await val[1].send_string("")
        await asyncio.sleep(0.001)

    def write_to_tun(self) -> None:
        if len(self.payload_queue) > 0:
            self.tun.write(self.payload_queue.pop(0))
            print("wrote to tun")

    def __initialize_client(self, client_ip: int) -> None:
        """
        set up client rep/req sockets to start communication

        :param client_ip: unique id of a new client
        """
        self.client_sockets[self.CLIENT_IP_PREFIX + str(client_ip)] = (
            self.context.socket(zmq.REQ),  # to client sock
            self.context.socket(zmq.REP),  # from client sock
        )
        self.client_sockets[self.CLIENT_IP_PREFIX + str(client_ip)][0].bind(
            self.IPC_PREFIX + self.CLIENT_IP_PREFIX + str(client_ip) + "_tocli"
        )
        self.client_sockets[self.CLIENT_IP_PREFIX + str(client_ip)][1].bind(
            self.IPC_PREFIX
            + self.CLIENT_IP_PREFIX
            + str(client_ip)
            + "_fromcli"
        )


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    server = Server()
    loop.add_reader(server.tun, server.process_outgoing)
    loop.add_writer(server.tun, server.write_to_tun)

    async def proc_handshake_forever(server: Server):
        while True:
            await server.handle_handshake()

    async def proc_incoming_forever(server: Server):
        while True:
            await server.process_incoming()

    loop.create_task(proc_handshake_forever(server))
    loop.create_task(proc_incoming_forever(server))
    loop.run_forever()

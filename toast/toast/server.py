import zmq
import pytun

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
        self.context = zmq.Context(1)

        self.tun = pytun.TunTapDevice(name=name)
        self.tun.addr = ip
        self.tun.netmask = "255.255.255.0"
        self.tun.mtu = self.MTU
        self.tun.up()

        self.handshake_sock: zmq.Socket = self.context.socket(zmq.REP)
        self.handshake_sock.bind(self.HANDSHAKE_ADDR)

        self.client_ip: int = 2

        # dict with key of client_ip, and value of (to_sock, from_sock)
        self.client_sockets: Dict[str, Tuple[zmq.Socket, zmq.Socket]] = {}

    def handle_handshake(self) -> None:
        """
        handle a handshake request
        """
        self.handshake_sock.recv()  # get some empty request
        self.__initialize_client(self.client_ip)
        self.handshake_sock.send_string(
            self.CLIENT_IP_PREFIX + str(self.client_ip)
        )
        self.client_ip += 1

    def process_outgoing(self) -> None:
        """
        reads a packet from the interface and sends it to the appropriate client
        """
        payload = self.tun.read(self.tun.MTU)
        temp = bytearray(payload)
        # strip the ipv4 packet to get dest addr
        dest: str = "".join(str(val) + "." for val in temp[20:24])[0:-1]
        if dest in self.client_sockets.keys():
            self.client_sockets[dest][0].send_string(payload)
            self.client_sockets[dest][0].recv()

    def process_incoming(self) -> None:
        """
        gets all packets from all clients, and sends it to the interface
        """
        for val in self.client_sockets.values():
            if val[1].poll(timeout=0.01):
                payload = val[1].recv_string()
                self.tun.write(payload)
                val[1].send_string("")

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

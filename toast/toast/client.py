import pytun
import zmq


class Client:
    """
    lightweight Client-side of a toast tunnel
    """

    IPC_PREFIX: str = "ipc:///dev/shm/"
    HANDSHAKE_ADDR: str = IPC_PREFIX + "toast_hs"
    MTU: int = 1500

    def __init__(self, name: str = "toast_ue") -> None:
        self.name = name

        self.context = zmq.Context(1)
        ip: str = self.__get_ip(self.context)

        self.tun = pytun.TunTapDevice(name=name)
        self.tun.addr = ip
        self.tun.netmask = "255.255.255.0"
        self.tun.mtu = self.MTU
        self.tun.up()

        self.recv_sock: zmq.Socket = self.context.socket(zmq.REP)
        self.send_sock: zmq.Socket = self.context.socket(zmq.REQ)

        self.recv_sock.connect(self.IPC_PREFIX + ip + "_recv")
        self.send_sock.connect(self.IPC_PREFIX + ip + "_send")

    def process_outgoing(self) -> None:
        """
        reads a packet from the interface and sends it to the server
        """
        payload = self.tun.read(self.tun.MTU)
        self.send_sock.send_string(payload)
        self.send_sock.recv()  # reset the socket

    def process_incoming(self) -> None:
        """
        gets a packet from the server and sends it to the interface
        """
        payload = self.recv_sock.recv_string()
        self.tun.write(payload)
        self.recv_sock.send()  # reset the socket

    def __get_ip(self, context: zmq.Context) -> str:
        """
        obtains an IP address from the server

        :param context: a ZMQ context used to connect to the server
        :return: an ip address obtained from the server
        """
        socket: zmq.Socket = context.socket(zmq.REQ)
        socket.connect(self.HANDSHAKE_ADDR)
        result: str = str(socket.recv())
        socket.close()
        return result

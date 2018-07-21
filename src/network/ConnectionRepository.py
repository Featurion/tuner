import socket


class ConnectionRepository(socket.socket):

    def __init__(self,
                 host: str, port: int,
                 # native socket.socket kwargs
                 family=socket.AF_INET, type=socket.SOCK_STREAM, **kwargs):
        super().__init__(family, type, **kwargs)
        self.address = (host, port)

    def connect(self):
        super().connect(self.address)

    def handleDisconnected(self):
        # discard pending data
        super().shutdown(socket.SHUT_RDWR)

    def cleanup(self):
        # close the socket
        super().close()

import asyncio
import base64
import msgpack
import socket
import struct


class Datagram(dict):

    @classmethod
    def load(cls, data):
        obj = cls()
        for k, v in msgpack.loads(base64.b85decode(data)).items():
            obj.setdefault(k.decode(), v)
        return obj

    def __init__(self):
        super().__init__(self)
        self['code'] = 0
        self['data'] = None

    def pack(self):
        return base64.b85encode(msgpack.dumps(self))


class ConnectionRepository(socket.socket):

    def __init__(self,
                 host: str, port: int,
                 # native socket.socket kwargs
                 family=socket.AF_INET, type_=socket.SOCK_STREAM, **kwargs):
        super().__init__(family, type_, **kwargs)
        self.address = (host, port)


class ConnectionManager(object):

    def __init__(self, uuid_, read_stream, write_stream):
        super().__init__()
        self._uuid = uuid_
        self._reader = read_stream
        self._writer = write_stream

    @property
    def id(self):
        return self._uuid.hex

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        pass

    async def start(self):
        while True:
            dg = await self.recvDatagram()
            if dg:
                self.handleDatagram(dg)
            else:
                break

    async def stop(self):
        pass

    async def recvDatagram(self, n_bytes: int = None) -> bytes:
        try:
            if n_bytes is None:
                pointer = await self._reader.readexactly(4)
                n_bytes = socket.ntohl(struct.unpack('I', pointer)[0])

            data = await self._reader.read(n_bytes)
            return Datagram.load(data)
        except ConnectionResetError:
            # client terminated
            pass
        except asyncio.streams.IncompleteReadError:
            # failed to receive pointer
            pass
        except struct.error:
            # bad pointer
            pass

    async def sendDatagram(self, dg: Datagram):
        try:
            bytes_ = dg.pack()
            n_bytes = len(bytes_)
            pointer = struct.pack('I', socket.htonl(n_bytes))
            self._writer.write(pointer + bytes_)
            await self._writer.drain()
        except ConnectionResetError:
            # client terminated
            pass

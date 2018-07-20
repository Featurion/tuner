import asyncio
import base64
import msgpack
import socket
import struct

from src.base.network.Datagram import Datagram
from src.base.network.meta import MetaHandler


class ClientRepositoryBase(metaclass=MetaHandler):

    msgtype = 'CLIENT'

    @classmethod
    def debyte(cls, elem):
        if isinstance(elem, (bytes, bytearray)):
            return elem.decode()
        elif isinstance(elem, (tuple, list, set)):
            return type(elem)(cls.debyte(e) for e in elem)
        elif isinstance(elem, dict):
            return {cls.debyte(k): cls.debyte(v) for k, v in elem.items()}
        else:
            return elem

    def __init__(self, uuid_, reader, writer):
        self._uuid = uuid_
        self.__reader = reader
        self.__writer = writer
        self.__handlers = {code: getattr(self, name) \
                           for code, name in \
                           self.__class__.handlers.items()}

    @property
    def id(self):
        return self._uuid.hex

    async def __aenter__(self):
        return self

    async def __aexit__(self, type_, val, tb):
        self.cleanup()

    async def start(self):
        while True:
            dg = await self.recvDatagram()
            if dg:
                try:
                    # check for native r_X handling
                    await self.__handlers[dg.code](dg)
                except (AttributeError, KeyError):
                    # default handler
                    await self.handleDatagram(dg)
            else:
                # connection broke
                break

    def cleanup(self):
        self.__reader = None
        self.__writer = None

    async def _send(self, bytes_: bytes):
        try:
            self.__writer.write(bytes_)
            await self.__writer.drain()  # helps avoid backlog
        except ConnectionResetError:
            # client terminated
            pass
        except AttributeError:
            # no transport
            pass

    async def _recv(self, size: int = None) -> bytes:
        try:
            return await self.__reader.read(size)
        except ConnectionResetError:
            # client terminated
            pass
        except asyncio.streams.IncompleteReadError:
            # failed to receive pointer
            pass
        except AttributeError:
            # no transport
            pass

        return bytes()

    async def sendDatagram(self, dg: Datagram):
        bytes_ = base64.b85encode(msgpack.dumps(dg))
        pointer = struct.pack('I', socket.htonl(len(bytes_)))
        await self._send(pointer + bytes_)

    async def recvDatagram(self) -> Datagram:
        try:
            pointer = await self._recv(4)
            size = socket.ntohl(struct.unpack('I', pointer)[0])
            bytes_ = await self._recv(size)
            data = msgpack.loads(base64.b85decode(bytes_))
            return Datagram(**self.debyte(data))
        except struct.error:
            # bad pointer
            pass
        except (TypeError, ValueError):
            # bad datagram
            pass

        return None

    async def handleDatagram(self, dg: Datagram):
        pass

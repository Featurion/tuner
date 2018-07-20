import asyncio
import uuid

from src.base.constants import *
from src.base.Datagram import Datagram
from src.distributed.ClientRepositoryBase import ClientRepositoryBase
from src.distributed.ConnectionRepository import ConnectionRepository


class ClientRepository(ClientRepositoryBase, ConnectionRepository):

    def __init__(self, *args, **kwargs):
        ConnectionRepository.__init__(self, *args, **kwargs)
        self.connect(self.address)

        coro = asyncio.open_connection(loop=self._loop, sock=self)
        streams = self._loop.run_until_complete(coro)
        ClientRepositoryBase.__init__(self, None, *streams)

        hex_ = self._loop.run_until_complete(self._recv(32))
        self._uuid = uuid.UUID(hex=hex_.decode())

    async def start(self):
        await self.sendHello()
        await super().start()

    def cleanup(self):
        super().cleanup()
        ConnectionRepository.cleanup(self)

    async def r_handleEject(self, dg):
        pass

    async def sendHello(self):
        dg = Datagram(code=CLIENT_HELLO, data=SERVER_VERSION)
        await self.sendDatagram(dg)

    async def r_handleHelloResp(self, dg):
        pass

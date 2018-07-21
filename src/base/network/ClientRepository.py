import asyncio
import uuid

from src.base.constants import *
from src.base.network.Datagram import Datagram
from src.base.network.ClientRepositoryBase import ClientRepositoryBase
from src.base.network.AsyncConnectionRepository import AsyncConnectionRepository


class ClientRepository(ClientRepositoryBase, AsyncConnectionRepository):

    def __init__(self, *args, **kwargs):
        AsyncConnectionRepository.__init__(self, *args, **kwargs)
        AsyncConnectionRepository.connect(self)

        coro = asyncio.open_connection(loop=self._loop, sock=self)
        streams = self._loop.run_until_complete(coro)
        ClientRepositoryBase.__init__(self, None, *streams)

        hex_ = self._loop.run_until_complete(self._recv(32))
        self._uuid = uuid.UUID(hex=hex_.decode())

    def connect(self):
        self._loop.run_until_complete(self.start())

    def cleanup(self):
        ClientRepositoryBase.cleanup(self)
        AsyncConnectionRepository.cleanup(self)

    async def start(self):
        await self.sendHello()
        await super().start()

    async def r_handleEject(self, dg):
        pass

    async def sendHello(self):
        dg = Datagram(code=CLIENT_HELLO, data=SERVER_VERSION)
        await self.sendDatagram(dg)

    async def r_handleHelloResp(self, dg):
        pass

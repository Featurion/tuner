import asyncio
import builtins
import uuid

from ..base.constants import *
from ..network.Datagram import Datagram
from ..network.ClientRepositoryBase import ClientRepositoryBase
from ..network.AsyncConnectionRepository import AsyncConnectionRepository


class ClientRepository(ClientRepositoryBase, AsyncConnectionRepository):

    def __init__(self, *args, **kwargs):
        try:
            AsyncConnectionRepository.__init__(self, *args, **kwargs)
            AsyncConnectionRepository.connect(self)
        except ConnectionRefusedError:
            # TODO
            return
        else:
            coro = asyncio.open_connection(loop=self._loop, sock=self)
            streams = self._loop.run_until_complete(coro)
            ClientRepositoryBase.__init__(self, None, *streams)

            hex_ = self._loop.run_until_complete(self._recv(32))
            self._uuid = uuid.UUID(hex=hex_.decode())
        finally:
            self.__running = False
            builtins.conn = self

    @property
    def running(self):
        return self.__running

    def connect(self):
        self.__running = True
        self._loop.run_until_complete(self.start())

    def disconnect(self):
        self.__running = False

    def cleanup(self):
        ClientRepositoryBase.cleanup(self)
        AsyncConnectionRepository.cleanup(self)

    async def start(self):
        await self.sendHello()
        await super().start()

    async def heartbeat(self):
        pass

    async def r_handleEject(self, dg):
        # TODO
        pass

    async def sendHello(self):
        dg = Datagram(code=CLIENT_HELLO, data=SERVER_VERSION)
        await self.sendDatagram(dg)

    async def r_handleHelloResp(self, dg):
        # TODO
        pass

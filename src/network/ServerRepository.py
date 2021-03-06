import asyncio
import builtins
import pyarchy
import socket

from ..network.ClientRepositoryAI import ClientRepositoryAI
from ..network.AsyncConnectionRepository import AsyncConnectionRepository


class ServerRepository(AsyncConnectionRepository):

    def __init__(self, *args, aiClass=ClientRepositoryAI, **kwargs):
        super().__init__(*args, **kwargs)
        self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.bind(self.address)
        self.__aiClass = aiClass
        self.clients = {}
        builtins.conn = self

    def connect(self):
        # setup serving protocol
        coro = self._network_loop.create_server(
            lambda: asyncio.StreamReaderProtocol(
                asyncio.StreamReader(),
                self.handleClientConnect),
            sock=self)
        # start serving
        self._network_loop.run_until_complete(coro)
        self._network_loop.run_until_complete(self.__storeData())
        self._network_loop.run_forever()

    async def handleClientConnect(self, reader, writer):
        async with self.__aiClass(reader, writer) as client:
            self.clients[client.id] = client
            await client.start()
            await client.stop()
            del self.clients[client.id]

    async def __storeData(self):
        while True:
            await self.storeData()
            await asyncio.sleep(15)

    async def storeData(self):
        pass

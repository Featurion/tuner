import asyncio
import socket

from src.base.network.ClientRepositoryAI import ClientRepositoryAI
from src.base.network.AsyncConnectionRepository import AsyncConnectionRepository


class ServerRepository(AsyncConnectionRepository):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.bind(self.address)

    def connect(self):
        # setup serving protocol
        coro = self._loop.create_server(
            lambda: asyncio.StreamReaderProtocol(
                asyncio.StreamReader(),
                self.handleClientConnect),
            sock=self)
        # start serving
        self._loop.run_until_complete(coro)
        self._loop.run_forever()

    async def handleClientConnect(self, reader, writer):
        async with ClientRepositoryAI(reader, writer) as conn:
            await conn.start()

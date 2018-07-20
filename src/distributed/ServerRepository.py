import asyncio
import socket

from src.distributed.ClientRepositoryAI import ClientRepositoryAI
from src.distributed.ConnectionManager import ConnectionManager
from src.distributed.ConnectionRepository import ConnectionRepository


class ServerRepository(ConnectionRepository):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.bind(self.address)
        self._loop = asyncio.get_event_loop()

    def _run(self):
        super()._run()
        # start serving
        self._loop.run_forever()

    async def start(self):
        # setup serving protocol
        await self._loop.create_server(
            lambda: asyncio.StreamReaderProtocol(
                asyncio.StreamReader(),
                self.handleConnected),
            sock=self)

    async def handleConnected(self, reader, writer):
        async with ClientRepositoryAI(reader, writer) as conn:
            try:
                await conn.start()
            except asyncio.CancelledError:
                # client terminated
                pass

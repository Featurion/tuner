import asyncio
import uuid

from src.base.core import ConnectionManager, ConnectionRepository


class ClientRepository(ConnectionRepository, ConnectionManager):

    def __init__(self, *args, **kwargs):
        ConnectionRepository.__init__(self, *args, **kwargs)
        self.connect(self.address)
        uuid_ = uuid.UUID(hex=self.recv(32))

        loop = asyncio.get_event_loop()
        coro = asyncio.open_connection(loop=loop, sock=self)
        ConnectionManager.__init__(self, uuid_, *loop.run_until_complete(coro))

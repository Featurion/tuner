import asyncio
import uuid

from ..base.constants import *
from ..network.Datagram import Datagram
from ..network.ClientRepositoryBase import ClientRepositoryBase


class ClientRepositoryAI(ClientRepositoryBase):

    def __init__(self, reader, writer):
        super().__init__(uuid.uuid4(), reader, writer)

    async def start(self):
        print(self.id)
        await self._send(self.id.encode())
        await super().start()

    async def r_handleHello(self, dg):
        if dg.data != SERVER_VERSION:
            dg = Datagram(code=CLIENT_EJECT, data='Wrong server version!')
        else:
            dg = Datagram(code=CLIENT_HELLO_RESP)

        await self.sendDatagram(dg)

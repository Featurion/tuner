import asyncio
import uuid

from src.base.constants import *
from src.network.Datagram import Datagram
from src.network.ClientRepositoryBase import ClientRepositoryBase


class ClientRepositoryAI(ClientRepositoryBase):

    def __init__(self, reader, writer):
        super().__init__(uuid.uuid4(), reader, writer)

    async def start(self):
        await self._send(self.id.encode())
        await super().start()

    async def r_handleHello(self, dg):
        if dg.data != SERVER_VERSION:
            dg = Datagram(code=CLIENT_EJECT, data='Wrong server version!')
        else:
            dg = Datagram(code=CLIENT_HELLO_RESP)

        await self.sendDatagram(dg)

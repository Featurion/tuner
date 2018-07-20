import asyncio

from src.base.constants import *
from src.base.core import ConnectionManager, Datagram
from src.base.server import ServerRepository


class DistributedClientAI(ConnectionManager):

    async def handleDatagram(self, dg):
        if dg['code'] == CLIENT_HELLO:
            if dg['data'] != SERVER_VERSION:
                self.ejectClient("Wrong server version!")
            else:
                dg = Datagram()
                dg['code'] = CLIENT_HELLO_RESP
                await self.sendDatagram(dg)

    async def ejectClient(self, msg):
        dg = Datagram()
        dg['code'] = CLIENT_EJECT
        dg['data'] = msg
        await self.sendDatagram(dg)


class DistributedServer(ServerRepository):

    async def accept(self, reader, writer):
        try:
            conn = await super().accept(reader, writer)
            await conn.start()
        except asyncio.CancelledError:
            # client terminated
            pass
        finally:
            await conn.stop()

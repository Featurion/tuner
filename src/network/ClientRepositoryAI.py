import asyncio
import base64
import msgpack
import uuid

from ..base.constants import *
from ..network.Datagram import Datagram
from ..network.ClientRepositoryBase import ClientRepositoryBase


class ClientRepositoryAI(ClientRepositoryBase):

    def __init__(self, reader, writer):
        super().__init__(uuid.uuid4(), reader, writer)

    async def start(self):
        print(self.id)
        conn.clients[self.id] = self
        await self._send(self.id.encode())
        await super().start()

    async def r_handleHello(self, dg):
        if dg.data != SERVER_VERSION:
            dg = Datagram(code=CLIENT_EJECT, data='Wrong server version!')
        else:
            dg = Datagram(code=CLIENT_HELLO_RESP)

        await self.sendDatagram(dg)

    async def r_handleViewSet(self, dg):
        conn.channelMap[dg.user_id] = set()

    async def r_handleViewReq(self, dg):
        viewers = conn.channelMap.get(dg.data)
        if viewers is not None:
            viewers.add(dg.user_id)

    async def r_handleFrame(self, dg):
        bytes_ = b''
        while len(bytes_) < dg.data:
            n_bytes = dg.data - len(bytes_)
            bytes_ += await self._recv(65536 if n_bytes > 65536 else n_bytes)

        viewers = conn.channelMap.get(dg.user_id)
        if viewers:
            for viewerId in viewers:
                client = conn.clients.get(viewerId)
                if client:
                    await client.sendDatagram(dg)
                    try:
                        await client._send(bytes_)
                    except asyncio.BrokenPipeError:
                        pass

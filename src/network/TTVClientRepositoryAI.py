import asyncio

from ..constants import *
from ..network.Datagram import Datagram
from ..network.ClientRepositoryAI import ClientRepositoryAI


class TTVClientRepositoryAI(ClientRepositoryAI):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._channel = 0

    async def stop(self):
        if self._channel:
            await self.sendStreamDone()
            self._channel = 0

    async def r_handleStreamReq(self, dg):
        channel = await conn.allocateChannel(dg.user_id)
        await self.sendStreamReqResp(channel)

    async def sendStreamReqResp(self, channel):
        dg = Datagram(code=CLIENT_STREAM_REQ_RESP, data=channel)
        await self.sendDatagram(dg)
        self._channel = channel

    async def sendStreamDone(self):
        channel = await conn.getChannel(self.id)
        if channel:
            dg = Datagram(code=CLIENT_STREAM_DONE, data=channel)
            await self.sendDatagram(dg)
            await conn.propogate(dg, channel)

    async def r_handleStreamDone(self, dg):
        await self.sendStreamDone()

    async def r_handleFrame(self, dg):
        if not self._channel:
            return

        bytes_ = b''
        while len(bytes_) < dg.data:
            n_bytes = dg.data - len(bytes_)
            bytes_ += await self._recv(65536 if n_bytes > 65536 else n_bytes)

        channel = await conn.getChannel(self.id)
        await conn.propogate(dg, channel, bytes_)

    async def r_handleViewReq(self, dg):
        success = await conn.enterView(dg)
        await self.sendViewReqResp(success)

    async def sendViewReqResp(self, channel):
        dg = Datagram(code=CLIENT_VIEW_REQ_RESP, data=channel)
        await self.sendDatagram(dg)

    async def r_handleViewDone(self, dg):
        await conn.exitView(dg)

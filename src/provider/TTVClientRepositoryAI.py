import asyncio

from ..base.constants import *
from ..network.Datagram import Datagram
from ..network.ClientRepositoryAI import ClientRepositoryAI


class TTVClientRepositoryAI(ClientRepositoryAI):

    async def r_handleStreamReq(self, dg):
        try:
            conn.freeChannels.sort()
            channel = conn.freeChannels.pop(0)
        except IndexError:
            channel = conn.channelCtx
            conn.channelCtx += 1

        conn.channelCtxMap[dg.user_id] = channel
        conn.channelMap[channel] = set()
        await self.sendStreamReqResp(channel)

    async def sendStreamReqResp(self, channel):
        dg = Datagram(code=CLIENT_STREAM_REQ_RESP, data=channel)
        await self.sendDatagram(dg)

    async def sendStreamDone(self):
        dg = Datagram(code=CLIENT_STREAM_DONE)
        await self.sendDatagram(dg)

        channel = conn.channelCtxMap.get(self.id)
        viewers = conn.getViewers(channel)
        for viewer in viewers:
            await viewer.sendViewDone(channel)
        del conn.channelCtxMap[self.id]
        conn.freeChannels.append(channel)

    async def r_handleStreamDone(self, dg):
        await self.sendStreamDone()

    async def r_handleFrame(self, dg):
        bytes_ = b''
        while len(bytes_) < dg.data:
            n_bytes = dg.data - len(bytes_)
            bytes_ += await self._recv(65536 if n_bytes > 65536 else n_bytes)

        channel = conn.channelCtxMap.get(self.id)
        viewers = conn.getViewers(channel)
        for viewer in viewers:
            await viewer.sendDatagram(dg)
            await viewer._send(bytes_)

    async def r_handleViewReq(self, dg):
        viewers = conn.channelMap.get(dg.data)
        if viewers is not None:
            await self.sendViewReqResp(dg.data)
            viewers.add(dg.user_id)
        else:
            await self.sendViewReqResp(0)

    async def sendViewReqResp(self, channel):
        dg = Datagram(code=CLIENT_VIEW_REQ_RESP, data=channel)
        await self.sendDatagram(dg)

    async def sendViewDone(self, channel):
        dg = Datagram(code=CLIENT_VIEW_DONE, data=channel)
        await self.sendDatagram(dg)

    async def r_handleViewDone(self, dg):
        viewers = conn.channelMap.get(dg.data)
        if viewers is not None:
            viewers.discard(dg.user_id)

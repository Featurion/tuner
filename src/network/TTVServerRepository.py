import yaml

from ..constants import *
from ..network.ServerRepository import ServerRepository
from ..network.TTVClientRepositoryAI import TTVClientRepositoryAI


class TTVServerRepository(ServerRepository):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, aiClass=TTVClientRepositoryAI, **kwargs)
        self.channelCtx = BASE_CHANNEL
        self.channelMap = {}
        self.channelIds = {}

    async def storeData(self):
        with open('data/channels.yml', 'w') as f:
            yaml.dump(self.channelMap, f, default_flow_style=False)

    async def allocateChannel(self, user_id):
        ctx = self.channelCtx
        self.channelCtx += 1
        if self.channelMap.get(ctx) is None:
            self.channelMap[ctx] = set()
        self.channelIds[ctx] = user_id
        return ctx

    async def propogate(self, dg, channel: int, ext_data: bytes = None):
        for viewer in await self.getViewers(channel):
            await viewer.sendDatagram(dg)
            if ext_data:
                await viewer._send(ext_data)

    async def getChannel(self, user_id):
        for channel, uid in self.channelIds.items():
            if uid == user_id:
                return channel
        return 0

    async def getViewers(self, channel):
        conns = []
        viewers = self.channelMap.get(channel)
        if viewers:
            for viewer_id in viewers:
                viewer = self.clients.get(viewer_id)
                if viewer:
                    conns.append(viewer)
        return conns

    async def enterView(self, dg):
        viewers = self.channelMap.get(dg.data, set())
        viewers.add(dg.user_id)
        self.channelMap[dg.data] = viewers
        return dg.data

    async def exitView(self, dg):
        viewers = self.channelMap.get(dg.data, set())
        viewers.discard(dg.user_id)
        self.channelMap[dg.data] = viewers

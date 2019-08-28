from ..base.constants import *
from ..network.ServerRepository import ServerRepository
from ..provider.TTVClientRepositoryAI import TTVClientRepositoryAI


class ProviderRepository(ServerRepository):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, aiClass=TTVClientRepositoryAI, **kwargs)
        self.channelCtx = BROADCAST_CHANNEL_MIN
        self.channelCtxMap = {}
        self.channelMap = {}
        self.freeChannels = []

    def getViewers(self, channel):
        conns = []
        viewers = self.channelMap.get(channel)
        if viewers:
            for viewer_id in viewers:
                viewer = self.clients.get(viewer_id)
                if viewer:
                    conns.append(viewer)
        return conns

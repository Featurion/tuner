from ..base.constants import *
from ..network.ServerRepository import ServerRepository
from ..network.TTVClientRepositoryAI import TTVClientRepositoryAI


class ProviderRepository(ServerRepository):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, aiClass=TTVClientRepositoryAI, **kwargs)
        self.channelMap = {}

    def getViewers(self, channel):
        conns = []
        viewers = self.channelMap.get(channel)
        if viewers:
            for viewer_id in viewers:
                viewer = self.clients.get(viewer_id)
                if viewer:
                    conns.append(viewer)
        return conns

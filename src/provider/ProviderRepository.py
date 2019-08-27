from ..network.ServerRepository import ServerRepository


class ProviderRepository(ServerRepository):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.channelMap = {}

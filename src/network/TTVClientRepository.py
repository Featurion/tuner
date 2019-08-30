import pyarchy

from ..network.ClientRepository import ClientRepository


class TTVClientRepository(ClientRepository):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_active = pyarchy.mechanical.BinarySwitch()
        self._activate = None

    async def connBroke(self):
        while self.is_active.state:
            app.window.video_mgr.static()

from ..network.ClientRepository import ClientRepository


class TTVClientRepository(ClientRepository):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__is_active = False
        self._activate = None

    @property
    def is_active(self):
        return self.__is_active

    @is_active.setter
    def is_active(self, bool_: bool):
        self.__is_active = bool(bool_)

    async def connBroke(self):
        while self.is_active:
            app.window.video_mgr.static()

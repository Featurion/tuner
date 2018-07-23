import cv2

from ..network.ClientRepository import ClientRepository


class ReceiverRepository(ClientRepository):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__running = False
        self.rec = cv2.VideoCapture(0) # TEMP

    async def heartbeat(self):
        # TEMP
        if self.rec:
            _, frame = self.rec.read()
        else:
            frame = None

        app.window.video_mgr.frame = frame

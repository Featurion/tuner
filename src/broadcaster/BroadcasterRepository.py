import base64
import cv2
import io
import json
import msgpack
import numpy as np

from ..base.constants import *
from ..network.ClientRepository import ClientRepository
from ..network.Datagram import Datagram


class BroadcasterRepository(ClientRepository):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__running = False
        self.rec = cv2.VideoCapture(0)
        self.sent = False

    async def sendViewSet(self):
        await self.sendDatagram(Datagram(code=CLIENT_VIEW_SET))

    async def sendFrame(self, frame):
        memfile = io.BytesIO()
        np.savez_compressed(memfile, frame)
        memfile.seek(0)
        data = memfile.getvalue()
        bytes_ = base64.b85encode(msgpack.dumps(data))

        dg = Datagram(code=CLIENT_FRAME, data=len(bytes_))
        await self.sendDatagram(dg)
        await self._send(bytes_)

    async def heartbeat(self):
        if not self.sent:
            self.sent = True
            await self.sendViewSet()
            return

        if self.rec:
            _, frame = self.rec.read()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            await self.sendFrame(frame)

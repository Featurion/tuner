import base64
import cv2
import io
import msgpack
import numpy as np

from ..base.constants import *
from ..network.ClientRepository import ClientRepository
from ..network.Datagram import Datagram


class ReceiverRepository(ClientRepository):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__running = False
        self.sent = False

    async def connBroke(self):
        while app.is_viewing:
            app.window.video_mgr.static()

    async def heartbeat(self):
        # TEST
        if not self.sent:
            self.sent = True
            await self.sendViewRequest('5f329f00f8584c7b9f8421ac71224dee')

    async def sendViewRequest(self, userId):
        dg = Datagram(code=CLIENT_VIEW_REQ, data=userId)
        await self.sendDatagram(dg)

    async def r_handleFrame(self, dg):
        bytes_ = b''
        while len(bytes_) < dg.data:
            n_bytes = dg.data - len(bytes_)
            bytes_ += await self._recv(65536 if n_bytes > 65536 else n_bytes)
        data = msgpack.loads(base64.b85decode(bytes_))

        memfile = io.BytesIO()
        memfile.write(data)
        memfile.seek(0)
        frame = np.load(memfile)['arr_0']
        app.window.video_mgr.frame = frame

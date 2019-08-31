import base64
import cv2
import numpy as np
import time

from ..constants import *
from ..gui.ChannelSelectGUI import ChannelSelectGUI
from ..network.TTVClientRepository import TTVClientRepository
from ..network.Datagram import Datagram


class ReceiverRepository(TTVClientRepository):

    def __init__(self, *args, **kwargs):
        app.signal_channel_select.emit()
        super().__init__(*args, **kwargs)
        self.frame_bytes = (None, time.time())

    async def heartbeat(self):
        if app._channel:
            if time.time() - self.frame_bytes[1] > 1:
                app.window.video_mgr.static()

    async def sendViewRequest(self, channel):
        dg = Datagram(code=CLIENT_VIEW_REQ, data=channel)
        await self.sendDatagram(dg)

    async def r_handleViewReqResp(self, dg):
        app.signal_receiving.emit(dg.data)

    async def sendViewDone(self, channel):
        dg = Datagram(code=CLIENT_VIEW_DONE, data=channel)
        await self.sendDatagram(dg)
        app.signal_channel_select.emit()

    async def sendFrameReq(self):
        dg = Datagram(code=CLIENT_FRAME, data=None)
        await self.sendDatagram(dg)

    async def r_handleFrame(self, dg):
        if not app._channel:
            return

        bytes_ = b''
        while len(bytes_) < dg.data:
            n_bytes = dg.data - len(bytes_)
            bytes_ += await self._recv(65536 if n_bytes > 65536 else n_bytes)

        self.frame_bytes = (base64.b64decode(bytes_), time.time())
        img = np.fromstring(self.frame_bytes[0], dtype=np.uint8)
        frame = cv2.imdecode(img, 1)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        app.window.video_mgr.frame = frame

    async def r_handleStreamDone(self, dg):
        self.frame_bytes = (None, time.time())

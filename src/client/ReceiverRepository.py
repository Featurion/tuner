import base64
import cv2
import io
import msgpack
import numpy as np

from ..base.constants import *
from ..gui.ChannelSelectGUI import ChannelSelectGUI
from ..network.TTVClientRepository import TTVClientRepository
from ..network.Datagram import Datagram


class ReceiverRepository(TTVClientRepository):

    def __init__(self, *args, **kwargs):
        app.signal_channel_select.emit()
        super().__init__(*args, **kwargs)
        self.__was_active = None
        self.sent = False

    async def heartbeat(self):
        if (self.__was_active is not None) and not self.is_active:
            # done viewing
            await self.sendViewDone(self.__was_active)
            self.__was_active = None
            app.signal_channel_select.emit()
        elif self.is_active:
            # currently viewing
            pass
        else:
            # not currently viewing
            # TEST
            if self._activate:
                await self.sendViewRequest(self._activate)
                self._activate = None

    async def sendViewRequest(self, channel):
        dg = Datagram(code=CLIENT_VIEW_REQ, data=channel)
        await self.sendDatagram(dg)

    async def r_handleViewReqResp(self, dg):
        if dg.data:
            self.is_active = True
            self.__was_active = dg.data
        else:
            pass # error

    async def sendViewDone(self, channel):
        dg = Datagram(code=CLIENT_VIEW_DONE, data=channel)
        await self.sendDatagram(dg)

    async def r_handleViewDone(self, dg):
        await self.connBroke()

    async def r_handleFrame(self, dg):
        bytes_ = b''
        while len(bytes_) < dg.data:
            n_bytes = dg.data - len(bytes_)
            bytes_ += await self._recv(65536 if n_bytes > 65536 else n_bytes)

        frame_bytes = base64.b64decode(bytes_)
        img = np.fromstring(frame_bytes, dtype=np.uint8)
        frame = cv2.imdecode(img, 1)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # threading problem
        if hasattr(app.window, 'video_mgr'):
            app.window.video_mgr.frame = frame

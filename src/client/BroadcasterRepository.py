import base64
import cv2
import io
import json
import msgpack
import numpy as np

from ..base.constants import *
from ..network.TTVClientRepository import TTVClientRepository
from ..network.Datagram import Datagram


class BroadcasterRepository(TTVClientRepository):

    def __init__(self, *args, **kwargs):
        app.signal_broadcasting.emit()
        super().__init__(*args, **kwargs)
        self.__was_active = False
        self.__capture = cv2.VideoCapture(0)
        self.sent = False

    async def heartbeat(self, x=0):
        if self.__was_active and not self.is_active:
            # done broadcasting
            await self.sendStreamDone()
            self.__was_active = False
            app.window.close()
        elif self.is_active:
            # currently broadcasting
            if self.__capture:
                success, frame = self.__capture.read()
                if success:
                    _, bytes_ = cv2.imencode('.jpg', frame)
                    await self.sendFrame(bytes_)

                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                    if hasattr(app.window, 'video_mgr'):
                        app.window.video_mgr.frame = frame
        else:
            # not currently broadcasting
            # TEST
            if not self.sent:
                await self.sendStreamReq()
                self.sent = True

    async def sendStreamReq(self):
        await self.sendDatagram(Datagram(code=CLIENT_STREAM_REQ))

    async def r_handleStreamReqResp(self, dg):
        print('broadcasting to channel: ', dg.data)
        self.is_active = True
        self.__was_active = True

    async def sendStreamDone(self):
        dg = Datagram(code=CLIENT_STREAM_DONE)
        await self.sendDatagram(dg)

    async def r_handleStreamDone(self, dg):
        await self.connBroke()

    async def sendFrame(self, frame_bytes):
        bytes_ = base64.b64encode(frame_bytes)
        dg = Datagram(code=CLIENT_FRAME, data=len(bytes_))
        await self.sendDatagram(dg)
        await self._send(bytes_)

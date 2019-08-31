import asyncio
import base64
import cv2
import numpy as np
import time

from ..constants import *
from ..network.TTVClientRepository import TTVClientRepository
from ..network.Datagram import Datagram


class BroadcasterRepository(TTVClientRepository):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__capture = cv2.VideoCapture(0)
        self.frame_bytes = (None, time.time())

    async def r_handleHelloResp(self, dg):
        await self.sendStreamReq()

    async def connBroke(self):
        while app._channel:
            app.window.video_mgr.static()

    async def heartbeat(self):
        if self.__capture and app._channel:
            success, frame = self.__capture.read()
            if success:
                _, bytes_ = cv2.imencode('.jpg', frame)
                await self.sendFrame(bytes_)
                self.frame_bytes = (bytes_, time.time())

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                app.window.video_mgr.frame = frame

    async def sendStreamReq(self):
        dg = Datagram(code=CLIENT_STREAM_REQ)
        await self.sendDatagram(dg)

    async def r_handleStreamReqResp(self, dg):
        app._channel = dg.data
        print('broadcasting to channel:', self.id)
        app.signal_broadcasting.emit()

    async def sendStreamDone(self):
        dg = Datagram(code=CLIENT_STREAM_DONE)
        await self.sendDatagram(dg)
        app._channel = 0

    async def r_handleStreamDone(self, dg):
        await self.connBroke()

    async def sendFrame(self, frame_bytes):
        bytes_ = base64.b64encode(frame_bytes)
        dg = Datagram(code=CLIENT_FRAME, data=len(bytes_))
        await self.sendDatagram(dg)
        await self._send(bytes_)

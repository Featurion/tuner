import asyncio

from PyQt5.QtCore import pyqtSignal

from src.gui.ChannelSelectGUI import ChannelSelectGUI
from src.gui.GraphicalApp import GraphicalApp
from src.gui.ViewerGUI import ViewerGUI


class ClientApp(GraphicalApp):

    signal_broadcasting = pyqtSignal()
    signal_exit_cast = pyqtSignal(int)
    signal_channel_select = pyqtSignal()
    signal_receiving = pyqtSignal(int)
    signal_exit_view = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.signal_broadcasting.connect(self.enterBroadcastingMode)
        self.signal_exit_cast.connect(self.exitCast)
        self.signal_channel_select.connect(self.enterChannelSelect)
        self.signal_receiving.connect(self.enterReceiverMode)
        self.signal_exit_view.connect(self.exitView)
        self._channel = 0

    def enterBroadcastingMode(self):
        self.window = ViewerGUI('Broadcaster', self.exitCast)

    def exitCast(self):
        if not conn._network_loop.is_closed():
            asyncio.tasks.ensure_future(
                conn.sendStreamDone(),
                loop=conn._network_loop)
        self._channel = 0
        app.window.close()

    def enterChannelSelect(self):
        def cb(channel):
            asyncio.tasks.ensure_future(
                conn.sendViewRequest(channel),
                loop=conn._network_loop)
        self.window = ChannelSelectGUI(cb)

    def enterReceiverMode(self, channel):
        self._channel = channel
        self.window = ViewerGUI('Receiver', self.exitView)

    def exitView(self):
        if self._channel:
            asyncio.tasks.ensure_future(
                conn.sendViewDone(self._channel),
                loop=conn._network_loop)
            self._channel = 0

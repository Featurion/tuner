from PyQt5.QtCore import pyqtSignal

from ..gui.BroadcasterViewGUI import BroadcasterViewGUI
from ..gui.ChannelSelectGUI import ChannelSelectGUI
from ..gui.GraphicalApp import GraphicalApp
from ..gui.ReceiverViewGUI import ReceiverViewGUI


class ClientApp(GraphicalApp):

    signal_broadcasting = pyqtSignal()
    signal_channel_select = pyqtSignal()
    signal_receiving = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.signal_broadcasting.connect(self.enterBroadcastingMode)
        self.signal_channel_select.connect(self.enterChannelSelect)
        self.signal_receiving.connect(self.enterReceiverMode)

    def enterBroadcastingMode(self):
        self.window = BroadcasterViewGUI()

    def enterChannelSelect(self):
        self.window = ChannelSelectGUI(self.enterReceiverMode)

    def enterReceiverMode(self, channel):
        self.window = ReceiverViewGUI(channel)

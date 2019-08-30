from PyQt5.QtCore import pyqtSignal

from src.gui.ChannelSelectGUI import ChannelSelectGUI
from src.gui.GraphicalApp import GraphicalApp
from src.gui.ReceiverViewGUI import ReceiverViewGUI
from src.gui.ViewerGUI import ViewerGUI


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
        self.window = ViewerGUI('Broadcaster')

    def enterChannelSelect(self):
        self.window = ChannelSelectGUI(self.enterReceiverMode)

    def enterReceiverMode(self, channel):
        self.window = ReceiverViewGUI(channel)

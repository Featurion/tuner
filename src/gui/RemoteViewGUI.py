from .Window import Window
from ..receiver.VideoManager import VideoManager


class RemoteViewGUI(Window):

    def __init__(self):
        super().__init__()
        self.video_mgr = None
        self.setWindowTitle('Receiver')

    def start(self):
        self.video_mgr = VideoManager(self)
        self.video_mgr.moveToThread(app.daemon)
        super().start()

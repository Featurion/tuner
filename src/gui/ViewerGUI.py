from .QWindow import QWindow
from ..client.VideoManager import VideoManager


class ViewerGUI(QWindow):

    def __init__(self, title=''):
        super().__init__()
        self.__closed = False # work around QT bug
        self.video_mgr = None
        self.setWindowTitle(title)

    def start(self):
        self.video_mgr = VideoManager(self)
        self.video_mgr.moveToThread(app.daemon)
        super().start()

    def exitView(self):
        conn.is_active.toggle()
        self.__closed = True

    def closeEvent(self, event):
        event.accept()
        if not self.__closed:
            conn.is_active.toggle()
        self.__closed = True

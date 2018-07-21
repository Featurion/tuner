from src.gui.Window import Window
from src.base.ClientAgent import ClientAgent
from src.receiver.VideoManager import VideoManager


class ViewerGUI(Window):

    def __init__(self, host, port):
        super().__init__()
        self.__address = (host, port)
        self.__net_thread = None
        self.video_mgr = None
        self.setWindowTitle('Receiver')

    def start(self):
        self.__net_thread = ClientAgent(*self.__address)
        self.__net_thread.start()

        self.video_mgr = VideoManager()
        self.video_mgr.moveToThread(self.__net_thread)

        app.exec_()

    def cleanup(self):
        if self.__net_thread:
            self.__net_thread.quit()
            self.__net_thread.wait()
            self.__net_thread = None

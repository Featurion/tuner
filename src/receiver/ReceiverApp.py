from ..base.ClientAgent import ClientAgent
from ..gui.App import App
from ..gui.RemoteViewGUI import RemoteViewGUI
from ..receiver.ReceiverRepository import ReceiverRepository


class ReceiverApp(App):

    def __init__(self):
        super().__init__()
        self.__net_thread = None

    @property
    def daemon(self):
        return self.__net_thread

    def connect(self, host, port):
        try:
            self.__net_thread = ClientAgent(ReceiverRepository)
            self.__net_thread.start(host, int(port))
            self.window = RemoteViewGUI()
        except ValueError:
            return

    def cleanup(self):
        if self.__net_thread:
            self.__net_thread.quit()
            self.__net_thread.wait()
            self.__net_thread = None

        self.window = None

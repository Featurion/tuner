from .ViewerGUI import ViewerGUI


class ReceiverViewGUI(ViewerGUI):

    def __init__(self, channel):
        super().__init__('Receiver')
        self.channel = channel

    def start(self):
        conn._activate = self.channel
        super().start()

from PyQt5.QtWidgets import QMainWindow


class QWindow(QMainWindow):

    def start(self):
        self.show()

    def cleanup(self):
        self.close()

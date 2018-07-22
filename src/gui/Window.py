from PyQt5.QtWidgets import QMainWindow


class Window(QMainWindow):

    def closeEvent(self, event):
        event.accept()
        app.window = None

    def start(self):
        self.show()

    def cleanup(self):
        self.close()

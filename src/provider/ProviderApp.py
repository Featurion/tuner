from .ProviderRepository import ProviderRepository


class ProviderApp:

    def start(self):
        self.conn = ProviderRepository('127.0.0.1', 7199)
        self.conn.run()

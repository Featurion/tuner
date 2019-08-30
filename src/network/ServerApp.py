from src.network.TTVServerRepository import TTVServerRepository


class ServerApp:

    def start(self):
        self.conn = TTVServerRepository('127.0.0.1', 7199)
        self.conn.run()

import asyncio
import socket
import uuid

from src.base.core import ConnectionManager, ConnectionRepository


class ServerRepository(ConnectionRepository):

    def __init__(self, *args, mgr_cls=ConnectionManager, **kwargs):
        super().__init__(*args, **kwargs)
        self.__mgr_cls = mgr_cls  # override for custom ConnectionManager

    def start(self):
        self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.bind(self.address)
        self.__run()

    def __run(self):
        loop = asyncio.get_event_loop()
        coro = loop.create_server(
            lambda: asyncio.StreamReaderProtocol(
                asyncio.StreamReader(),
                self.accept),
            sock=self)

        # ignore ConnectionManager exceptions
        loop.set_exception_handler(lambda loop, context: None)

        try:
            loop.run_until_complete(coro)
            loop.run_forever()
        except KeyboardInterrupt:
            # done with server
            pass
        finally:
            tasks = asyncio.gather(*asyncio.Task.all_tasks(loop=loop))
            tasks.cancel()

            loop.run_until_complete(self.cleanup())
            loop.stop()

    async def accept(self, reader, writer):
        conn = self.__mgr_cls(uuid.uuid4(), reader, writer)
        await conn.send(conn.id)
        return conn

    async def cleanup(self):
        self.close()

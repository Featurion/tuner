import asyncio
import socket


class ConnectionRepository(socket.socket):

    def __init__(self,
                 host: str, port: int,
                 # native socket.socket kwargs
                 family=socket.AF_INET, type=socket.SOCK_STREAM, **kwargs):
        super().__init__(family, type, **kwargs)
        self._loop = asyncio.get_event_loop()
        self.address = (host, port)

    def _run(self):
        self._loop.run_until_complete(self.start())

    def run(self):
        try:
            self._run()
        except KeyboardInterrupt:
            # done with server
            self.cleanup()
        finally:
            self._loop.close()

    async def start(self):
        pass

    def cleanup(self):
        # close the socket
        self.close()

        # stop all tasks
        tasks = asyncio.gather(*asyncio.Task.all_tasks(loop=self._loop),
                               loop=self._loop,
                               return_exceptions=True)
        tasks.add_done_callback(lambda task: self._loop.stop())
        tasks.cancel()

        # wait for tasks to finish
        while not tasks.done() and not self._loop.is_closed():
            self._loop.run_forever()

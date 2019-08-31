import asyncio

from ..network.ConnectionRepository import ConnectionRepository


class AsyncConnectionRepository(ConnectionRepository):

    def __init__(self, *args, loop=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._network_loop = loop or asyncio.get_event_loop()

    def run(self):
        try:
            self.connect()
        except (KeyboardInterrupt, SystemExit):
            # done with connection
            self.handleDisconnected()
        finally:
            self.cleanup()

    def handleDisconnected(self):
        # stop all tasks
        tasks = asyncio.gather(*asyncio.Task.all_tasks(loop=self._network_loop),
                               loop=self._network_loop,
                               return_exceptions=True)
        tasks.add_done_callback(lambda task: self._network_loop.stop())
        tasks.cancel()

        # wait for tasks to finish
        while not tasks.done() and not self._network_loop.is_closed():
            self._network_loop.run_forever()

    def cleanup(self):
        super().cleanup()
        self._network_loop.close()

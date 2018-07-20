import asyncio
import argparse
import uvloop


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class Launcher(object):

    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-b', '--broadcaster',
                            dest='broadcaster',
                            action='store_true',
                            default=False,
                            help='launch broadcaster server')
        parser.add_argument('-p', '--provider',
                            dest='provider',
                            action='store_true',
                            default=False,
                            help='launch provider server')
        self.args = parser.parse_args()

    def run(self):
        if self.args.broadcaster:
            self.__launchBroadcaster()
        elif self.args.provider:
            self.__launchProvider()
        else:
            self.__launchReceiver()

    def __launchBroadcaster(self):
        # ???
        pass

    def __launchProvider(self):
        from src.provider.Provider import ProviderUI
        provider = ProviderUI()
        provider.start()

    def __launchReceiver(self):
        from src.receiver.ReceiverUI import ReceiverUI
        receiver = ReceiverUI()
        receiver.start()


if __name__ == '__main__':
    Launcher().run()

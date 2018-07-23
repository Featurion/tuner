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
            return
        elif self.args.provider:
            from .provider.ProviderApp import ProviderApp as App
        else:
            from .receiver.ReceiverApp import ReceiverApp as App

        __builtins__.app = App()
        app.start()


if __name__ == '__main__':
    Launcher().run()

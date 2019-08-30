import asyncio
import argparse
import uvloop


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class Launcher(object):

    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-p', '--provider',
                            dest='provider',
                            action='store_true',
                            default=False,
                            help='launch provider server')
        self.args = parser.parse_args()

    def run(self):
        if self.args.provider:
            from .network.ServerApp import ServerApp as App
        else:
            from .client.ClientApp import ClientApp as App

        __builtins__.app = App()
        app.start()


if __name__ == '__main__':
    Launcher().run()

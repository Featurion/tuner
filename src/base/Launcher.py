import argparse

class Launcher(object):

    def __init__(self):
        info = self.getLaunchInfo()
        if info.broadcaster:
            self.type = 'broadcaster'
            self.__launchBroadcaster()
        elif info.provider:
            self.type = 'provider'
            self.__launchProvider()
        else:
            self.type = 'receiver'
            self.__launchReceiver()

    def getLaunchInfo(self):
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
        args = parser.parse_args()
        return args

    def __launchProvider(self):
        from src.provider.Provider import ProviderUI

        provider = ProviderUI()

        provider.start()

    def __launchReceiver(self):
        from src.receiver.ReceiverUI import ReceiverUI

        receiver = ReceiverUI()

        receiver.start()

if __name__ == '__main__':
    Launcher()
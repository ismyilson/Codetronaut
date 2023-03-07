from processor import Processor

import atexit


class App:
    processor: Processor

    def __init__(self):
        self.processor = Processor()

        atexit.register(self.clean_up)

    def start(self):
        self.processor.start()

    def clean_up(self):
        print('Cleaning up')

        # self.processor.clean_up()


if __name__ == '__main__':
    application = App()
    application.start()

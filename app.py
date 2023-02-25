import atexit

import processor as pr
import transcriber

from context import CurrentContext

from handlers import audio_handler, file_handler


class App:
    processor: pr.Processor

    def __init__(self):
        self.processor = pr.Processor()

        self.sample_size = audio_handler.get_sample_size()

        atexit.register(self.clean_up)

    def start(self):
        while True:
            frames = audio_handler.record()

            with file_handler.audio_to_file(frames, self.sample_size) as audio_file:
                user_input = transcriber.transcribe(audio_file)
                self.processor.process_command(user_input)

    def clean_up(self):
        print('Cleaning up')

        self.processor.clean_up()
        audio_handler.clean_up()

        CurrentContext.clean_up()


if __name__ == '__main__':
    application = App()
    application.start()

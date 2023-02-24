from handlers import audio_handler as ah, file_handler

import processor as pr
import transcriber


class App:
    audio_handler: ah.AudioHandler
    processor: pr.Processor

    def __init__(self):
        self.audio_handler = ah.AudioHandler()
        self.processor = pr.Processor()

        self.sample_size = self.audio_handler.get_sample_size()

    def start(self):
        while True:
            frames = self.audio_handler.record()

            with file_handler.audio_to_file(frames, self.sample_size) as audio_file:
                user_input = transcriber.transcribe(audio_file)
                self.processor.process_command(user_input)


if __name__ == '__main__':
    application = App()
    application.start()

import audio_handler as ah
import file_handler
import transcriber


class App:
    audio_handler: ah.AudioHandler

    def __init__(self):
        self.audio_handler = ah.AudioHandler()
        self.sample_size = self.audio_handler.get_sample_size()

    def start(self):
        while True:
            frames = self.audio_handler.record()

            with file_handler.audio_to_file(frames, self.sample_size) as audio_file:
                print(transcriber.transcribe(audio_file))

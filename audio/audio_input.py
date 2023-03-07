import pyaudio
import numpy as np

from audio import transcriber
from handlers import file_handler
from user_input import UserInput


FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 30


class AudioInput:

    audio: pyaudio.PyAudio
    stream: pyaudio.Stream

    def __init__(self):
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK, start=False)

    def get_input(self):
        frames = self._record()

        with file_handler.audio_to_file(frames, self.audio.get_sample_size(FORMAT)) as audio_file:
            text = transcriber.transcribe(audio_file)

        return UserInput(text)

    def _record(self):
        just_started = True
        retries = 0
        frames = []

        self.stream.start_stream()

        print('Recording...')
        for i in range(int(RATE / CHUNK * RECORD_SECONDS)):
            data = np.frombuffer(self.stream.read(CHUNK), dtype=np.int16)
            peak = np.average(np.abs(data)) * 2

            if int(50 * peak / 2 ** 16) < 1:
                retries += 1
            elif just_started:
                retries = 0
                just_started = False

            if retries >= 75 and not just_started:
                break

            frames.append(data)
        print('Recording stop')

        self.stream.stop_stream()

        return frames

    def clean_up(self):
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

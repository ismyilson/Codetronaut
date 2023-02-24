import pyaudio
import numpy as np


FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 30


class AudioHandler:
    def __init__(self):
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=FORMAT,
                                      channels=CHANNELS,
                                      rate=RATE,
                                      input=True,
                                      frames_per_buffer=CHUNK,
                                      start=False)

        self.sample_size = self.audio.get_sample_size(FORMAT)

    def record(self):
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

    def get_sample_size(self):
        return self.audio.get_sample_size(FORMAT)

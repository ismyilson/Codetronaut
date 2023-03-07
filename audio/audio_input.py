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
    """
    Handles the user audio input.
    """

    _audio: pyaudio.PyAudio
    _stream: pyaudio.Stream

    def __init__(self):
        """
        Create a PyAudio object and an audio stream. The stream is closed by default.
        """

        self._audio = pyaudio.PyAudio()
        self._stream = self._audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK, start=False)

    def get_input(self):
        """
        Grabs audio input from the user's default input device for 30 seconds or until silence, and transcribes it.

        Returns:
            An object of type UserInput.
        """

        frames = self._record()

        with file_handler.audio_to_file(frames, self._audio.get_sample_size(FORMAT)) as audio_file:
            text = transcriber.transcribe(audio_file)

        return UserInput(text)

    def _record(self):
        """
        Records frames from the user's default input device for RECORD_SECONDS or until silence.

        Returns:
            A list of frames.
        """

        just_started = True
        retries = 0
        frames = []

        self._stream.start_stream()

        print('Recording...')
        for i in range(int(RATE / CHUNK * RECORD_SECONDS)):
            data = np.frombuffer(self._stream.read(CHUNK), dtype=np.int16)
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

        self._stream.stop_stream()

        return frames

    def clean_up(self):
        """
        Closes all open streams of audio.
        """

        self._stream.stop_stream()
        self._stream.close()
        self._audio.terminate()

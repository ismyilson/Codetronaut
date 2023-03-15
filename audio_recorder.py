import os
import queue
import tempfile
import threading
import wave
import pyaudio
import numpy as np
import transcriber

from contextlib import contextmanager
from global_vars import t_event_record, t_event_not_muted
from user_input.user_input import UserInput

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 48100
CHUNK = 2048
RECORD_SECONDS = 30

MAX_RETRIES = 30


@contextmanager
def audio_to_file(frames, sample_size):
    tmp = tempfile.NamedTemporaryFile(delete=False)
    wave_file = wave.open(tmp, 'wb')
    wave_file.setnchannels(CHANNELS)
    wave_file.setsampwidth(sample_size)
    wave_file.setframerate(RATE)
    wave_file.writeframes(b''.join(frames))

    yield tmp.name

    wave_file.close()
    tmp.close()
    os.unlink(tmp.name)


class AudioRecorder(threading.Thread):
    _audio: pyaudio.PyAudio
    _stream: pyaudio.Stream

    _processor_queue: queue.Queue

    def __init__(self, processor_queue):
        super().__init__(daemon=True)

        self._audio = pyaudio.PyAudio()
        self._stream = self._audio.open(format=FORMAT,
                                        channels=CHANNELS,
                                        rate=RATE,
                                        input=True,
                                        frames_per_buffer=CHUNK)

        self._processor_queue = processor_queue

    def _loop(self):
        while True:
            t_event_record.wait()
            t_event_not_muted.wait()

            frames = self._record()

            if not frames:
                continue

            with audio_to_file(frames, self._audio.get_sample_size(FORMAT)) as audio_file:
                text = transcriber.transcribe(audio_file)
                user_input = UserInput(text)

            self._processor_queue.put(user_input)

            t_event_record.clear()  # After putting text we wait for processor to signal us again

    def _record(self):
        frames = []

        just_started = True
        retries = 0

        self._stream.start_stream()

        print('Recording...')
        for i in range(int(RATE / CHUNK * RECORD_SECONDS)):
            if not t_event_not_muted.is_set():
                continue

            data = np.frombuffer(self._stream.read(CHUNK), dtype=np.int16)

            if self._is_silence(data):
                if just_started:
                    continue
                else:
                    retries += 1
            elif just_started:
                retries = 0
                just_started = False

            if retries >= MAX_RETRIES and not just_started:
                break

            print(f'Appending {data}')
            frames.append(data)
        print('Recording stop')

        self._stream.stop_stream()
        return frames

    def _is_silence(self, data):
        peak = np.average(np.abs(data)) * 2
        return int(50 * peak / 2 ** 16) < 1

    def run(self):
        self._loop()

from contextlib import contextmanager
from handlers.audio_handler import (
    CHANNELS,
    RATE
)
import tempfile
import wave
import os


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

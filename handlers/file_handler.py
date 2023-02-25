from pathlib import Path
from contextlib import contextmanager
from handlers.audio_handler import (
    CHANNELS,
    RATE
)
import tempfile
import pickle
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


def write_to_file(path, data):
    try:
        dir_path = path[0:path.rindex('\\')]
        Path(dir_path).mkdir(parents=True, exist_ok=True)
    except ValueError:
        pass

    with open(path, 'wb') as file:
        pickle.dump(data, file)


def load_file(path):
    with open(path, 'rb') as file:
        data = pickle.load(file)
        return data

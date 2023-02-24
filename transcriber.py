import whisper
import torch


device = "cuda" if torch.cuda.is_available() else "cpu"
model = whisper.load_model("base", device=device)


class UserInput:
    text: str
    words: list

    def __init__(self, text):
        text = text.lower()

        self.text = text
        self.words = text.replace('.', '').split()


def transcribe(file):
    # Load audio and pad/trim it to fit 30 seconds
    audio = whisper.load_audio(file)
    audio = whisper.pad_or_trim(audio)

    # Transcribe
    decode_options = {
        'fp16': False
    }
    result = whisper.transcribe(model, audio, **decode_options)

    return UserInput(result['text'])

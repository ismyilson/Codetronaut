import torch
import whisper


device = "cuda" if torch.cuda.is_available() else "cpu"
model = whisper.load_model("base", device=device)


def transcribe(file):
    audio_data = whisper.load_audio(file)
    audio_data = whisper.pad_or_trim(audio_data)

    decode_options = {
        'fp16': False,
        'language': 'en'
    }
    result = whisper.transcribe(model, audio_data, **decode_options)

    return result['text']

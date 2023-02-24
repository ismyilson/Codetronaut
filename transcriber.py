import whisper
import torch


def transcribe(file):
    # Setup
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = whisper.load_model("base", device=device)

    # Load audio and pad/trim it to fit 30 seconds
    audio = whisper.load_audio(file)
    audio = whisper.pad_or_trim(audio)

    # Transcribe
    decode_options = {
        'fp16': False
    }
    result = whisper.transcribe(model, audio, **decode_options)

    return result['text']

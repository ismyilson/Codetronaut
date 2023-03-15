import torch
import whisper


device = "cuda" if torch.cuda.is_available() else "cpu"
model = whisper.load_model("small.en", device=device)


def transcribe(file_path):
    """
    Transcribe an audio file to text.
    Args:
        file_path: The audio file path.
    Returns:
        A string containing the audio's transcribed text.
    """

    audio_data = whisper.load_audio(file_path)
    audio_data = whisper.pad_or_trim(audio_data)

    decode_options = {
        'fp16': False,
        'language': 'en',
        'best_of': 5,
        'beam_size': 5,
        'task': 'transcribe'
    }

    result = whisper.transcribe(model,
                                audio_data,
                                temperature=(0.0, 0.2, 0.4, 0.6, 0.8, 1.0),
                                **decode_options)

    # Hacky way to check if it's just noise. It's (for some reason) faster than passing the params to whisper.transcribe
    if result['segments'][0]['avg_logprob'] < -0.7 and result['segments'][0]['no_speech_prob'] > 0.6:
        return ''

    return result['text']

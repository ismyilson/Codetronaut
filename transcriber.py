import whisper
import torch


device = "cuda" if torch.cuda.is_available() else "cpu"
model = whisper.load_model("base", device=device)


CONNECTORS = [
    'to'
]


class UserInput:
    text: str
    words: list

    def __init__(self, text):
        text = text.lower()

        self.text = text
        self.words = self._get_words(text)

    def _get_words(self, text):
        words = []

        text = text.strip()
        idx = text.find(' ')
        while idx != -1:
            word = text[0:idx]
            text = text[idx+1:]

            if self._is_valid_word(word):
                if '.' in word:
                    word = word.replace('.', '')

                    words.append(word)
                    words.append('.')
                else:
                    words.append(word)

            idx = text.find(' ')

        word = text[0:]
        if self._is_valid_word(word):
            if '.' in word:
                word = word.replace('.', '')

                words.append(word)
                words.append('.')
            else:
                words.append(word)

        print(words)
        return words

    def _is_valid_word(self, word):
        if word == '':
            return False

        if self._is_connector(word):
            return False

        return True

    def _is_connector(self, word):
        return word in CONNECTORS

    def word_index(self, word_list):
        for word in word_list:
            word_index = self.words.index(word)

            if word_index != -1:
                return word_index

        return -1

    def contains_command(self, command):
        return any(x in command.cmd for x in self.words)


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

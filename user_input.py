CONNECTORS = [
    'to'
]


class UserInput:
    commands: list

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


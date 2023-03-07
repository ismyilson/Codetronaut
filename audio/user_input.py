CONNECTORS = [
    'to'
]


class UserInput:
    commands: list

    text: str
    words: list

    def __init__(self, text):
        text = text.lower().replace(',', '').replace('!', '')

        print(text)

        self.text = text
        self.words = []

        self._get_words(text)

        print(self.words)

    def _get_words(self, text):
        text = text.strip()
        idx = text.find(' ')
        while idx != -1:
            word = text[0:idx]
            text = text[idx+1:]

            if self._is_valid_word(word):
                self._add_word(word)

            idx = text.find(' ')

        word = text[0:]
        if self._is_valid_word(word):
            self._add_word(word)

    def _is_valid_word(self, word):
        if word == '':
            return False

        if self._is_connector(word):
            return False

        return True

    def _add_word(self, word):
        if '.' in word:
            dot_idx = word.find('.')
            while dot_idx != -1:
                try:
                    if word[dot_idx + 1] == ' ':
                        self.words.append(word.replace('.', ''))
                        self.words.append('..')
                    else:
                        self.words.append(word)

                    dot_idx = word[dot_idx + 1:].find('.')
                except IndexError:
                    self.words.append(word.replace('.', ''))
                    break
        else:
            self.words.append(word)

    def _is_connector(self, word):
        return word in CONNECTORS

    def word_index(self, word_list):
        for word in word_list:
            try:
                word_index = self.words.index(word)
                return word_index
            except ValueError:
                continue

        return -1

    def contains_word(self, command):
        return any(x in command.cmd_text for x in self.words)


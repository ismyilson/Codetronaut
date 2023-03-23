

class UserInput:
    text: str
    raw_text: str

    commands: list[list[str]]

    def __init__(self, text):
        self.raw_text = ''
        self.text = ''

        self.commands = []

        self._process_text(text)

    def _process_text(self, text):
        self.raw_text = text
        self.text = self._make_sanitized_text(text)

        if len(self.text) == 0:
            return

        self.commands = self._get_commands()

    def _make_sanitized_text(self, text):
        text = text.lower()
        text = text.strip()
        text = text.replace('!', '').replace('?', '').replace(',', '')

        return text

    def _get_words(self):
        words = self.text.split(' ')

        to_insert = []
        for idx, word in enumerate(words):
            if word[-1] == '.':
                words[idx] = word[:-1]
                to_insert.append(idx + 1 + len(to_insert))

        for idx in to_insert:
            words.insert(idx, '.')

        return words

    def _get_commands(self):
        words = self._get_words()
        commands = []

        last_idx = 0
        for idx, word in enumerate(words):
            if word == '.' or word == 'and':
                commands.append(words[last_idx:idx])
                last_idx = idx + 1

        if last_idx != len(words):
            commands.append(words[last_idx:])

        return commands

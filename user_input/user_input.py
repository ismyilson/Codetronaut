

class UserInput:
    text: str
    raw_text: str

    commands: list
    words: list

    def __init__(self, text):
        self.raw_text = ''
        self.text = ''

        self.commands = []
        self.words = []

        self._process_text(text)

    def _process_text(self, text):
        self.raw_text = text
        self.text = self._make_sanitized_text(text)

        if len(self.text) == 0:
            return

        self.words = self._get_words()
        self.commands = self._get_commands()

    def _make_sanitized_text(self, text):
        text = text.lower()
        text = text.strip()

        return text

    def _get_words(self):
        words = self.text.split(' ')
        print(words)

        to_insert = []
        for i in range(0, len(words)):
            if words[i][-1] == '.':
                words[i] = words[i][:-1]
                to_insert.append(i + 1 + len(to_insert))

        for idx in to_insert:
            words.insert(idx, '.')

        return words

    def _get_commands(self):
        commands = []

        last_idx = 0
        for i in range(0, len(self.words)):
            if self.words[i] == '.':
                commands.append(' '.join(self.words[last_idx:i]))
                last_idx = i + 1

        if last_idx != len(self.words):
            commands.append(' '.join(self.words[last_idx:]))

        return commands

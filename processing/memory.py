
SUBJECT_WORDS = [
    'it',
    'its',
    'it\'s',
]


class Memory:
    last_subject: str

    def __init__(self):
        self.last_subject = ''

    def set_last_subject(self, action):
        param = ''
        if len(action.command.params) > 0:
            param = action.command.params[0]

        self.last_subject = f'{action.command.cmd[0]} {param}'

    def replace_subject(self, command_words):
        if self.last_subject == '':
            return command_words

        last_subject_words = self.last_subject.split()
        for idx, word in enumerate(command_words):
            if word in SUBJECT_WORDS:
                del command_words[idx]

                for i in range(0, len(last_subject_words)):
                    command_words.insert(idx + i, last_subject_words[i])

        print(f'new command words: {command_words}')
        return command_words

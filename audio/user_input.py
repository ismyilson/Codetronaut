CONNECTORS = [
    'to'
]


class UserInput:
    """
    Helper class for the transcribed audio data.

    Attributes:
        commands: A list of strings representing each command. A Command is usually a sentence.
        text: A string containing the transcribed audio data.
        words: A list of strings containing each word in the text.
    """

    commands: list

    text: str
    words: list

    def __init__(self, text):
        """
        Sanitizes text and breaks it into words.

        Args:
            text: The input text. Usually transcribed audio text, but not limited to.
        """

        text = text.lower().replace(',', '').replace('!', '')

        print(text)

        self.text = text
        self.words = []

        self._get_words(text)

        print(self.words)

    def _get_words(self, text):
        """
        Divides a string into words. If a period is found, it's treated as a word.

        Args:
            text: The string to divide into words.
        """
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
        """
        Checks if a string is a valid word.

        Args:
            word: The string to check.

        Returns:
             True if valid, False otherwise.
        """

        if word == '':
            return False

        if self._is_connector(word):
            return False

        return True

    def _add_word(self, word):
        """
        Adds a word to the list of words. If the word contains a period, it adds the word and the period.

        Args:
            word: The word to add.
        """

        if '.' in word:
            dot_idx = word.find('.')
            while dot_idx != -1:
                try:
                    if word[dot_idx + 1] == ' ':
                        self.words.append(word.replace('.', ''))
                        self.words.append('.')
                    else:
                        self.words.append(word)

                    dot_idx = word[dot_idx + 1:].find('.')
                except IndexError:
                    self.words.append(word.replace('.', ''))
                    break
        else:
            self.words.append(word)

    def _is_connector(self, word):
        """
        Checks if a word is a connector

        Args:
            word: The string to check.

        Returns:
            True if it's a connector, False otherwise.
        """

        return word in CONNECTORS

    def word_index(self, word_list):
        """
        Attempts to find a word, from the given word list, in the user's input.

        Args:
            word_list: A list of strings representing the words. It only needs to find one.

        Returns:
            The index of the word that was found, or -1 if no word is found.
        """

        for word in word_list:
            try:
                word_index = self.words.index(word)
                return word_index
            except ValueError:
                continue

        return -1

    def contains_command(self, command):
        """
        Checks if user's input contains a command.

        Args:
            command: The command to check for.

        Returns:
            True if the command is found, False otherwise.
        """

        return any(x in command.cmd_text for x in self.words)


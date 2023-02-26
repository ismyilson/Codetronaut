import reader

from commands.command_list import COMMAND_LIST
from commands.command import CommandError


class Processor:
    def __init__(self):
        pass

    def process_command(self, user_input):
        print(f'Attempting to process: {user_input.text}')

        result = self._process_command(user_input)
        reader.read_text(result.response)

    def _process_command(self, user_input):
        main_command = self._get_main_command(user_input)
        return main_command.on_command(user_input)

    def _get_main_command(self, user_input):
        for command in COMMAND_LIST:
            if user_input.contains_word(command):
                return command

        raise CommandError('Unknown command')

    def clean_up(self):
        pass

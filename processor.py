import reader

from commands.command_list import COMMAND_LIST
from commands.command import CommandError


def make_response(status, msg):
    return {
        'status': status,
        'msg': msg
    }


class Processor:
    def __init__(self):
        pass

    def process_command(self, user_input):
        print(f'Attempting to process: {user_input.text}')

        result = self._process_command(user_input)
        reader.read_text(result['msg'])

    def _process_command(self, user_input):
        main_command = self._get_main_command(user_input)

        if main_command is None:
            return make_response('failed', 'Unknown command.')

        try:
            response = main_command.on_command(user_input)
        except CommandError as e:
            return make_response('failed', str(e))

        return make_response('success', response)

    def _get_main_command(self, user_input):
        for command in COMMAND_LIST:
            if user_input.contains_word(command):
                return command

        return None

    def clean_up(self):
        pass

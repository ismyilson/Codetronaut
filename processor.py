from commands.command_list import COMMAND_LIST

import reader


def make_response(status, message):
    return {
        'status': status,
        'message': message
    }


class Processor:
    def __init__(self):
        pass

    def process_command(self, user_input):
        print(f'Attempting to process: {user_input.text}')

        result = self._process_command(user_input)

        reader.read_text(result['message'])

    def _process_command(self, user_input):
        main_command = self._get_main_command(user_input)

        if main_command is None:
            return make_response('failed', 'Unknown command')

        main_command.on_command(user_input)
        return make_response('success', '')

    def _get_main_command(self, user_input):
        for command in COMMAND_LIST:
            if any(x in command.cmd for x in user_input.words):
                return command

        return None

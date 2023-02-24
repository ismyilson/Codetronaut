import reader


class Processor:
    def __init__(self):
        pass

    def process_command(self, user_input):
        result = self._process_command(user_input)

        reader.read_text(result['message'])

    def _process_command(self, user_input):
        return {
            'status': 'Success',
            'message': 'Successfully executed command'
        }

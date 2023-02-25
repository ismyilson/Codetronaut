from commands.command import MainCommand, SubCommand, CommandError
from context import CurrentContext
from handlers import win_handler


class SubCommandFile(SubCommand):
    cmd = [
        'file'
    ]

    def on_command(self, user_input):
        command_index = user_input.word_index(self.cmd)

        if command_index == -1:
            raise CommandError('Could not find subcommand')

        file_name = ''.join(user_input.words[command_index + 1:])

        path = win_handler.get_path_to_file(CurrentContext.directory, file_name)
        if path == '':
            return f'File {file_name} not found'

        return CurrentContext.editor.go_to_file(file_name)


class CommandGo(MainCommand):
    cmd = [
        'go',
        'open'
    ]

    sub_commands = [
        SubCommandFile()
    ]

    requires_sub_command = True

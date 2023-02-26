from commands.command import MainCommand, SubCommand, CommandError, CommandStatus, CommandResult
from context import CurrentContext
from handlers import win_handler


class SubCommandGoToFile(SubCommand):
    cmd = [
        'file'
    ]

    def on_command(self, user_input):
        command_index = user_input.word_index(self.cmd)

        if command_index == -1:
            raise CommandError('Could not find subcommand')

        file_name = ''.join(user_input.words[command_index + 1:])

        path = win_handler.get_path_to_file(CurrentContext.workdir, file_name)
        if path == '':
            return CommandResult(CommandStatus.STATUS_FAILED, f'File {file_name} not found')

        if CurrentContext.editor.go_to_file(file_name):
            return CommandResult(CommandStatus.STATUS_SUCCESS, f'File loaded')
        else:
            return CommandResult(CommandStatus.STATUS_FAILED, f'Could not load file')


class CommandGo(MainCommand):
    cmd = [
        'go',
        'open'
    ]

    sub_commands = [
        SubCommandGoToFile()
    ]

    requires_sub_command = True

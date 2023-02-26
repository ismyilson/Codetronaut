from commands.command import MainCommand, SubCommand, CommandError, CommandResult, CommandStatus
from context import CurrentContext


class SubCommandCreateFile(SubCommand):
    cmd = [
        'file'
    ]

    def on_command(self, user_input):
        command_index = user_input.word_index(self.cmd)

        if command_index == -1:
            raise CommandError('Could not find subcommand')

        file_name = ''.join(user_input.words[command_index + 1:])

        path = f'{CurrentContext.workdir}{CurrentContext.current_directory}{file_name}'
        if CurrentContext.editor.create_file(path):
            return CommandResult(CommandStatus.STATUS_SUCCESS, f'File created')
        else:
            return CommandResult(CommandStatus.STATUS_FAILED, f'File already exists')


class CommandCreate(MainCommand):
    cmd = [
        'create'
    ]

    sub_commands = [
        SubCommandCreateFile()
    ]

    requires_sub_command = False

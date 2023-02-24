from commands.command import MainCommand, SubCommand, CommandError


class SubCommandSetEditor(SubCommand):
    cmd = [
        'editor',
        'ide'
    ]

    def get_values(self):
        return [
            (('vscode', 'visualstudiocode'), self.set_vscode)
        ]

    def on_command(self, user_input):
        command_index = user_input.word_index(self.cmd)

        if command_index == -1:
            raise CommandError('Could not find subcommand')

        values = self.get_values()
        ide_name = ''

        for i in range(command_index + 1, len(user_input.words)):
            ide_name += user_input.words[i]

            for value in values:
                if ide_name in value[0]:
                    return value[1]()

        return CommandError('Could not find IDE')

    def set_vscode(self):
        return 'Editor set to VSCode'


class CommandSet(MainCommand):
    cmd = [
        'set'
    ]

    sub_commands = [
        SubCommandSetEditor()
    ]

    requires_sub_command = True

    def on_command(self, user_input):
        for sub_command in self.sub_commands:
            if user_input.contains_command(sub_command):
                return sub_command.on_command(user_input)

        raise CommandError('Set requires something else')

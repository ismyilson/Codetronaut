class BaseCommand:
    cmd: list

    def on_command(self, user_input):
        pass


class MainCommand(BaseCommand):
    sub_commands: list
    requires_sub_command: bool

    def on_command(self, user_input):
        super().on_command(user_input)

        for sub_command in self.sub_commands:
            if user_input.contains_word(sub_command):
                return sub_command.on_command(user_input)

        if self.requires_sub_command:
            raise CommandError(f'{self.cmd[0]} requires subcommand')


class SubCommand(BaseCommand):
    def get_values(self):
        return []


class CommandError(Exception):
    msg: str

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class CommandStatus:
    STATUS_SUCCESS = 'success'
    STATUS_FAILED = 'failed'


class CommandResult:
    status: CommandStatus
    response: str

    def __init__(self, status, response):
        self.status = status
        self.response = response

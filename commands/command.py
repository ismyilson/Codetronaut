class BaseCommand:
    cmd: list

    def on_command(self, user_input):
        return ''


class MainCommand(BaseCommand):
    sub_commands: list
    requires_sub_command: bool


class SubCommand(BaseCommand):
    def get_values(self):
        return []


class CommandError(Exception):
    msg: str

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

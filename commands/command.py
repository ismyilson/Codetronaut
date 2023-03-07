class Command:
    cmd_text: list = []

    requires_data: bool = False
    data: str = None

    def execute(self):
        return

    def _is_valid_data(self):
        return True


class MainCommand(Command):
    sub_commands: list = []

    requires_sub_command: bool = False


class SubCommand(Command):
    pass

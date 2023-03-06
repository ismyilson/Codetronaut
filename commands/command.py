class BaseCommand:
    cmd_text: list = []

    requires_data: bool = False
    data: str = None

    def execute(self):
        return

    def _is_valid_data(self):
        return True


class MainCommand(BaseCommand):
    sub_commands: list = []

    requires_sub_command: bool = False


class SubCommand(BaseCommand):
    pass

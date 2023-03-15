
class BaseCommand:
    cmd: list
    requires_subcommand: bool

    subcommands: list

    def __init__(self, cmd, requires_subcommand):
        self.cmd = cmd
        self.requires_subcommand = requires_subcommand

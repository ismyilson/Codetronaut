import sys

from commands.command import MainCommand


class MainCommandStop(MainCommand):
    cmd_text = [
        'stop',
        'quit',
        'exit'
    ]

    requires_sub_command = False

    def execute(self):
        sys.exit(1)

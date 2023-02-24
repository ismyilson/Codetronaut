import sys

from commands.command import MainCommand


class CommandStop(MainCommand):
    cmd = [
        'stop',
        'quit',
        'exit'
    ]

    requires_sub_command = False

    def on_command(self, user_input):
        sys.exit(0)

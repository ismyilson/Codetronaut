from commands.command import Command


class ActionStatus:
    READY = 'ready'
    INVALID_COMMAND = 'invalid_command'
    INVALID_SUBCOMMAND = 'invalid_subcommand'
    MISSING_DATA = 'missing_data'
    INVALID_DATA = 'invalid_data'


class Action:
    status: ActionStatus
    command: Command

    def __init__(self, status, command):
        self.status = status
        self.command = command

from commands.base_command import BaseCommand


class ActionStatus:
    READY = 'ready'
    INVALID_COMMAND = 'invalid_command'
    INVALID_SUBCOMMAND = 'invalid_subcommand'
    MISSING_DATA = 'missing_data'
    INVALID_DATA = 'invalid_data'
    MISSING_MODIFIERS = 'missing_modifiers'


class Action:
    status: ActionStatus
    command: BaseCommand

    def __init__(self, status, command):
        self.status = status
        self.command = command

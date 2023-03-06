from commands.command import MainCommand


class MainCommandSet(MainCommand):
    cmd_text = [
        'set'
    ]

    sub_commands = [
    ]

    requires_sub_command = True

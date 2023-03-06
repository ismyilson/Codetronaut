from commands.command import MainCommand


class MainCommandGo(MainCommand):
    cmd_text = [
        'go',
        'open'
    ]

    sub_commands = [
    ]

    requires_sub_command = True

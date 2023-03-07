from commands.command import MainCommand, SubCommand


class SubCommandFile(SubCommand):
    cmd_text = [
        'file'
    ]

    requires_data = True


class MainCommandCreate(MainCommand):
    cmd_text = [
        'create'
    ]

    sub_commands = [
        SubCommandFile
    ]

    requires_sub_command = True

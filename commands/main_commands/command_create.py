from commands.command import BaseCommand, SubCommand


class SubCommandFile(SubCommand):
    cmd_text = [
        'file'
    ]

    requires_data = True


class MainCommandCreate(BaseCommand):
    cmd_text = [
        'create'
    ]

    sub_commands = [
        SubCommandFile
    ]

    requires_sub_command = True

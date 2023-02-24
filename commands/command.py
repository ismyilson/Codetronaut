class BaseCommand:
    cmd: list

    def on_command(self, user_input):
        return


class MainCommand(BaseCommand):
    sub_commands: list


class SubCommand(BaseCommand):
    variables: list

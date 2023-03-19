import inspect
import sys
import reader

from commands.base_command import MainCommand, SubCommand
from global_vars import t_event_quit


class CommandHello(MainCommand):
    cmd = ['hello', 'hey', 'hi']

    def execute(self, context):
        reader.read_text('Hey there')


class CommandStop(MainCommand):
    cmd = ['stop', 'quit', 'exit', 'leave', 'bye']

    def execute(self, context):
        t_event_quit.set()


class SubcommandSetIDE(SubCommand):
    cmd = ['ide', 'editor']

    def execute(self, context):
        print('Called set IDE')


class CommandSet(MainCommand):
    cmd = ['set']

    requires_subcommand = True

    subcommands = [
        SubcommandSetIDE
    ]

    def execute(self, context):
        pass


def get_commands():
    commands = []

    module = sys.modules[__name__]
    for c in dir(module):
        klass = getattr(module, c)

        if not inspect.isclass(klass):
            continue

        if not issubclass(klass, MainCommand):
            continue

        if klass is MainCommand:
            continue

        commands.append(klass)

    return commands

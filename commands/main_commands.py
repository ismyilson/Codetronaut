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
        reader.read_text('See you later')

        t_event_quit.set()


class SubcommandSetEditor(SubCommand):
    cmd = ['ide', 'editor']

    def execute(self, context):
        print('Called set Editor')


class CommandSet(MainCommand):
    cmd = ['set']

    requires_subcommand = True

    subcommands = [
        SubcommandSetEditor
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

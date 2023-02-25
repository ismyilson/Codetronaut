from commands.main_commands.command_go import CommandGo
from commands.main_commands.command_stop import CommandStop
from commands.main_commands.command_set import CommandSet


COMMAND_LIST = [
    CommandStop(),
    CommandSet(),
    CommandGo()
]

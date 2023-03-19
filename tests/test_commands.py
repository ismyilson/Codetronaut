import pytest

from commands.main_commands import SubcommandSetEditor


def test_command_set_editor(default_context):
    command = SubcommandSetEditor()

    command.execute()



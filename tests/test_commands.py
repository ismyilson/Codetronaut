import pytest

from commands.commands import SubcommandSetEditor
from editors.base_editor import BaseEditor


class _EditorTest(BaseEditor):
    identifiers = ['testeditor']
    name = 'Test Editor'


def test_command_set_editor(default_context):
    command = SubcommandSetEditor()
    context = default_context()

    context._available_editors = [_EditorTest]

    params = 'to test editor'.split()

    command.set_params(context, params)
    assert command.params == ['testeditor']

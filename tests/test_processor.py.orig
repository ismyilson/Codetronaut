import pytest

from commands.base_command import BaseCommand


class _SubcommandTest(BaseCommand):
    cmd = ['name']

    def execute(self, context):
        pass


class _CommandTest(BaseCommand):
    cmd = ['set']

    subcommands = [
        _SubcommandTest
    ]

    def execute(self, context):
        pass


def _test_get_commands():
    return [
        _CommandTest
    ]


def test_processor_get_main_command_none(get_processor):
    processor = get_processor(_test_get_commands())

    command = 'unknowncommandheretest'.split()
    main_command, idx = processor._get_main_command(command)

    assert main_command is None
    assert idx == -1


def test_processor_get_main_command(get_processor):
    processor = get_processor(_test_get_commands())

    command = 'set this please!'.split()
    main_command, idx = processor._get_main_command(command)

    assert type(main_command) is _CommandTest
    assert idx == 0

    command = 'at once we must set this!'.split()
    main_command, idx = processor._get_main_command(command)

    assert type(main_command) is _CommandTest
    assert idx == 4

    command = 'set'.split()
    main_command, idx = processor._get_main_command(command)

    assert type(main_command) is _CommandTest
    assert idx == 0


def test_processor_get_sub_command_none(get_processor):
    processor = get_processor(_test_get_commands())

    command = 'set something here'.split()
    main_command, idx = processor._get_main_command(command)
    sub_command, idx = processor._get_sub_command(command, main_command)

    assert sub_command is None
    assert idx == -1


def test_processor_get_sub_command(get_processor):
    processor = get_processor(_test_get_commands())

    command = 'set name to something'.split()
    main_command, idx = processor._get_main_command(command)
    sub_command, idx = processor._get_sub_command(command, main_command)

    assert type(sub_command) is _SubcommandTest
    assert idx == 1

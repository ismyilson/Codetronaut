from unittest.mock import patch, PropertyMock

import pytest

import queue

from commands.base_command import BaseCommand
from processor import Processor


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


@pytest.fixture
def _get_processor():
    processor_queue = queue.Queue()
    gui_data_queue = queue.Queue()

    processor = Processor(processor_queue, gui_data_queue)

    processor._commands = _test_get_commands()
    return processor


def _test_get_commands():
    return [
        _CommandTest
    ]


def test_processor_get_main_command_none(_get_processor):
    processor = _get_processor

    command = 'unknowncommandheretest'.split()
    main_command, idx = processor._get_main_command(command)

    assert main_command is None
    assert idx == -1


def test_processor_get_main_command(_get_processor):
    processor = _get_processor

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


def test_processor_get_sub_command_none(_get_processor):
    processor = _get_processor

    command = 'set something here'.split()
    main_command, idx = processor._get_main_command(command)
    sub_command, idx = processor._get_sub_command(command, main_command)

    assert sub_command is None
    assert idx == -1


def test_processor_get_sub_command(_get_processor):
    processor = _get_processor

    command = 'set name to something'.split()
    main_command, idx = processor._get_main_command(command)
    sub_command, idx = processor._get_sub_command(command, main_command)

    assert type(sub_command) is _SubcommandTest
    assert idx == 1

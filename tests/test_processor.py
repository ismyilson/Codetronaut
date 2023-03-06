import pytest

from commands.action import ActionStatus
from commands.main_commands.command_stop import MainCommandStop
from processor import Processor

from commands.main_commands.command_create import MainCommandCreate, SubCommandFile
from commands.main_commands.command_go import MainCommandGo
from commands.main_commands.command_set import MainCommandSet


def test_get_main_command_pass():
    processor = Processor()

    command_text = 'create file'
    ret, text = processor._get_main_command(command_text)

    assert ret is MainCommandCreate
    assert text == 'file'

    command_text = 'go to file'
    ret, text = processor._get_main_command(command_text)

    assert ret is MainCommandGo
    assert text == 'to file'

    command_text = 'some gibberish set'
    ret, text = processor._get_main_command(command_text)

    assert ret is MainCommandSet
    assert text == ''

    command_text = 'unknowncommandhere'
    ret, text = processor._get_main_command(command_text)

    assert ret is None
    assert text == command_text


def test_get_sub_command_pass():
    processor = Processor()

    command_text = 'file Main.java'
    ret, text = processor._get_sub_command(command_text, MainCommandCreate)

    assert ret is SubCommandFile
    assert text == 'Main.java'

    command_text = 'unknownstuff Main.java'
    ret, text = processor._get_sub_command(command_text, MainCommandCreate)

    assert ret is None
    assert text == command_text


def test_process_command_pass_ready():
    processor = Processor()

    command_text = 'create file main.java'
    action = processor.process_command(command_text)

    assert action.status == ActionStatus.READY
    assert action.command == SubCommandFile

    command_text = 'stop gibberish data here'
    action = processor.process_command(command_text)

    assert action.status == ActionStatus.READY
    assert action.command == MainCommandStop


def test_process_command_pass_invalid_subcommand():
    processor = Processor()

    command_text = 'create'
    action = processor.process_command(command_text)

    assert action.status == ActionStatus.INVALID_SUBCOMMAND
    assert action.command == MainCommandCreate


def test_process_command_pass_missing_data():
    processor = Processor()

    command_text = 'create file'
    action = processor.process_command(command_text)

    assert action.status == ActionStatus.MISSING_DATA
    assert action.command == SubCommandFile


def test_process_command_pass_invalid_data():
    pass

import pytest

from input_handling.user_input import UserInput


def test_user_input_empty_text():
    text = ''
    user_input = UserInput(text)

    assert user_input.raw_text == text
    assert user_input.text == ''
    assert len(user_input.commands) == 0


def test_user_input_single_word_single_command_text():
    text = 'Create'
    user_input = UserInput(text)

    assert user_input.raw_text == text
    assert user_input.text == 'create'
    assert len(user_input.commands) == 1
    assert len(user_input.commands[0]) == 1
    assert user_input.commands[0][0] == 'create'


def test_user_input_many_words_single_command_text():
    text = 'Create a file'
    user_input = UserInput(text)

    assert user_input.raw_text == text
    assert user_input.text == 'create a file'
    assert len(user_input.commands) == 1
    assert len(user_input.commands[0]) == 3
    assert ' '.join(user_input.commands[0]) == 'create a file'


def test_user_input_many_words_many_commands_text():
    text = 'Create a file. Make it something.'
    user_input = UserInput(text)

    assert user_input.raw_text == text
    assert user_input.text == 'create a file. make it something.'
    assert len(user_input.commands) == 2
    assert len(user_input.commands[0]) == 3
    assert len(user_input.commands[1]) == 3
    assert ' '.join(user_input.commands[0]) == 'create a file'
    assert ' '.join(user_input.commands[1]) == 'make it something'


def test_user_input_filter_dots():
    # Only one dot should count as word
    text = 'Create file main.java.'
    user_input = UserInput(text)

    assert user_input.raw_text == text
    assert user_input.text == 'create file main.java.'
    assert len(user_input.commands) == 1
    assert len(user_input.commands[0]) == 3
    assert ' '.join(user_input.commands[0]) == 'create file main.java'

    # No dots should be filtered here
    text = 'Create file main.java'
    user_input = UserInput(text)

    assert user_input.raw_text == text
    assert user_input.text == 'create file main.java'
    assert len(user_input.commands) == 1
    assert len(user_input.commands[0]) == 3
    assert ' '.join(user_input.commands[0]) == 'create file main.java'


def test_user_input_remove_spaces():
    text = '   Create file main.java   '
    user_input = UserInput(text)

    assert user_input.raw_text == text
    assert user_input.text == 'create file main.java'
    assert len(user_input.commands) == 1
    assert len(user_input.commands[0]) == 3
    assert ' '.join(user_input.commands[0]) == 'create file main.java'

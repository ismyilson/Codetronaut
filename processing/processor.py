import threading
import time
import reader

from queue import Queue, Empty

from commands.action import Action, ActionStatus
from commands.commands import get_commands

from input_handling.user_input import UserInput

from processing.context import Context
from processing.memory import Memory

from global_vars import t_event_record, t_event_quit


class Processor(threading.Thread):
    context: Context
    memory: Memory

    _queue: Queue
    _gui_data_queue: Queue

    _commands: list

    _current_command_idx: int

    def __init__(self, processor_queue, gui_data_queue):
        super().__init__()

        self._queue = processor_queue
        self._gui_data_queue = gui_data_queue

    def _clean_up(self):
        print('Cleaning up processor')

        self.context.clean_up()

    def _loop(self):
        while not t_event_quit.is_set():
            try:
                user_input = self._queue.get(block=True, timeout=1)
            except Empty:
                continue

            self._gui_data_queue.put(('-TRANSCRIBEDTEXT1-', user_input.raw_text))

            self._process(user_input)

            t_event_record.set()

        self._clean_up()

    def _process(self, user_input):
        actions = []
        for idx, command_words in enumerate(user_input.commands):
            self._current_command_idx = idx

            action = self._process_new_command_text(command_words)

            if action.status == ActionStatus.READY:
                self.memory.set_last_subject(action)
                self.memory.set_last_command(action)

            actions.append(action)

        for action in actions:
            self._process_action(action)
            time.sleep(0.3)

    def _process_new_command_text(self, command_words):
        print(f'Attempting to process: {command_words}')

        command_words = self.memory.replace_subject(command_words)

        main_cmd, main_cmd_idx = self._get_main_command(command_words)

        # Handle no main command
        if main_cmd is None:
            # There's a possibility we recognized "and" as another command, so just load up the last command and copy it
            if self._current_command_idx > 0:
                command_words = self.memory.add_last_command(command_words)
                main_cmd, main_cmd_idx = self._get_main_command(command_words)

                if main_cmd is None:
                    return Action(ActionStatus.INVALID_COMMAND, None)
            else:
                return Action(ActionStatus.INVALID_COMMAND, None)

        # Handle main command can only be run without parameters
        if main_cmd.is_no_params_only:
            return Action(ActionStatus.READY, main_cmd)

        sub_cmd, sub_cmd_idx = self._get_sub_command(command_words, main_cmd)

        # Handle no sub command
        if sub_cmd is None:
            if main_cmd.requires_subcommand:
                return Action(ActionStatus.INVALID_SUBCOMMAND, main_cmd)

            if main_cmd.default_subcommand:
                return self._handle_command(main_cmd.default_subcommand(), command_words, main_cmd_idx, main_cmd_idx, main_command=main_cmd)

            return self._handle_command(main_cmd, command_words, main_cmd_idx, main_cmd_idx)

        return self._handle_command(sub_cmd, command_words, main_cmd_idx, sub_cmd_idx, main_command=main_cmd)

    def _get_main_command(self, command_words):
        for idx, cmd_word in enumerate(command_words):
            for main_command in self._commands:
                for mc_text in main_command.cmd:
                    if cmd_word == mc_text:
                        return main_command(), idx

        return None, -1

    def _get_sub_command(self, command_words, main_command):
        for sub_cmd in main_command.subcommands:
            for sc_text in sub_cmd.cmd:
                for idx, cmd_word in enumerate(command_words):
                    if cmd_word == sc_text:
                        return sub_cmd(), idx

        return None, -1

    def _handle_command(self, command, command_words, main_cmd_idx, sub_cmd_idx, main_command=None):
        # First grab modifiers
        from_idx = 0
        if main_cmd_idx != sub_cmd_idx:
            from_idx = main_cmd_idx + 1

        if not command.set_modifiers(self.context, command_words[from_idx:sub_cmd_idx]):
            if command.requires_modifiers:
                return Action(ActionStatus.MISSING_MODIFIERS, command)

        # Then grab params
        if sub_cmd_idx == len(command_words) - 1:
            if command.requires_params:
                return Action(ActionStatus.MISSING_DATA, command)

            return Action(ActionStatus.READY, command, main_command)

        params = command_words[sub_cmd_idx + 1:]
        if not command.set_params(self.context, params):
            return Action(ActionStatus.INVALID_DATA, command)

        return Action(ActionStatus.READY, command, main_command)

    def _process_action(self, action):
        if action.status == ActionStatus.INVALID_COMMAND:
            # Not sure if I want this, its a little annoying..
            # reader.read_text(f'Invalid command')
            return

        if action.status == ActionStatus.INVALID_SUBCOMMAND:
            reader.read_text(f'Invalid subcommand for command: {action.command.cmd[0]}')
            return

        if action.status == ActionStatus.MISSING_DATA:
            if action.command.last_error_message:
                reader.read_text(action.command.last_error_message)
            else:
                reader.read_text(f'Missing data for command {action.command.cmd[0]}')
            return

        if action.status == ActionStatus.INVALID_DATA:
            if action.command.last_error_message:
                reader.read_text(action.command.last_error_message)
            else:
                reader.read_text(f'Invalid data for command {action.command.cmd[0]}')
            return

        if action.status == ActionStatus.MISSING_MODIFIERS:
            if action.command.last_error_message:
                reader.read_text(action.command.last_error_message)
            else:
                reader.read_text(f'Invalid modifiers for command {action.command.cmd[0]}')
            return

        if action.status == ActionStatus.READY:
            print(f'Executing command with params: {action.command.params}')

            if not action.command.validate_params(self.context):
                if action.command.last_error_message:
                    reader.read_text(action.command.last_error_message)
                else:
                    reader.read_text(f'Invalid parameters for command {action.command.cmd[0]}')
                return

            action.command.execute(self.context)
            return

    def run(self):
        self._commands = get_commands()
        print(f'Loaded {len(self._commands)} commands')

        self.context = Context()
        self.context.load_config()

        self.memory = Memory()

        self._loop()

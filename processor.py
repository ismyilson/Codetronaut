import threading

from queue import Queue, Empty

from commands.main_commands import get_commands

from context import Context
from global_vars import t_event_record, t_event_quit


class Processor(threading.Thread):
    context: Context

    _queue: Queue
    _gui_data_queue: Queue

    _commands: list

    def __init__(self, processor_queue, gui_data_queue):
        super().__init__()

        self._queue = processor_queue
        self._gui_data_queue = gui_data_queue

        self._commands = get_commands()
        print(f'Loaded {len(self._commands)} commands')

        self.context = Context()

    def _loop(self):
        while not t_event_quit.is_set():
            try:
                user_input = self._queue.get(block=True, timeout=1)
            except Empty:
                continue

            self._gui_data_queue.put(('-TRANSCRIBEDTEXT-', user_input.raw_text))

            self._process(user_input)

            t_event_record.set()

        self._clean_up()

    def _process(self, user_input):
        for command in user_input.commands:
            self._process_new_command(command)

    def _process_new_command(self, command):
        print(f'Attempting to process: {command}')

        main_cmd, main_cmd_idx = self._get_main_command(command)
        if main_cmd is None:
            print(f'Unrecognized command: "{command}"')
            return

        if main_cmd.is_no_params_only:
            main_cmd.execute(self.context)
            return

        sub_cmd, sub_cmd_idx = self._get_sub_command(command, main_cmd)
        if sub_cmd is None:
            print(f'No sub cmd')
            return

        print(f'Subcmd found: {sub_cmd.cmd[0]} at {sub_cmd_idx}')
        return


        # main_command, mc_idx = self._get_main_command(command_words)
        # if main_command is None:
        #     print(f'Unrecognized command: "{command}"')
        #     return
        #
        # if main_command.is_no_params_only:
        #     main_command.execute(self.context)
        #     return
        #
        # sub_command = self._get_sub_command(command, main_command)
        # if sub_command is None:
        #     if main_command.requires_subcommand:
        #         print(f'Command {main_command.cmd[0]} requires subcommand')
        #         return
        #     else:
        #         main_command.execute(self.context)
        #         return
        #
        # sub_command.execute(self.context)

    def _get_main_command(self, command):
        for main_command in self._commands:
            for mc_text in main_command.cmd:
                for idx, cmd_word in enumerate(command):
                    if cmd_word == mc_text:
                        return main_command(), idx

        return None, -1

    def _get_sub_command(self, command, main_command):
        for sub_cmd in main_command.subcommands:
            for sc_text in sub_cmd.cmd:
                for idx, cmd_word in enumerate(command):
                    if cmd_word == sc_text:
                        return sub_cmd(), idx

        return None, -1

    def _clean_up(self):
        print('Cleaning up processor')

    def run(self):
        self._loop()

from commands.action import Action, ActionStatus
from commands.command_list import COMMAND_LIST


class Processor:
    def __init__(self):
        pass

    def process_commands(self, command_text):
        """
        Processes a list of commands into their respective actions.

        Args:
            command_text: A list of strings representing the commands.

        Returns:
            A list of Action objects.

            The length of the list is always equal to the length of the list of commands.
        """

        actions = []

        for cmd_text in command_text:
            action = self.process_command(cmd_text)
            actions.append(action)

        return actions

    def process_command(self, command_text):
        """
        Processes a command into its action.

        Args:
            command_text: A string representing the command.

        Returns:
            An object of type Action.
        """

        main_command, command_text = self._get_main_command(command_text)
        if main_command is None:
            return Action(ActionStatus.INVALID_COMMAND, None)

        sub_command, command_text = self._get_sub_command(command_text, main_command)
        if sub_command is None:
            if main_command.requires_sub_command:
                return Action(ActionStatus.INVALID_SUBCOMMAND, main_command)

            return self._get_action_for_command(main_command, command_text)

        return self._get_action_for_command(sub_command, command_text)

    def _get_main_command(self, command_text):
        """
        Attempts to identify the main command in a given command string.

        Args:
            command_text: A string representing the command.

        Returns:
            An object of type MainCommand, and a substring of the "command_text" parameter, from the index of where the
            main command has been found until the end of the string.

            If no main command is found, returns None, and the original "command_text" parameter.
        """

        for cmd in COMMAND_LIST:
            for i in range(0, len(cmd.cmd_text)):
                idx = command_text.find(cmd.cmd_text[i])
                if idx == -1:
                    continue

                command_text = command_text[idx + len(cmd.cmd_text[i]) + 1:]
                return cmd, command_text

        return None, command_text

    def _get_sub_command(self, command_text, main_command):
        """
        Attempts to identify the subcommand of a main command in a given command string.

        Args:
            command_text: A string representing the command.

            main_command: Object of type MainCommand.

        Returns:
            An object of type SubCommand, and a substring of the "command_text" parameter, from the index of where the
            sub command has been found until the end of the string.

            If no sub command is found, returns None, and the original "command_text" parameter.
        """

        for cmd in main_command.sub_commands:
            for i in range(0, len(cmd.cmd_text)):
                idx = command_text.find(cmd.cmd_text[i])
                if idx == -1:
                    continue

                command_text = command_text[idx + len(cmd.cmd_text[i]) + 1:]
                return cmd, command_text

        return None, command_text

    def _get_action_for_command(self, command, data):
        command.data = data

        if len(data) < 1:
            if command.requires_data:
                return Action(ActionStatus.MISSING_DATA, command)

            return Action(ActionStatus.READY, command)

        # if not command.is_valid_data(data):
            # return Action(ActionStatus.INVALID_DATA, command)

        return Action(ActionStatus.READY, command)

import tkinter as tk

from tkinter.filedialog import askdirectory

from commands.command import MainCommand, SubCommand, CommandError, CommandResult, CommandStatus
from context import CurrentContext
from editors.vscode import EditorVsCode


class SubCommandSetDirectory(SubCommand):
    cmd = [
        'directory',
    ]

    def on_command(self, user_input):
        root = tk.Tk()

        root.withdraw()
        root.overrideredirect(True)
        root.geometry('0x0+0+0')

        root.deiconify()
        root.lift()
        root.focus_force()

        path = askdirectory(title='Select Folder')  # shows dialog box and return the path
        root.destroy()

        if path is None or path == '':
            raise CommandError('Invalid directory')

        folder = path[path.rindex('/') + 1:]

        CurrentContext.workdir = path
        CurrentContext.current_directory = '/'
        return CommandResult(CommandStatus.STATUS_SUCCESS, f'Work directory set to {folder}')


class SubCommandSetEditor(SubCommand):
    cmd = [
        'editor',
        'ide'
    ]

    def get_values(self):
        return [
            (('vscode', 'visualstudiocode'), self.set_vscode)
        ]

    def on_command(self, user_input):
        command_index = user_input.word_index(self.cmd)

        if command_index == -1:
            raise CommandError('Could not find subcommand')

        values = self.get_values()
        ide_name = ''

        for i in range(command_index + 1, len(user_input.words)):
            ide_name += user_input.words[i]

            for value in values:
                if ide_name in value[0]:
                    ret = value[1]()

                    if ret.status == CommandStatus.STATUS_SUCCESS:
                        CurrentContext.editor.run(CurrentContext.workdir)

                    return ret

        return CommandError('Could not find Editor')

    def set_vscode(self):
        CurrentContext.editor = EditorVsCode()
        return CommandResult(CommandStatus.STATUS_SUCCESS, 'Editor set to VSCode')


class CommandSet(MainCommand):
    cmd = [
        'set'
    ]

    sub_commands = [
        SubCommandSetEditor(),
        SubCommandSetDirectory()
    ]

    requires_sub_command = True

import reader

from commands.base_command import MainCommand, SubCommand
from global_vars import t_event_quit
from utils import get_classes_in_module


def get_commands():
    return get_classes_in_module(__name__, subclass_of=MainCommand)


class CommandHello(MainCommand):
    cmd = ['hello', 'hey', 'hi']

    def execute(self, context):
        reader.read_text('Hey there')


class CommandStop(MainCommand):
    cmd = ['stop', 'quit', 'exit', 'leave', 'bye']

    def execute(self, context):
        reader.read_text('See you later')

        t_event_quit.set()


class SubcommandSetEditor(SubCommand):
    cmd = ['ide', 'editor']

    requires_params = True

    def execute(self, context):
        context.set_editor(self.params[0])

    def _valid_params(self, context, params):
        param = ''

        for p in params:
            if p == 'to':
                continue

            param += p

        if not context.is_valid_editor_name(param):
            return []

        return [param]


class SubcommandSetWorkdir(SubCommand):
    cmd = ['workdir', 'work directory', 'directory']

    requires_params = False

    def execute(self, context):
        from tkinter.filedialog import askdirectory
        path = askdirectory(title='Select folder')

        if path is None:
            print('No directory set')
            return

        context.set_workdir(path)


class CommandSet(MainCommand):
    cmd = ['set']

    requires_subcommand = True

    subcommands = [
        SubcommandSetEditor,
        SubcommandSetWorkdir
    ]


class SubcommandOpenFile(SubCommand):
    cmd = ['file']

    requires_params = True

    def execute(self, context):
        if len(self.params) > 1:
            print('multiple params')
            return

        context.go_to_file(self.params[0])

    def _valid_params(self, context, params):
        valid_params = []

        file_name = ''.join(params)
        file_ext = None
        check_file_ext = False

        if self.modifiers:
            file_ext = self.modifiers[0]
            check_file_ext = True
        else:
            idx = file_name.rfind('.')
            if idx != -1:
                file_ext = file_name[file_ext:]
                check_file_ext = True

        files = context.get_files_in_directory(context.workdir)

        for file in files:
            if check_file_ext and file[1] != file_ext:
                continue

            if file[0] in file_name:
                valid_params.append(''.join(file))

        return valid_params

    def _valid_modifiers(self, context, modifiers):
        mods = []

        for mod in modifiers:
            ext = context.get_extension_by_prog_name(mod)

            if ext is None:
                continue

            mods.append(ext)

        return mods


class SubcommandOpenEditor(SubCommand):
    cmd = ['editor']

    requires_params = False

    def execute(self, context):
        context.start_editor()


class CommandOpen(MainCommand):
    cmd = ['open']

    requires_subcommand = True

    subcommands = [
        SubcommandOpenEditor,
        SubcommandOpenFile
    ]


class SubcommandCreateFile(SubCommand):
    cmd = ['file']

    requires_params = True

    def execute(self, context):
        context.create_file(self.params[0])

    def _valid_params(self, context, params):
        file_name = ''.join(params)

        if self.modifiers:
            file_name += self.modifiers[0]

        return [file_name]

    def _valid_modifiers(self, context, modifiers):
        for mod in modifiers:
            ext = context.get_extension_by_prog_name(mod)

            if ext is None:
                continue

            return [ext]

        return []


class CommandCreate(MainCommand):
    cmd = ['create']

    requires_subcommand = True

    subcommands = [
        SubcommandCreateFile
    ]

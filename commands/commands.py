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

    def validate_params(self, context):
        if not context.is_valid_editor_name(self.params[0]):
            return False

        return True

    def _valid_params(self, context, params):
        param = ''

        for p in params:
            if p == 'to':
                continue

            param += p

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


class SubcommandSetVariable(SubCommand):
    cmd = ['variable', 'var', 'attribute']

    requires_params = True

    def execute(self, context):
        context.set_variable(self.params[0], self.params[1])

    def _valid_params(self, context, params):
        try:
            idx = params.index('to')
        except ValueError:
            return []

        var_name = ''.join(params[:idx])
        var_value = ''.join(params[idx+1:])

        return [var_name, var_value]


class CommandSet(MainCommand):
    cmd = ['set']

    requires_subcommand = True

    subcommands = [
        SubcommandSetEditor,
        SubcommandSetWorkdir,
        SubcommandSetVariable
    ]


class SubcommandOpenFile(SubCommand):
    cmd = ['file']

    requires_params = True

    def execute(self, context):
        if len(self.params) > 1:
            print('multiple params')
            return

        context.go_to_file(self.params[0])

    def validate_params(self, context):
        file_name = self.params[0]

        files = context.get_files_in_directory(context.workdir)
        for file in files:
            if file[0] in file_name:
                self.params[0] = ''.join(file)
                return True

        return False

    def _valid_params(self, context, params):
        file_name = ''.join([param.title() for param in params])
        file_ext = ''
        if self.modifiers:
            file_ext = self.modifiers[0]

        return [f'{file_name}{file_ext}']

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

    def validate_params(self, context):
        if context.file_exists(self.params[0]):
            return False

        return True

    def _valid_params(self, context, params):
        file_name = ''.join([param.title() for param in params])

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


class SubcommandCreateClass(SubCommand):
    cmd = ['class']

    requires_params = True

    def execute(self, context):
        context.create_class(self.params[0])

    def _valid_params(self, context, params):
        param = ''.join([param.title() for param in params])
        return [param]


class SubcommandCreateVariable(SubCommand):
    cmd = ['variable', 'var', 'attribute']

    requires_params = True

    requires_modifiers = True

    def execute(self, context):
        var_type = self.modifiers[0]
        var_name = self.params[0]

        context.create_variable(var_type, var_name)

    def validate_params(self, context):
        # Need to check if the language requires variable type here
        return True

    def _valid_params(self, context, params):
        var_name = ''.join(params)
        return [var_name]

    def _valid_modifiers(self, context, modifiers):
        var_type = ''.join([mod.title() for mod in modifiers])
        return [var_type]


class SubcommandCreateMethod(SubCommand):
    cmd = ['method', 'function']

    requires_params = True
    requires_modifiers = False

    _func_data: dict

    def execute(self, context):
        context.create_method(self.params[0], self._func_data['access_type'], self._func_data['is_static'], self._func_data['ret_type'])

    def validate_params(self, context):
        self._func_data = {
            'access_type': 'public',
            'is_static': False,
            'ret_type': 'void',
        }

        for mod in self.modifiers:
            if mod in ['public', 'private', 'protected']:
                self._func_data['access_type'] = mod
            elif mod in ['static']:
                self._func_data['is_static'] = True
            elif mod in ['void', 'int', 'string']:
                self._func_data['ret_type'] = mod

        return True

    def _valid_params(self, context, params):
        method_name = ''.join([param.title() for param in params])

        if method_name == '':
            return []

        return [method_name]

    def _valid_modifiers(self, context, modifiers):
        return modifiers


class CommandCreate(MainCommand):
    cmd = ['create']

    requires_subcommand = True

    subcommands = [
        SubcommandCreateFile,
        SubcommandCreateClass,
        SubcommandCreateVariable,
        SubcommandCreateMethod
    ]


class SubcommandGoLine(SubCommand):
    cmd = ['line']

    requires_params = True

    def execute(self, context):
        context.go_to_line(self.params[0])

    def validate_params(self, context):
        if len(self.params) < 1:
            return True

        if int(self.params[0]) > context.get_current_file_line_count():
            return False

        return True

    def _valid_params(self, context, params):
        num_str = ''
        for param in params:
            param = param.replace(',', '').replace('-', '')
            if not param.isnumeric():
                break

            num_str += param

        return [num_str]


class SubcommandGoFile(SubcommandOpenFile):
    pass


class CommandGo(MainCommand):
    cmd = ['go']

    requires_subcommand = True

    subcommands = [
        SubcommandGoLine,
        SubcommandGoFile,
    ]

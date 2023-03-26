import reader

from commands.base_command import MainCommand, SubCommand
from global_vars import t_event_quit
from utils import get_classes_in_module, last_index_of_list


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
        if self.params[2]:
            context.set_variable_initial_value(self.params[0], self.params[1])
        else:
            context.set_variable(self.params[0], self.params[1])

    def _valid_params(self, context, params):
        initial_value = False
        if 'initial' in params and 'value' in params:
            initial_value = True
            params.remove('initial')
            params.remove('value')

        try:
            idx = params.index('to')
        except ValueError:
            return []

        var_name = ''.join(params[:idx])

        var_value_params = params[idx+1:]
        if 'new' in var_value_params:
            idx = var_value_params.index('new')
            var_value = 'new '
            var_value += ''.join([val.title() for val in var_value_params[idx+1:]])
            var_value += '()'
        else:
            var_value = ''.join(params[idx+1])

        return [var_name, var_value, initial_value]


class CommandSet(MainCommand):
    cmd = ['set']

    requires_subcommand = False
    default_subcommand = SubcommandSetVariable

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
            if context.is_valid_extension(mod):
                return [mod]

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

        if var_type.lower() in ['int', 'boolean', 'char']:
            var_type = var_type.lower()

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
        SubcommandCreateMethod,
    ]


class SubcommandGoLine(SubCommand):
    cmd = ['line']

    requires_params = True

    def execute(self, context):
        context.go_to_line(self.params[0])

    def validate_params(self, context):
        if len(self.params) < 1:
            return False

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


class SubcommandDeleteLine(SubCommand):
    cmd = ['line', 'lines']

    requires_params = False

    def execute(self, context):
        line_start = None
        line_end = None

        if len(self.params) == 1:
            line_start = self.params[0]
        elif len(self.params) > 1:
            line_start = self.params[0]
            line_end = self.params[1]

        context.delete_lines(line_start, line_end)

    def validate_params(self, context):
        return True

    def _valid_params(self, context, params):
        if len(params) == 1:
            return [params[0]]

        line_start = ''
        line_end = ''

        switch = False
        for param in params:
            if param.isnumeric():
                if switch:
                    line_end += param
                else:
                    line_start += param
            else:
                if param == 'to' or param == 'through':
                    switch = True
                    continue

        return [line_start, line_end]


class CommandDelete(MainCommand):
    cmd = ['delete']

    requires_subcommand = True

    subcommands = [
        SubcommandDeleteLine
    ]


class SubcommandRenameVariable(SubCommand):
    cmd = ['variable', 'var']

    requires_params = True

    def execute(self, context):
        context.rename_variable(self.params[0], self.params[1])

    def validate_params(self, context):
        # Need context.find_variable here
        if self.params[0] == '':
            return False

        if self.params[1] == '':
            return False

        return True

    def _valid_params(self, context, params):
        var_name = ''
        new_var_name = ''

        try:
            to_idx = last_index_of_list(params, 'to')
        except IndexError:
            return []

        for idx, param in enumerate(params):
            if idx < to_idx:
                var_name += param
            elif idx > to_idx:
                new_var_name += param

        return [var_name, new_var_name]


class CommandRename(MainCommand):
    cmd = ['rename']

    requires_subcommand = True

    subcommands = [
        SubcommandRenameVariable
    ]


class CommandIf(MainCommand):
    cmd = ['if']

    requires_subcommand = False

    requires_params = True

    def execute(self, context):
        context.add_if_condition(self.params[0], self.params[1], self.params[2])

    def _valid_params(self, context, params):
        valid_params = self._parse_if_condition(params)
        return valid_params

    def _parse_if_condition(self, params):
        complete_sentence = ' '.join(params)

        operations = {
            'is greater than': '>',
            'is higher than': '>',
            'is greater or equal to': '>=',
            'is higher or equal to': '>=',
            'is less than': '<',
            'is lower than': '<',
            'is less or equal to': '<=',
            'is lower or equal to': '<=',
            'is equal to': '==',
            'is true': 'true',
            'is false': 'false'
        }

        idx_start = -1
        idx_end = -1
        operation = None
        for special in operations.keys():
            if special in complete_sentence:
                idx_start = complete_sentence.index(special)
                idx_end = idx_start + len(special) + 1
                operation = special
                break

        if idx_start == -1:
            print('Not found')
            return

        operation = operations.get(operation)

        first_param = complete_sentence[:idx_start].replace(' ', '')
        second_param = complete_sentence[idx_end:].replace(' ', '')

        if operation == 'true':
            operation = '=='
            second_param = 'true'
        elif operation == 'false':
            operation = '=='
            second_param = 'false'

        return [first_param, operation, second_param]


class CommandReturn(MainCommand):
    cmd = ['return']

    requires_subcommand = False

    requires_params = True

    def execute(self, context):
        context.add_return(self.params)

    def _valid_params(self, context, params):
        complete_sentence = ' '.join(params)
        operations = {
            'plus': '+',
            'minus': '-',
            'multiplied by': '*',
            'divided by': '/'
        }

        operation = None
        idx_start = -1
        idx_end = -1
        for special in operations.keys():
            if special in complete_sentence:
                idx_start = complete_sentence.index(special)
                idx_end = idx_start + len(special) + 1
                operation = special
                break

        # Single variable
        if idx_start == -1:
            return [''.join(params)]

        operation = operations.get(operation)

        first_param = complete_sentence[:idx_start].replace(' ', '')
        second_param = complete_sentence[idx_end:].replace(' ', '')

        return [first_param, operation, second_param]


class SubcommandSelectLine(SubCommand):
    cmd = ['line']

    requires_params = False

    def execute(self, context):
        line = self.params[0] if len(self.params) > 0 else None

        context.select_line(line)

    def _valid_params(self, context, params):
        param = ''.join([param for param in params if param.isnumeric()])
        return [param]


class CommandSelect(MainCommand):
    cmd = ['select']

    requires_subcommand = True

    subcommands = [
        SubcommandSelectLine
    ]


class CommandCall(MainCommand):
    cmd = ['call']

    requires_subcommand = False

    requires_params = True

    def execute(self, context):
        if len(self.params) > 1:
            method = f'{self.params[1]}.{self.params[0]}'
        else:
            method = self.params[0]

        context.add_call_method(method)

    def validate_params(self, context):
        method_data = context.get_method_data(self.params[0])

        if method_data is None:
            return False

        self.params[0] = method_data['name']
        return True

    def _valid_params(self, context, params):
        var_name = None
        method_name = ''
        for param in params:
            if '.' in param:  # Variable and method
                idx = param.index('.')
                var_name = param[:idx]
                method_name = param[idx+1:]
                break

            method_name += param.title()

        if method_name == '':
            return []

        return [method_name, var_name]


class CommandPrint(MainCommand):
    cmd = ['print']

    requires_params = True

    def execute(self, context):
        context.add_print(self.params)

    def _valid_params(self, context, params):
        param = ''.join(params)
        return [param]


class SubcommandAddParameter(SubCommand):
    cmd = ['parameter']

    requires_params = True
    requires_modifiers = False

    def execute(self, context):
        var_type = self.modifiers[0] if len(self.modifiers) > 0 else None
        method_name = self.params[0]
        var_name = self.params[1]

        context.add_parameter_to_method(method_name, var_name, var_type)

    def validate_params(self, context):
        method_data = context.get_method_data(self.params[0])

        return method_data is not None

    def _valid_params(self, context, params):
        try:
            to_idx = last_index_of_list(params, 'to')
        except IndexError:
            return []

        var_name = ''.join(params[:to_idx])
        method_name = ''.join(params[to_idx+1:])

        return [method_name, var_name]

    def _valid_modifiers(self, context, modifiers):
        var_type = ''.join([mod.title() for mod in modifiers])

        if var_type.lower() in ['int', 'boolean', 'char']:
            var_type = var_type.lower()

        return [var_type]


class CommandAdd(MainCommand):
    cmd = ['add']

    requires_subcommand = True

    subcommands = [
        SubcommandAddParameter
    ]


class CommandFor(MainCommand):
    cmd = ['for']

    requires_subcommand = False

    requires_params = True

    def execute(self, context):
        if len(self.params) == 2:
            context.add_for_each(self.params[0], self.params[1])
        elif len(self.params) == 3:
            context.add_for_loop(self.params[0], self.params[1], self.params[2])

    def validate_params(self, context):
        if len(self.params) == 3:
            return True

        var_data = context.get_variable_data(self.params[1])

        if var_data is None:
            return False

        var_type = var_data['type']
        if '[' not in var_type:
            print('Not an array')
            return False

        var_type = var_type[:var_type.index('[')]
        self.params[0] = f'{var_type} {self.params[0]}'
        return True

    def _valid_params(self, context, params):
        try:
            in_idx = params.index('in')
        except ValueError:
            return []

        try:
            range_idx = params.index('range')
            return self._handle_for_range(params, in_idx, range_idx)
        except ValueError:
            return self._handle_for_each(params, in_idx)

    def _handle_for_range(self, params, in_idx, range_idx):
        try:
            to_idx = params.index('to')
        except ValueError:
            return []

        for_var = ''
        for param in params[:in_idx]:
            if param == 'every':
                continue

            for_var += param.strip()

        if for_var == '':
            return []

        for_range_start = ''
        for param in params[range_idx+1:to_idx]:
            for_range_start += param.strip()

        if for_range_start == '':
            return []

        for_range_end = ''
        for param in params[to_idx+1:]:
            for_range_end += param.strip()

        if for_range_end == '':
            return []

        return [for_var, for_range_start, for_range_end]

    def _handle_for_each(self, params, in_idx):
        for_var = ''
        for param in params[:in_idx]:
            if param == 'every':
                continue

            for_var += param.strip()

        if for_var == '':
            return []

        for_end_var = ''
        for param in params[in_idx + 1:]:
            for_end_var += param.strip()

        if for_end_var == '':
            return []

        return [for_var, for_end_var]

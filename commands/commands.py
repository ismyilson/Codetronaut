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
            self.last_error_message = f'Editor {self.params[0]} is not recognized'
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
            reader.read_text(f'No directory set')
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
            self.last_error_message = f'Invalid param structure, use: "variable name", "to", "variable value"'
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

        self.last_error_message = f'Cant find file {file_name}'
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
            self.last_error_message = f'File {self.params[0]} already exists'
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

    def validate_params(self, context):
        # Need to check if class exists here
        return True

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
            self.last_error_message = 'Method name required'
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
        if int(self.params[0]) > context.get_current_file_line_count():
            self.last_error_message = f'Invalid line'
            return False

        return True

    def _valid_params(self, context, params):
        num_str = ''
        for param in params:
            param = param.replace(',', '').replace('-', '')
            if not param.isnumeric():
                break

            num_str += param

        if num_str == '':
            self.last_error_message = f'Must specify a line'
            return []

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

    _connectors = ['to', 'through']

    def execute(self, context):
        line_start = self.params[0] if len(self.params) > 0 else None
        line_end = self.params[1] if len(self.params) > 1 else None

        context.delete_lines(line_start, line_end)

    def validate_params(self, context):
        line_count = context.get_current_file_line_count()
        if len(self.params) == 0:
            return True
        elif len(self.params) == 1:
            if self.params[0] > line_count:
                self.last_error_message = f'Line doesnt exist'
                return False
        else:
            if self.params[0] > self.params[1]:
                tmp = self.params[0]
                self.params[0] = self.params[1]
                self.params[1] = tmp

            if self.params[1] > line_count:
                self.last_error_message = f'Line doesnt exist'
                return False

        return True

    def _valid_params(self, context, params):
        if len(params) == 1:
            return [int(params[0])]

        idx = self._find_idx(params)
        if idx == -1:
            self.last_error_message = f'Invalid param structure. Use example: Line 10 to 15'
            return []

        line_start = ''.join([param for param in params[:idx] if param.isnumeric()])
        line_end = ''.join([param for param in params[idx+1:] if param.isnumeric()])

        if line_start == '':
            self.last_error_message = f'Invalid param structure, must specify a starting line'
            return []

        if line_end == '':
            self.last_error_message = f'Invalid param structure, must specify an ending line'
            return []

        return [int(line_start), int(line_end)]

    def _find_idx(self, params):
        for connector in self._connectors:
            try:
                return params.index(connector)
            except ValueError:
                continue

        return -1


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
        var_data = context.get_variable_data(self.params[0])

        if var_data is None:
            self.last_error_message = f'Variable {self.params[0]} does not exist'
            return False

        return True

    def _valid_params(self, context, params):
        try:
            to_idx = last_index_of_list(params, 'to')
        except IndexError:
            return []

        var_name = ''.join(params[:to_idx])
        new_var_name = ''.join(params[to_idx+1:])

        if var_name == '':
            self.last_error_message = f'Invalid param structure, specify a variable name'
            return []

        if new_var_name == '':
            self.last_error_message = f'Invalid param structure, specify a new variable name'
            return []

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

    _operations = {
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

    def execute(self, context):
        context.add_if_condition(self.params[0], self.params[1], self.params[2])

    def _valid_params(self, context, params):
        valid_params = self._parse_if_condition(params)

        if len(valid_params) < 1:
            self.last_error_message = 'Invalid param structure, specify the condition'
            return []

        return valid_params

    def _parse_if_condition(self, params):
        complete_sentence = ' '.join(params)

        idx_start = -1
        idx_end = -1
        operation = None
        for special in self._operations.keys():
            if special in complete_sentence:
                idx_start = complete_sentence.index(special)
                idx_end = idx_start + len(special) + 1
                operation = special
                break

        if idx_start == -1:
            return []

        operation = self._operations.get(operation)

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

    _operations = {
        'plus': '+',
        'minus': '-',
        'multiplied by': '*',
        'divided by': '/'
    }

    def execute(self, context):
        context.add_return(self.params)

    def _valid_params(self, context, params):
        complete_sentence = ' '.join(params)

        operation = None
        idx_start = -1
        idx_end = -1
        for special in self._operations.keys():
            if special in complete_sentence:
                idx_start = complete_sentence.index(special)
                idx_end = idx_start + len(special) + 1
                operation = special
                break

        # Single variable
        if idx_start == -1:
            var_name = ''.join(params)
            if var_name == '':
                self.last_error_message = 'Invalid param structure, specify what to return'
                return []

            return [var_name]

        operation = self._operations.get(operation)

        first_param = complete_sentence[:idx_start].replace(' ', '')
        second_param = complete_sentence[idx_end:].replace(' ', '')

        return [first_param, operation, second_param]


class SubcommandSelectLine(SubCommand):
    cmd = ['line']

    requires_params = False

    def execute(self, context):
        line = self.params[0] if len(self.params) > 0 else None

        context.select_line(line)

    def validate_params(self, context):
        if len(self.params) < 1:
            return True

        line = int(self.params[0])
        if line > context.get_current_file_line_count():
            self.last_error_message = 'Invalid line'
            return False

        return True

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
            self.last_error_message = f'Method {self.params[0]} not found'
            return False

        # Should maybe check variable exists here

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
            self.last_error_message = 'Invalid param structure, specify a method name'
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

        if method_data is None:
            self.last_error_message = f'Method {self.params[0]} does not exist'
            return False

        return True

    def _valid_params(self, context, params):
        try:
            to_idx = last_index_of_list(params, 'to')
        except IndexError:
            self.last_error_message = f'Invalid param structure. Use example: Add String parameter name to setName'
            return []

        var_name = ''.join(params[:to_idx])
        method_name = ''.join(params[to_idx+1:])

        if var_name == '':
            self.last_error_message = 'Invalid param structure, specify the name of the parameter'
            return []

        if method_name == '':
            self.last_error_message = 'Invalid param structure, specify the name of the method'
            return []

        return [method_name, var_name]

    def _valid_modifiers(self, context, modifiers):
        var_type = ''.join([mod.title() for mod in modifiers])

        # This needs to change to context.get_programming_language_variable_types() or something like that
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

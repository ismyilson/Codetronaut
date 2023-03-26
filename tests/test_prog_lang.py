from prog_langs.base_prog_lang import BaseProgrammingLanguage


class _TestProgLang(BaseProgrammingLanguage):
    pass


def test_get_variable_data_simple():
    prog_lang = _TestProgLang()

    text = ['int Name;']
    var_data = prog_lang.find_variable(text, 'name')
    assert var_data['name'] == 'Name'
    assert var_data['type'] == 'int'
    assert var_data['value'] is None
    assert var_data['static'] is False
    assert var_data['access_type'] == 'private'

    text = ['String[] strings;']
    var_data = prog_lang.find_variable(text, 'strings')
    assert var_data['name'] == 'strings'
    assert var_data['type'] == 'String[]'
    assert var_data['value'] is None
    assert var_data['static'] is False
    assert var_data['access_type'] == 'private'

    text = ['var_NAME = 10']
    var_data = prog_lang.find_variable(text, 'var_name')
    assert var_data['name'] == 'var_NAME'
    assert var_data['type'] is None
    assert var_data['value'] == '10'
    assert var_data['static'] is False
    assert var_data['access_type'] == 'private'


def test_get_variable_data_with_static():
    prog_lang = _TestProgLang()

    text = ['static int Name;']
    var_data = prog_lang.find_variable(text, 'name')
    assert var_data['name'] == 'Name'
    assert var_data['type'] == 'int'
    assert var_data['value'] is None
    assert var_data['static'] is True
    assert var_data['access_type'] == 'private'
    assert var_data['line_index'] == 1
    assert var_data['var_index'] == 11


def test_get_variable_data_with_value():
    prog_lang = _TestProgLang()

    text = ['int Name = 10;']
    var_data = prog_lang.find_variable(text, 'name')
    assert var_data['name'] == 'Name'
    assert var_data['type'] == 'int'
    assert var_data['value'] == '10'
    assert var_data['static'] is False
    assert var_data['access_type'] == 'private'
    assert var_data['line_index'] == 1
    assert var_data['var_index'] == 4


def test_get_variable_data_with_access_type():
    prog_lang = _TestProgLang()

    text = ['protected int Name;']
    var_data = prog_lang.find_variable(text, 'name')
    assert var_data['name'] == 'Name'
    assert var_data['type'] == 'int'
    assert var_data['value'] is None
    assert var_data['static'] is False
    assert var_data['access_type'] == 'protected'
    assert var_data['line_index'] == 1
    assert var_data['var_index'] == 14


def test_get_method_data_simple():
    prog_lang = _TestProgLang()

    text = ['void doStuff() {']
    method_data = prog_lang.get_method_data(text, 'dostuff')
    assert method_data['name'] == 'doStuff'
    assert method_data['type'] == 'void'
    assert method_data['params'] == []
    assert method_data['static'] is False
    assert method_data['access_type'] == 'private'
    assert method_data['line_index'] == 1
    assert method_data['method_index'] == 5
    assert method_data['params_end_index'] == 13


def test_get_method_data_with_static():
    prog_lang = _TestProgLang()

    text = ['static void doStuff() {']
    method_data = prog_lang.get_method_data(text, 'dostuff')
    assert method_data['name'] == 'doStuff'
    assert method_data['type'] == 'void'
    assert method_data['params'] == []
    assert method_data['static'] is True
    assert method_data['access_type'] == 'private'
    assert method_data['line_index'] == 1
    assert method_data['method_index'] == 12
    assert method_data['params_end_index'] == 20


def test_get_method_data_with_params():
    prog_lang = _TestProgLang()

    text = ['void doStuff(int value) {']
    method_data = prog_lang.get_method_data(text, 'dostuff')
    assert method_data['name'] == 'doStuff'
    assert method_data['type'] == 'void'
    assert method_data['params'] == ['int value']
    assert method_data['static'] is False
    assert method_data['access_type'] == 'private'
    assert method_data['line_index'] == 1
    assert method_data['method_index'] == 5
    assert method_data['params_end_index'] == 22

    text = ['void doStuff(int value, String otherValue) {']
    method_data = prog_lang.get_method_data(text, 'dostuff')
    assert method_data['name'] == 'doStuff'
    assert method_data['type'] == 'void'
    assert method_data['params'] == ['int value', 'String otherValue']
    assert method_data['static'] is False
    assert method_data['access_type'] == 'private'
    assert method_data['line_index'] == 1
    assert method_data['method_index'] == 5
    assert method_data['params_end_index'] == 41

    text = ['void doStuff(int value, String otherValue,String other2) {']
    method_data = prog_lang.get_method_data(text, 'dostuff')
    assert method_data['name'] == 'doStuff'
    assert method_data['type'] == 'void'
    assert method_data['params'] == ['int value', 'String otherValue', 'String other2']
    assert method_data['static'] is False
    assert method_data['access_type'] == 'private'
    assert method_data['line_index'] == 1
    assert method_data['method_index'] == 5
    assert method_data['params_end_index'] == 55


def test_get_method_data_with_access_type():
    prog_lang = _TestProgLang()

    text = ['protected static void doStuff() {']
    method_data = prog_lang.get_method_data(text, 'dostuff')
    assert method_data['name'] == 'doStuff'
    assert method_data['type'] == 'void'
    assert method_data['params'] == []
    assert method_data['static'] is True
    assert method_data['access_type'] == 'protected'
    assert method_data['line_index'] == 1
    assert method_data['method_index'] == 22
    assert method_data['params_end_index'] == 30

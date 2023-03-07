import winapps
import psutil
from audio import reader
import os


def run(name, exe_name, **kwargs):
    apps = winapps.search_installed(name)
    app_location = ''
    for app in apps:
        app_location = get_path_to_file(app.install_location, exe_name)

        if app_location != '':
            break

    if app_location == '':
        reader.read_text(f'Could not find installation of {name}')
        return None

    return psutil.Popen([app_location, '-a', kwargs['workdir']])


def close_process(pid):
    p = psutil.Process(pid)
    p.kill()


def process_is_running(exe_name):
    return exe_name.lower() in [p.name().lower() for p in psutil.process_iter()]


def create_file(path):
    f = open(path, 'x')
    f.close()


def get_path_to_file(path, file_name, recursive=True):
    if recursive:
        return _get_path_to_file_recursive(path, file_name)
    else:
        return _get_path_to_file(path, file_name)


def _get_path_to_file(path, file_name):
    for file in os.listdir(path):
        if file == file_name:
            return os.path.join(path, file_name)

    return ''


def _get_path_to_file_recursive(path, file_name):
    for root, dirs, files in os.walk(path):
        if file_name in files:
            return os.path.join(root, file_name)

    return ''

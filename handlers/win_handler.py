import winapps
import psutil
import reader
import os


def run(name, exe_name, **kwargs):
    apps = winapps.search_installed(name)
    app_location = ''
    for app in apps:
        app_location = get_relative_path(app.install_location, exe_name)

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


def get_relative_path(path, file_name):
    for root, dirs, files in os.walk(path):
        if file_name in files:
            return os.path.join(root, file_name)

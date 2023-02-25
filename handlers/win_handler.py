import subprocess
import psutil


def open_process(process_name, **kwargs):
    return subprocess.run([process_name, '-a', kwargs['workdir']], shell=True)


def process_is_running(process_name):
    return process_name in [p.name() for p in psutil.process_iter()]

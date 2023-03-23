import win32con
import win32gui
import win32process
import winapps

from platforms.base_platform import BasePlatform
from utils import get_classes_in_module


def get_platforms():
    return get_classes_in_module(__name__, subclass_of=BasePlatform)


class PlatformWindows(BasePlatform):
    identifier = 'Windows'
    name = 'Windows'

    def get_install_path(self, name):
        apps = winapps.search_installed(name)

        for app in apps:
            return app.install_location

        return None

    def focus(self, pid):
        hwnds = self._get_hwnds_for_pid(pid)

        if len(hwnds) < 1:
            return

        win32gui.SetForegroundWindow(hwnds[0])

    def _get_hwnds_for_pid(self, pid):
        def callback(hwnd, hwnds):
            if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
                _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
                if found_pid == pid:
                    hwnds.append(hwnd)
            return True

        hwnds = []
        win32gui.EnumWindows(callback, hwnds)
        return hwnds

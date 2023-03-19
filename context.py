import platform

from editors.base_editor import BaseEditor

from platforms.base_platform import BasePlatform, UnsupportedPlatform
from platforms.platforms import PLATFORMS

from prog_langs.base_prog_lang import BaseProgrammingLanguage


class Context:
    platform: BasePlatform
    editor: BaseEditor
    prog_lang: BaseProgrammingLanguage

    def __init__(self):
        self._setup_platform()

    def _setup_platform(self):
        os_name = platform.system()

        platform_class = PLATFORMS.get(os_name, None)
        if platform_class is None:
            raise UnsupportedPlatform(f'{os_name} is not a supported platform')

        self.platform = platform_class()

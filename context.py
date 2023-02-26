import reader

from handlers.file_handler import write_to_file, load_file
from os import path


CONTEXT_SAVE_PATH = path.expandvars(r'%LOCALAPPDATA%\Voice2Code\context')


class Context:
    workdir: str
    editor: None

    current_directory: str

    def __init__(self):
        self.load_context()

    def save_context(self):
        config = self._get_config()

        write_to_file(CONTEXT_SAVE_PATH, config)

    def load_context(self):
        try:
            config = load_file(CONTEXT_SAVE_PATH)

            for k, v in config.items():
                setattr(self, k, v)
        except FileNotFoundError:
            self._load_defaults()

        self.read_config()

    def _load_defaults(self):
        self.workdir = ''
        self.editor = None

        self.current_directory = ''

    def read_config(self):
        if self.workdir != '':
            reader.read_text(f'Directory set to: {self.get_directory()}')

        if self.editor is not None:
            reader.read_text(f'Editor set to: {self.editor.editor_name}')

            if not self.editor.is_running():
                self.editor.run(self.workdir)

    def get_directory(self):
        idx = self.workdir.rfind('/')
        return self.workdir[idx + 1:] if idx != -1 else self.workdir

    def clean_up(self):
        self.editor.close()

        self.save_context()

    def _get_config(self):
        return {
            'workdir': self.workdir,
            'editor': self.editor,
            'current_directory': self.current_directory
        }


CurrentContext = Context()


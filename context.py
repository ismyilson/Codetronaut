import reader
from handlers.file_handler import write_to_file, load_file
from os import path


CONTEXT_SAVE_PATH = path.expandvars(r'%LOCALAPPDATA%\Voice2Code\context')


class Context:
    directory: str
    editor: str

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

    def _load_defaults(self):
        self.directory = ''
        self.editor = ''

    def read_config(self):
        reader.read_text(f'Directory set to: {self.get_directory()}')
        reader.read_text(f'Editor set to: {self.editor}')

    def get_directory(self):
        idx = self.directory.rfind('/')
        return self.directory[idx + 1:] if idx != -1 else self.directory

    def _get_config(self):
        return {
            'directory': self.directory,
            'editor': self.editor
        }


CurrentContext = Context()


import reader

from handlers.file_handler import write_to_file, load_file
from os import path


CONTEXT_SAVE_PATH = path.expandvars(r'%LOCALAPPDATA%\Voice2Code\context')


class Context:
    directory: str
    editor: None

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
        self.directory = ''
        self.editor = None

    def read_config(self):
        if self.directory != '':
            reader.read_text(f'Directory set to: {self.get_directory()}')

        if self.editor is not None:
            reader.read_text(f'Editor set to: {self.editor.editor_name}')

            if not self.editor.is_running():
                self.editor.run(self.directory)

    def get_directory(self):
        idx = self.directory.rfind('/')
        return self.directory[idx + 1:] if idx != -1 else self.directory

    def clean_up(self):
        self.editor.close()

        self.save_context()

    def _get_config(self):
        return {
            'directory': self.directory,
            'editor': self.editor
        }


CurrentContext = Context()


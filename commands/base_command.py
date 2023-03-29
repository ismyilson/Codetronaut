import abc


class BaseCommand(abc.ABC):
    cmd: list[str] = []

    requires_modifiers: bool = False
    modifiers: list[str] = []

    requires_params: bool = False
    params: list[str] = []

    last_error_message: str = None

    def execute(self, context):
        pass

    def set_modifiers(self, context, modifiers):
        if len(modifiers) < 1:
            return False

        valid_modifiers = self._valid_modifiers(context, modifiers)

        if len(valid_modifiers) < 1:
            return False

        self.modifiers = valid_modifiers
        return True

    def _valid_modifiers(self, context, modifiers):
        return []

    def validate_params(self, context):
        return True

    def set_params(self, context, params):
        valid_params = self._valid_params(context, params)

        if len(valid_params) < 1:
            return False

        self.params = valid_params
        return True

    def _valid_params(self, context, params):
        return []


class SubCommand(BaseCommand):
    pass


class MainCommand(BaseCommand):
    requires_subcommand: bool = False
    default_subcommand: SubCommand = None

    subcommands: list[SubCommand] = []

    @property
    def is_no_params_only(self):
        return not self.requires_subcommand and\
            len(self.subcommands) < 1 and\
            not self.requires_params

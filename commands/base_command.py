import abc


class BaseCommand(abc.ABC):
    cmd: list[str] = []

    def execute(self, context):
        raise NotImplementedError('BaseCommand does not have an implementation for `execute`')


class MainCommand(BaseCommand):
    requires_subcommand: bool = False

    subcommands: list = []

    def execute(self, context):
        raise NotImplementedError('MainCommand does not have an implementation for `execute`')

    @property
    def is_no_params_only(self):
        return not self.requires_subcommand and len(self.subcommands) < 1


class SubCommand(BaseCommand):
    def execute(self, context):
        raise NotImplementedError('SubCommand does not have an implementation for `execute`')

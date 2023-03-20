import abc


class BaseProgrammingLanguage(abc.ABC):
    identifiers: list[str]
    name: str

    extensions: list[str]

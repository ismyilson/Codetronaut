import abc
import sys


class UnsupportedPlatform(Exception):
    def __init__(self, message):
        super().__init__(message)


class BasePlatform(abc.ABC):
    pass

from abc import ABCMeta, abstractmethod


class BaseCommandManager(metaclass=ABCMeta):

    @abstractmethod
    def get_command(self, command_number):
        ...

    @abstractmethod
    def add_command(self, command_number, command_class):
        ...

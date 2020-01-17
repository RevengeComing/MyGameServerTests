from .base import BaseCommandManager

from server.command.base import BaseCommand


class InMemoryCommandManager(BaseCommandManager):
    def __init__(self):
        self.commands = {}

    def add_command(self, command_number, command_class):
        self.commands[command_number] = command_class

    def get_command(self, command_number) -> BaseCommand:
        return self.commands[command_number]

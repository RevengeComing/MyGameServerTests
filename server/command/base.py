import ujson

from abc import ABCMeta, abstractmethod


class BaseCommand(metaclass=ABCMeta):

    def __init__(self, data, client_data):
        self.data = self.parse(data)

    def parse(self, data):
        return ujson.loads(data)

    @abstractmethod
    def process(self):
        ...

    def update_client_data(self):
        pass

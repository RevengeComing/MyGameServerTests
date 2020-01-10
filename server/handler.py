import asyncio

from .command.manager.base import BaseCommandManager

clients = []


class ClientHandlerFactory():
    def __init__(self, command_manager, game_world):
        self.command_manager = command_manager
        self.game_world = game_world

    async def __call__(self, reader, writer):
        print("New connection")
        ch = ClientHandler(reader, writer, self.command_manager, self.game_world)
        asyncio.ensure_future(ch.send_updates())
        asyncio.ensure_future(ch.handle_packets())


class ClientHandler():
    def __init__(self, reader, writer, command_manager, game_world):
        self.reader = reader
        self.writer = writer

        self.data = {}

        self.world = game_world

        self.command_manager: BaseCommandManager = command_manager

    async def handle_packets(self):
        while self.writer and (not self.writer.is_closing() or not self.writer.close()):
            command_number = await self.reader.read(4)
            data_length = await self.reader.read(4)
            try:
                data = await self.reader.read(int(data_length))
                command_class = self.command_manager.get_command(command_number)
                command = command_class(data)
                command.process()
                self.data.update(command.update_player())
                self.world.update_data(command.update_world())
            except Exception:
                if not self.writer.close():
                    self.writer.write(b"ERROR")
                    try:
                        await self.writer.drain()
                    except ConnectionResetError:
                        self.writer.close()
                        self.writer = None

    async def send_updates(self):
        while self.writer and (not self.writer.is_closing() or not self.writer.close()):
            self.writer.write(b"asdqwe")
            try:
                await self.writer.drain()
            except ConnectionResetError:
                self.writer.close()
                self.writer = None
            await asyncio.sleep(0.07)

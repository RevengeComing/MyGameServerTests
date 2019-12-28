import asyncio

from .command import commands


clients = []


async def handle_new_connection(reader, writer):
    ch = ClientHandler(reader, writer)
    asyncio.ensure_future(ch.send_updates())
    asyncio.ensure_future(ch.handle_packets())


class ClientHandler():
    def __init__(self, reader, writer):
        self.reader = reader
        self.writer = writer

        self.is_connected = True

    async def handle_packets(self):
        while self.is_connected:
            command_number = await self.reader.read(4)
            data_length = await self.reader.read(4)
            data = await self.reader.read(int(data_length))
            command = commands[command_number]
            command(data).process()

    async def send_updates(self):
        while self.is_connected:
            self.writer.write(b"asdqwe")
            await self.writer.drain()
            await asyncio.sleep(0.07)

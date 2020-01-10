import asyncio
import pygame
from functools import partial

from server.handler import ClientHandlerFactory

from server.command.commands.auth import Authenticate
from server.command.manager.in_memory import InMemoryCommandManager
from server.game.world import GameWorld


def main():
    pygame.init()
    print("Pygame init done")

    command_manager = InMemoryCommandManager()
    command_manager.add_command(1, Authenticate)

    game_world = GameWorld()

    loop = asyncio.get_event_loop()
    coro = asyncio.start_server(ClientHandlerFactory(command_manager, game_world), '0.0.0.0', 8888, loop=loop)

    server = loop.run_until_complete(coro)

    future = asyncio.Future()
    loop.run_until_complete(game_world.update())

    print('Serving on {}'.format(server.sockets[0].getsockname()))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    # Close the server
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


if __name__ == "__main__":
    main()

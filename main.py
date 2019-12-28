import asyncio
import pygame

from server.handler import handle_new_connection



def main():
    pygame.init()
    
    loop = asyncio.get_event_loop()
    coro = asyncio.start_server(handle_new_connection, '0.0.0.0', 8888, loop=loop)
    server = loop.run_until_complete(coro)

    print('Serving on {}'.format(server.sockets[0].getsockname()))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    # Close the server
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()
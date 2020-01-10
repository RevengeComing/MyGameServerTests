import asyncio


class GameWorld:
    def __init__(self):
        self.data = {}
        self.is_active = True

    def update_data(self, data: dict):
        self.data.update(data)

    async def update(self, clock=0.0166):
        while self.is_active:
            await asyncio.sleep(clock)

    def shut_down(self):
        self.is_active = False

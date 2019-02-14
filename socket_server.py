import os
import asyncio
import json
import logging
import websockets
import random
from threading import Thread


class SocketServer:

    logging.basicConfig()
    users = set()

    def __init__(self, state, count):
        self.state = state
        self.count = count

        config = json.loads(open("config.json").read())

        print("Hello (⌐■_■)")
        print("Welcome to your socket server!")
        print(
            "We're currently running a good service @ %s:%s"
            % (config["ip_address"], config["port"])
        )

        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(
            websockets.serve(self.counter, config["ip_address"], config["port"])
        )

        if os.name == "nt":
            self.loop.create_task(self.interrupt())

        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            print("Goodbye ʕ·͡ᴥ·ʔ")
            pass

    def state_event(self):
        return json.dumps(
            {"type": "state", "state": self.state, "count": self.count[0]}
        )

    async def notify_state(self):
        if self.users:  # asyncio.wait doesn't accept an empty list
            message = self.state_event()
            await asyncio.wait([user.send(message) for user in self.users])

    async def register(self, websocket):
        self.users.add(websocket)

    async def unregister(self, websocket):
        self.users.remove(websocket)

    async def counter(self, websocket, path):
        # register(websocket) sends user_event() to websocket
        await self.register(websocket)
        try:
            dummy_state = self.state.copy()
            while True:

                if dummy_state != self.state:
                    dummy_state = self.state.copy()
                    await websocket.send(self.state_event())

                await asyncio.sleep(random.random())
        finally:
            await self.unregister(websocket)

    async def interrupt(self):
        while True:
            await asyncio.sleep(1)


if __name__ == "__main__":
    print("You're running solo. This is intended to be ran as part of a package.")
    main = SocketServer([True, False, True, False, True], 0)

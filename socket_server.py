#!/usr/bin/env python

# WS server example that synchronizes state across clients

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
            % (config["ip_address"], config["port"]))

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(websockets.serve(
            self.counter, config["ip_address"], config["port"]))

        if os.name == "nt":
            loop.create_task(self.interrupt())

        try:
            loop.run_forever()
        except KeyboardInterrupt:
            print("Goodbye ʕ·͡ᴥ·ʔ")
            pass

    def state_event(self):
        return json.dumps({"type":"state", "state": self.state, "count": self.count})

    def users_event(self):
        return json.dumps({"type":"users", "count": len(self.users)})

    async def notify_state(self):
        if self.users:  # asyncio.wait doesn't accept an empty list
            message = self.state_event()
            await asyncio.wait([user.send(message) for user in self.users])

    async def notify_users(self):
        if self.users:  # asyncio.wait doesn't accept an empty list
            message = self.users_event()
            await asyncio.wait([user.send(message) for user in self.users])

    async def register(self, websocket):
        self.users.add(websocket)
        await self.notify_users()

    async def unregister(self, websocket):
        self.users.remove(websocket)
        await self.notify_users()

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

    def clear(self, collection):
        for item in collection:
            if isinstance(collection[item], dict):
                for direction in collection[item]:
                    collection[item][direction] = 0
            else:
                collection[item] = 0

    def update_state(self, data):
        camera_id = list(data.keys())[0]
        self.state[camera_id] = data[camera_id]

    def update_total(self):
        # tally totals
        down_total = 0
        up_total = 0
        for camera in STATE:
            if isinstance(STATE[camera], dict):
                down_total += STATE[camera]["down"]
                up_total += STATE[camera]["up"]

        # calculate current "inside"
        insiders = up_total - down_total
        # if insiders < 0:
        #    insiders = 0
        return insiders

    async def interrupt(self):
        while True:
            await asyncio.sleep(1)


if __name__ == "__main__":
    state = [True, False, True, False, True]
    count = 0
    main = SocketServer(state, count)


"""def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(websockets.serve(counter, 'localhost', 6789))
    loop.run_forever()

new_loop = asyncio.new_event_loop()
t = Thread(target=start_loop, args=(new_loop,))
t.start()"""

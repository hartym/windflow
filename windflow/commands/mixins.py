import asyncio

import uvloop
from tornado.platform.asyncio import AsyncIOMainLoop


class EventLoopCommandMixin():
    def get_event_loop(self, debug=False):
        if not debug:
            asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
            asyncio.set_event_loop(uvloop.new_event_loop())
        AsyncIOMainLoop().install()
        return asyncio.get_event_loop()
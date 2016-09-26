import asyncio

import uvloop
from tornado.platform.asyncio import AsyncIOMainLoop


class ServerCommand:
    name = 'server'

    def __init__(self, app_factory, host='0.0.0.0', port=8081, **kwargs):
        self.app_factory = app_factory
        self.host = host
        self.port = port
        self.kwargs = kwargs

    def register_commands(self, subparsers):
        server = subparsers.add_parser(self.name)
        server.set_defaults(handler=self.handle)

    def get_event_loop(self, debug=False):
        if not debug:
            asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
            asyncio.set_event_loop(uvloop.new_event_loop())
        AsyncIOMainLoop().install()
        return asyncio.get_event_loop()

    def handle(self, logger, options):
        self.kwargs['debug'] = bool(self.kwargs.pop('debug', False))
        loop = self.get_event_loop(self.kwargs['debug'])

        self.app_factory(**self.kwargs).listen(self.port, self.host)
        logger.info('Listening to {}:{} - {}'.format(self.host, self.port, self.kwargs))
        loop.run_forever()

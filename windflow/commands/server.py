from windflow.commands.base import Command
from windflow.commands.mixins import EventLoopCommandMixin


class ServerCommand(EventLoopCommandMixin, Command):
    name = 'server'

    def __init__(self, app_factory, host='0.0.0.0', port=8081, **kwargs):
        self.app_factory = app_factory
        self.host = host
        self.port = port
        self.kwargs = kwargs

    def handle(self, logger, options):
        self.kwargs['debug'] = bool(self.kwargs.pop('debug', False))
        loop = self.get_event_loop(self.kwargs['debug'])

        self.app_factory(**self.kwargs).listen(self.port, self.host)
        logger.info('Listening to {}:{} - {}'.format(self.host, self.port, self.kwargs))
        loop.run_forever()

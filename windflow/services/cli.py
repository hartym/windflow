import argparse
import logging

from tornado.log import enable_pretty_logging
from windflow.services import Service


class CommandLine(Service):
    """
    Command line interface service.

    """

    def __init__(self, default_handler=None):
        self.default_handler = default_handler

        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('--debug', '-d', action='store_true', help='enable debugging features')
        self.parser.add_argument('--verbose', '-v', action='count', help='increase output verbosity')

        self.subparsers = self.parser.add_subparsers(dest='handler')
        self.subparsers.required = not callable(default_handler)

    def register(self, service, method='register_commands'):
        return getattr(service, method)(self.subparsers)

    def parse(self, args=None, namespace=None):
        return self.parser.parse_args(args, namespace)

    def run(self, args=None, namespace=None):
        options = self.parser.parse_args(args=args, namespace=namespace)
        enable_pretty_logging()
        logger = logging.getLogger(__name__)

        # todo configure_logger() method ?
        if options.debug:
            logging.getLogger('root').setLevel(logging.INFO)
        if options.verbose:
            if options.verbose >= 1:
                logging.getLogger('root').setLevel(logging.DEBUG)
            if options.verbose >= 2:
                logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO if options.verbose < 2 else logging.DEBUG)

        try:
            handler = options.handler
        except AttributeError as e:
            if not callable(self.default_handler):
                raise
            handler = None

        return (handler or self.default_handler)(logger, options)

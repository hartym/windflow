import argparse
import logging

from tornado.log import enable_pretty_logging
from windflow.services import Service


class CommandLine(Service):
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('--verbose', '-v', action='store_const', const=logging.DEBUG, default=logging.INFO)
        self.subparsers = self.parser.add_subparsers(dest='handler')
        self.subparsers.required = False

    def register(self, service, method='register_commands'):
        return getattr(service, method)(self.subparsers)

    def parse(self, args=None, namespace=None):
        options = self.parser.parse_args(args, namespace)
        logger = logging.getLogger(__name__)
        enable_pretty_logging()
        return options, logger

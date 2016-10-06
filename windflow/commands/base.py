class Command:
    name = None

    def register_commands(self, subparsers):
        """
        :param subparsers:
        :return parser:
        """
        if not self.name:
            raise NotImplementedError('You must define a name attribute in your command class.')

        parser = subparsers.add_parser(self.name)
        parser.set_defaults(handler=self.handle)

        return parser

    def handle(self, logger, options):
        raise NotImplementedError('You must implement the handle() method in your command class.')

import tornado.web
import os.path


class ApplicationFactory:
    def __init__(self, factory=tornado.web.Application):
        self.factory = factory
        self.mounts = []
        self.configured = False

    def configure(self, configurator=None):
        self.configured = True
        configured = None
        if configurator:
            configured = configurator(self) or configured
        return configured or self

    def mount(self, prefix, config):
        self.mounts.append((prefix, config))

    def __call__(self, *args, **kwargs):
        if not self.configured:
            return self.configure(*args, **kwargs)

        app = self.factory(*args, **kwargs)

        for prefix, config in self.mounts:
            app.add_handlers('.*$', [
                (os.path.join(prefix, handler[0].lstrip('/')), *handler[1:]) for handler in config.get_handlers()
                ])

        return app

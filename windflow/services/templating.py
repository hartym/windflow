import simplejson
from jinja2 import Environment, FileSystemLoader
from windflow.services.base import Service


class Templating(Service):
    """
    Jinja2 templating service.

    """

    name = 'templating'

    @property
    def loader(self):
        return FileSystemLoader('templates')

    def __init__(self):
        self.env = Environment(loader=self.loader)
        self.env.filters['json'] = simplejson.dumps

    def render(self, name, *args, **kwargs):
        return self.env.get_template(name).render(*args, **kwargs)

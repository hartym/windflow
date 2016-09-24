import simplejson
from windflow.services import Service


class WebpackAssets(Service):
    filename = 'static/assets.json'

    def get(self):
        try:
            with open(self.filename) as f:
                return simplejson.load(f)
        except:
            # todo this is evil, but we'd need to find out errors e do want to "ignore" or how to tell user about it.
            # at the very minimum: simplejson.scanner.JSONDecodeError and probably missing file
            return {}

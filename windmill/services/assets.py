import simplejson
from windmill.services import Service


class WebpackAssets(Service):
    filename = 'static/assets.json'

    def get(self):
        with open(self.filename) as f:
            return simplejson.load(f)


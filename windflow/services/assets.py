import json
import os

from windflow.services import Service


class Assets(dict):
    def __init__(self, path, iterable=None, **kwargs):
        super().__init__(iterable or (), **kwargs)
        self._path = path

    def get_style(self, name):
        try:
            bundle = self[name]
        except KeyError as e:
            return ''

        try:
            return '<link href="' + os.path.join(self._path, bundle['css']) + '" rel="stylesheet">'
        except KeyError as e:
            return ''

    def get_script(self, name):
        try:
            bundle = self[name]
        except KeyError as e:
            return ''

        try:
            return '<script src="' + os.path.join(self._path, bundle['js']) + '" type="text/javascript"></script>'
        except KeyError as e:
            return ''


class UnavailableAssets(Assets):
    def get_style(self, name):
        return ''

    def get_script(self, name):
        return ('<script type="text/javascript">document.write("Assets are not available. It may means that the '
                'bundling process is still running, or that the webpack AssetsPlugin did not run. Look for the '
                'assets.json file in your static directory (and look at webpack output).")</script>')


class WebpackAssets(Service):
    """
    Webpack assets service.

    Simply reads the output of the assets plugin (json) so it can be used in a templating context.

    """

    filename = 'static/assets.json'
    path = '/'

    assets_type = Assets
    unavailable_assets_type = UnavailableAssets

    def get(self):
        try:
            with open(self.filename) as f:
                return self.assets_type(self.path, json.load(f))
        except:
            # todo this is evil, but we'd need to find out errors e do want to "ignore" or how to tell user about it.
            # at the very minimum: simplejson.scanner.JSONDecodeError and probably missing file
            return self.unavailable_assets_type(self.path)

import simplejson
from windflow.services import Service


class Assets(dict):
    def get_style(self, name):
        bundle = self[name]
        if 'css' in bundle:
            return '<link href="' + bundle['css'] + '" rel="stylesheet">'
        return ''

    def get_script(self, name):
        bundle = self[name]
        if 'js' in bundle:
            return '<script src="' + bundle['js'] + '" type="text/javascript"></script>'
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

    def get(self):
        try:
            with open(self.filename) as f:
                return Assets(simplejson.load(f))
        except:
            # todo this is evil, but we'd need to find out errors e do want to "ignore" or how to tell user about it.
            # at the very minimum: simplejson.scanner.JSONDecodeError and probably missing file
            return UnavailableAssets()

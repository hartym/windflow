def create_url_for_helper(name, *parts, **defaults):
    def url_for_helper(self, *args, absolute=False, **kwargs):
        params = dict(defaults)
        params.update(kwargs)
        _parts = params.pop('parts', {})
        _parts.update(dict(zip(parts, map(str, args))))
        if _parts:
            params['parts'] = _parts
        url = self.request.app.router[name].url(**params)
        return self.make_url_absolute(url) if absolute else url

    url_for_helper.__name__ = 'url_for_' + name
    return url_for_helper

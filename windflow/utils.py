def absolute_url(request, path):
    """
    :param HTTPServerRequest request:
    :param str path:

    :return str:
    """
    return request.protocol + "://" + request.host + path

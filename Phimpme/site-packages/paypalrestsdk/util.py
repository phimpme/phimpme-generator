import re

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode


def join_url(url, *paths):
    """
    Joins individual URL strings together, and returns a single string.

    Usage::

        >>> util.join_url("example.com", "index.html")
        'example.com/index.html'
    """
    for path in paths:
        url = re.sub(r'/?$', re.sub(r'^/?', '/', path), url)
    return url


def join_url_params(url, params):
    """Constructs percent-encoded query string from given parms dictionary
     and appends to given url

    Usage::

        >>> util.join_url_params("example.com/index.html", {"page-id": 2, "Company": "Pay Pal"})
        example.com/index.html?page-id=2&Company=Pay+Pal
    """
    return url + "?" + urlencode(params)


def merge_dict(data, *override):
    """
    Merges any number of dictionaries together, and returns a single dictionary

    Usage::

        >>> util.merge_dict ({"foo": "bar"}, {1: 2}, {"Pay": "Pal"})
        {1: 2, 'foo': 'bar', 'Pay': 'Pal'}
    """
    result = {}
    for current_dict in (data,) + override:
        result.update(current_dict)
    return result

from django import template
import urlparse
from urllib import urlencode

register = template.Library()

def version(url, version):
    url_parts = urlparse.urlparse(url)
    query = urlparse.parse_qs(url_parts.query)
    query['v'] = version

    return urlparse.urlunparse(url_parts[:4] + (urlencode(query, True),) + url_parts[5:])

register.filter('version', version)

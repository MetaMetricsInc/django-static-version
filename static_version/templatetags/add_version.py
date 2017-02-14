import urlparse
from django import template
from urllib import urlencode
from django.templatetags.static import static
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def version(url, version):
    url_parts = urlparse.urlparse(url)
    query = urlparse.parse_qs(url_parts.query)
    query['v'] = version

    return urlparse.urlunparse(url_parts[:4] + (urlencode(query, True),) + url_parts[5:])

@register.simple_tag(takes_context=True)
def static_version(context, url):
    v = context['static_version']
    return version(static(url), v)

"""
    DO NOT ALTER OR REMOVE COPYRIGHT NOTICES OR THIS HEADER.

    Copyright (c) 2017 MetaMetrics Inc. All rights reserved.

    The contents of this file are subject to the terms of either the BSD
    or the Common Development and Distribution License("CDDL")
    (collectively, the "License").  You may not use this file except in
    compliance with the License.  You can obtain a copy of the License
    from LICENSE.txt in the root of the source distribution.
    See the License for the specific language governing permissions
    and limitations under the License.

    When distributing the software, include this License Header Notice in each
    file and include the License file LICENSE.txt.

    Modifications:
    If applicable, add the following below the License Header, with the fields
    enclosed by brackets [] replaced by your own identifying information:
    "Portions Copyright [year] [name of copyright owner]"
"""

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

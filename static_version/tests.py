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

import unittest

from django.conf import settings
from static_version.templatetags.add_version import version, static_version
from static_version.context_processors import static_urls

class TestPackage(unittest.TestCase):

    def test_context_processor(self):
        feaux_request = {
            'testkey':"testvalue"
        }

        updated_request = static_urls(feaux_request)

        # Make sure the version shows up properly
        self.assertEqual(updated_request['static_version'], settings.STATIC_VERSION)
        # Make sure the rest of the request doesn't disappear
        self.assertEqual(feaux_request['testkey'], updated_request['testkey'])

    def test_templatetag_simple(self):
        test_url = "http://fake.com/"

        tagged_url = version(test_url, settings.STATIC_VERSION)

        # Make sure the url is just the old url plus the version query
        self.assertEqual(test_url + "?v={}".format(settings.STATIC_VERSION), tagged_url)

    def test_templatetag_big_url(self):
        test_url = "file://fake.com:8080/this/has/multiple/levels/of/thing"

        tagged_url = version(test_url, settings.STATIC_VERSION)

        # Make sure the url is just the old url plus the version query
        self.assertIn(test_url + "?v={}".format(settings.STATIC_VERSION), tagged_url)

    def test_templatetag_add(self):
        test_url = "http://fake.com/?frontier=final"

        tagged_url = version(test_url, settings.STATIC_VERSION)

        # Make sure the new url has both query components
        self.assertIn("v={}".format(settings.STATIC_VERSION), tagged_url)
        self.assertIn("frontier=final", tagged_url)

    def test_template_tag(self):
        test_url = "relative.jpg"
        test_context = {'static_version':"1.0.1"}

        tagged_url = static_version(test_context, test_url)

        # Make sure the new url has both query components
        self.assertIn("v={}".format(test_context['static_version']), tagged_url)
        self.assertIn(settings.STATIC_URL, tagged_url)
        self.assertIn(test_url, tagged_url)

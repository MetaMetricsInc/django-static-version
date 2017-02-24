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
from mock import patch, mock_open
from django.test import TestCase
from django.conf import settings
from django.utils.six import StringIO
from static_version.util import parse_version
from django.core.management import call_command
from static_version.context_processors import static_urls
from static_version.templatetags.add_version import version, static_version

class TestManagementCommand(TestCase):

    @patch("checksumdir.dirhash")
    def test_matching_hash(self, mocked_dirhash):
        with patch("__builtin__.open", mock_open(read_data="7\nnotreallyahash\n")) as mocked_open:
            with self.settings(STATIC_VERSION_FILE='STATIC.VERSION'):
                mocked_dirhash.return_value = "notreallyahash"

                out = StringIO()
                call_command("check_version_update", stdout=out)

                self.assertNotIn("Detected hash change", out.getvalue())

    @patch("checksumdir.dirhash")
    def test_different_hash(self, mocked_dirhash):
        with patch("__builtin__.open", mock_open(read_data="7\nnotreallyahash\n")) as mocked_open:
            with self.settings(STATIC_VERSION_FILE='STATIC.VERSION'):
                mocked_dirhash.return_value = "notreallyahash3"

                out = StringIO()
                call_command("check_version_update", stdout=out)

                self.assertIn("Detected hash change", out.getvalue())

    @patch("checksumdir.dirhash")
    def test_missing_hash(self, mocked_dirhash):
        with patch("__builtin__.open", mock_open(read_data="7\n")) as mocked_open:
            with self.settings(STATIC_VERSION_FILE='STATIC.VERSION'):
                mocked_dirhash.return_value = "notreallyahash"

                out = StringIO()
                call_command("check_version_update", stdout=out)

                self.assertIn("Hash missing", out.getvalue())


    @patch("checksumdir.dirhash")
    def test_missing_version(self, mocked_dirhash):
        with patch("__builtin__.open", mock_open(read_data="notanumber\nnotreallyahash\n")) as mocked_open:
            with self.settings(STATIC_VERSION_FILE='STATIC.VERSION'):
                mocked_dirhash.return_value = "notreallyahash"

                out = StringIO()
                call_command("check_version_update", stdout=out)

                self.assertIn("Improperly formatted or missing version number", out.getvalue())

    @patch("checksumdir.dirhash")
    def test_missing_dir(self, mocked_dirhash):
        mocked_dirhash.side_effect = TypeError()
        with patch("__builtin__.open", mock_open(read_data="notanumber\nnotreallyahash\n")) as mocked_open:
            with self.settings(STATIC_VERSION_FILE='STATIC.VERSION'):
                # If the directory is missing. A TypeError will be raised.
                with self.assertRaises(TypeError):
                    out = StringIO()
                    call_command("check_version_update", stdout=out, stderr=out)


class TestUtils(TestCase):
    def test_util(self):
        with patch("static_version.util.open", mock_open(read_data="1\nnotreallyahash\n")) as mocked_open:
            with self.settings(STATIC_VERSION_FILE='STATIC.VERSION'):
                v = parse_version()

                self.assertEqual(1, v)

    def test_missing_setting(self):
        with patch("static_version.util.open", mock_open(read_data="1\nnotreallyahash\n")) as mocked_open:
            with self.assertRaises(AttributeError):
                v = parse_version()

    def test_bad_version_format(self):
        with patch("static_version.util.open", mock_open(read_data="notanumber\nnotreallyahash\n")) as mocked_open:
            with self.settings(STATIC_VERSION_FILE='STATIC.VERSION'):
                with self.assertRaises(ValueError):
                    v = parse_version()


    def test_missing_file(self):
        with patch("static_version.util.open", mock_open()) as mocked_open:
            mocked_open.side_effect =  IOError()
            with self.settings(STATIC_VERSION_FILE='STATIC.VERSION'):
                with self.assertRaises(IOError):
                    v = parse_version()

class TestContextProcessor(TestCase):
    def test_context_processor(self):
        feaux_request = {
        "testkey":"testvalue"
        }

        updated_request = static_urls(feaux_request)

        # Make sure the version shows up properly
        self.assertEqual(updated_request["static_version"], settings.STATIC_VERSION)
        # Make sure the rest of the request doesn't disappear
        self.assertEqual(feaux_request["testkey"], updated_request["testkey"])

class TestTemplateTag(TestCase):
    def test_templatetag_simple(self):
        test_url = "http://fake.com/"

        tagged_url = version(test_url, settings.STATIC_VERSION)

        # Make sure the url is just the old url plus the version query
        self.assertEqual(test_url + "?v={}".format(settings.STATIC_VERSION), tagged_url)

    def test_templatetag_big_url(self):
        test_url = "file://fake.com:8080/this/has/multiple/levels/of/thing"

        tagged_url = version(test_url, settings.STATIC_VERSION)

        self.assertIn(test_url + "?v={}".format(settings.STATIC_VERSION), tagged_url)

    def test_templatetag_add(self):
        test_url = "http://fake.com/?frontier=final"

        tagged_url = version(test_url, settings.STATIC_VERSION)

        self.assertEqual(test_url + "&v={}".format(settings.STATIC_VERSION), tagged_url)

    def test_templatetag_add_big_query(self):
        test_url = "http://fake.com/?this=that&here=there&tomayto=tomahto&foo=bar&location=nowhere"

        tagged_url = version(test_url, settings.STATIC_VERSION)

        self.assertEqual(test_url + "&v={}".format(settings.STATIC_VERSION), tagged_url)
        self.assertEqual(test_url + "&v={}".format(settings.STATIC_VERSION), tagged_url)

    def test_templatetag_add_query_with_fragment(self):
        test_url = "http://fake.com/"
        fragment= "#fragment"

        tagged_url = version(test_url + fragment, settings.STATIC_VERSION)

        self.assertEqual(test_url + "?v={}".format(settings.STATIC_VERSION) + fragment, tagged_url)

    def test_template_tag(self):
        test_url = "relative.jpg"
        test_context = {"static_version":"1.0.1"}

        tagged_url = static_version(test_context, test_url)

        # Make sure the new url has the query component, the relative url, and the static portion
        self.assertIn("v={}".format(test_context["static_version"]), tagged_url)
        self.assertIn(settings.STATIC_URL, tagged_url)
        self.assertIn(test_url, tagged_url)

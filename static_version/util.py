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

def parse_version():
    # A simple utility to parse the version out of the STATIC.VERSION file's first line
    from django.conf import settings
    try:
        with open(settings.STATIC_VERSION_FILE, 'r') as version_file:
            old_version = int(version_file.readline().strip())

            try:
                int(old_version)
            except ValueError as err:
                err.message = "The version number in {} is in an unsupported format. Please use an integer.".format(settings.STATIC_VERSION_FILE)
                raise

    except AttributeError as err:
        err.message = "The function parse_version requires a version file to be provided to parse. Please set the STATIC_VERSION_FILE setting"
        raise
    except IOError as err:
        err.message = "Please check that your {} file exists.".format(settings.STATIC_VERSION_FILE)
        raise

    return old_version

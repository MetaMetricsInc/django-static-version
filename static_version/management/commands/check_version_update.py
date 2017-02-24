
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
import checksumdir
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Check if the static files have changed, if neccessary bumps the integer version number and writes out the  new hash value.'

    def handle(self, *args, **options):
        old_version = 0
        old_hash = ""

        try:
            with open(settings.STATIC_VERSION_FILE, 'r') as version_file:
                old_version = int(version_file.readline().strip())
                old_hash = version_file.readline().strip()
        except IOError:
            self.stdout.write("No version file found, a new default file will be created at STATIC.VERSION")
        except StopIteration:
            self.stdout.write("Hash missing, this will ensure a version bump, but is otherwise harmless.")
        except ValueError:
            self.stdout.write("Improperly formatted or missing version number. Assumed 0.")

        try:
            new_hash = checksumdir.dirhash(settings.STATIC_ROOT, 'md5')
            self.stdout.write("Directory '{}' hashed to value: {}".format(settings.STATIC_ROOT, new_hash))
        except TypeError:
            self.stderr.write("Error: cannot compute the md5 checksum of the static directory.")
            raise

        if old_hash != new_hash:
            new_version = old_version + 1

            self.stdout.write("Detected hash change, writing out the bumped version (v={}) and new hash.".format(new_version))
            with open(settings.STATIC_VERSION_FILE, 'w') as version_file_out:
                version_file_out.write("{}\n".format(new_version))
                version_file_out.write("{}\n".format(new_hash))

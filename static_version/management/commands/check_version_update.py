
from checksumdir import dirhash
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Check if the static files have changed'

    def handle(self, *args, **options):
        # open up the stored version info
            # check for a hash value
            # hash the current directory
            #   have them run the collectstatic manually?
            #   grab the static dir and hash that
            # compare hashes and update version if neccessary
            # write out new version and hash
        old_version = 0
        old_hash = ""

        try:
            with open('STATIC.VERSION', 'r') as version_file:
                # We're only really interested in the first two lines of this file
                old_version = int(next(version_file).strip())
                old_hash = next(version_file).strip()
        except IOError:
            print("No version file found, a new default file will be created at STATIC.VERSION")
        except StopIteration:
            print("Hash missing, this will ensure a version bump, but is otherwise harmless.")
        except ValueError:
            print("Improperly formatted or missing version number. Assumed 0.")

        new_hash = dirhash(settings.STATIC_ROOT, 'md5')
        print("Directory '{}' hashed to value: {}".format(settings.STATIC_ROOT, new_hash))

        if old_hash != new_hash:
            new_version = old_version + 1

            print("Detected hash change, writing out the bumped version (v={}) and new hash.".format(new_version))
            with open('STATIC.VERSION', 'w') as version_file_out:
                version_file_out.write("{}\n".format(new_version))
                version_file_out.write("{}\n".format(new_hash))

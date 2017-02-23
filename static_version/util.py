# A simple utility to parse the version out of the STATIC.VERSION file's first line
def parse_version():
    from django.conf import settings
    try:
        with open(settings.STATIC_VERSION_FILE, 'r') as version_file:
            old_version = next(version_file).strip()

            try:
                int(old_version)
            except ValueError:
                raise Exception("The version number in {} is in an unsupported format. Please use an integer.".format(settings.STATIC_VERSION_FILE))

    except AttributeError:
        raise Exception("The function parse_version requires a version file to be provided to parse. Please set the STATIC_VERSION_FILE setting")
    except IOError:
        raise Exception("Please check that your {} file exists.".format(settings.STATIC_VERSION_FILE))

    return old_version

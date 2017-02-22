
# A simple utility to parse the version out of the VERSION file's first line
def parse_version():
    try:
        with open('STATIC.VERSION', 'r') as version_file:
            old_version = next(version_file).strip()
    except IOError:
        return "0"

    return old_version

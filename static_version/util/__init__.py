
# A simple utility to parse the version out of the VERSION file's first line
def parse_version():
    with open('VERSION', 'r') as version_file:
        old_version = next(version_file).strip()

    return old_version

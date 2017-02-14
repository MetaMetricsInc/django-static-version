import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()

setup(
    name='django-static-version',
    version='0.1',
    packages=['static_version', 'static_version.templatetags'],
    description='Small lib to add a version numbers to urls',
    long_description=README,
    author='Peter Konrad Konneker',
    author_email='pkonneker@lexile.com',
    url='https://github.com/yourname/django-myapp/',
    data_files = [("", ["LICENSE.txt"])],
    install_requires=[
        'Django>=1.9,<1.10',
    ]
)

import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

setup(
    name='django-static-version',
    version='0.1',
    packages=['static_version', 'static_version.templatetags'],
    description='Small lib to add a version numbers to urls',
    author='Peter Konrad Konneker',
    author_email='pkonneker@lexile.com',
    url='https://github.com/MetaMetricsInc/django-static-version',
    data_files = [("", ["LICENSE.txt", "README.md"])],
    install_requires=[
        'Django>=1.8,<1.10',
    ]
)

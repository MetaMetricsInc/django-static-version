# Static version

This is a simple django utility that adds a version number to static files with
a custom templatetag and context_processor. The version number is pulled from
the django settings. The  motivating use case was cache busting in S3, we will
simple bump up the version number on redeploy to invalidate static files.


# How to use

* Install this package
> python setup.py install
    - or
> pip install django-static-version
* Add setting for STATIC_VERSION (envs recommended, see example file: example/example/settings.py)
* Add context processor in settings (see example file: example/example/settings.py)
* Use the custom filter to add the version number to url query strings (again, see example file: example/example/home/templates/example/home/homepage.html)


# Tests
To run tests you simple run django-admin with the test_settings file

> django-admin.py test --settings=test_settings

# Static version

This is a simple django utility that adds a version number to static files with
a custom templatetag and context_processor. The version number is pulled from
the django settings. The  motivating use case was cache busting in CloudFront, we will
simple bump up the version number on redeploy to invalidate static files.


## How to use

* Install this package.
```bash
pip install django-static-version
```
* Add the setting for STATIC_VERSION.
```python
STATIC_VERSION="1.0.1"
```
* The setting can also be pulled from a version file. In this case you will also need the STATIC_VERSION_FILE setting. See below for the format of this file.
```python
from static_version.util import parse_version
STATIC_VERSION_FILE="STATIC.VERSION"
STATIC_VERSION=parse_version()
```
* Add the context processor in settings. This adds the setting above to the request context.
```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'static_version.context_processors.static_urls'
            ],
        },
    },
]
```
* Use the custom filter or tag to add the version number to url query strings. The filter `version` is available as follows:
```django
{{ "http://fake.com/"|version:static_version }}
```
The above code block will add our version number, 1.0.1, as the query string `?v=1.0.1` to the end of the url `http://fake.com/` resulting in `http://fake.com/?v=1.0.1`

Alternately we can use the custom template tag `static_version`.

```django
{% static_version 'bogus.jpg' %}
```
The above code will pull the version from the context and append it to the url returned by the built-in `static` tag and append the version number as above. This will result in `/static/bogus.jpg?v=1.2 ` if your static root is `/static/`.

## Version Management

### Management Command
A custom management command has been provided to hash a local copy of the collected static files and compare it to the hash stored in the version file. If the version needs  a bump, it will store a bumped version number and the new hash back into the version file. Make sure you call collectstatic first if neccessary.
```bash
python manage.py collectstatic  # need to have static files to hash
python manage.py check_version_update
```

### Version File
Consists of two parts on the first two lines of the file
1. Version number, currently just an integer
2. md5 hash of the static directory

Example:
```
7
0bba161a7165a211c7435c950ee78438
```

## Tests
To run tests you simple run django-admin with the test_settings file
```bash
django-admin.py test --settings=test_settings
```

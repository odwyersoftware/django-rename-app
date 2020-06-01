# django-rename-app

A Django Management Command to rename existing Django Applications.

[![PyPI version](https://badge.fury.io/py/django-rename-app.svg)](https://pypi.org/project/django-rename-app/)

# Installation

`pip install django-rename-app`.

Add to your Django settings.py `INSTALLED_APPS`:

```
INSTALLED_APPS = [
    ...
    'django_rename_app',
    ...
]
```

# Usage


`python manage.py rename_app <old_app_name> <new_app_name>`

For full detailed instructions see https://odwyer.software/blog/how-to-rename-an-existing-django-application


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

For full detailed instructions see https://odwyer.software/blog/how-to-rename-an-existing-django-application

`python manage.py rename_app <old_app_name> <new_app_name>`

If some of the affected models of your app use a custom table name by setting the attribute [db_table](https://docs.djangoproject.com/en/4.0/ref/models/options/#db-table), use the following additional argument:

`python manage.py rename_app <old_app_name> <new_app_name> -m "<old_tab_1>=<new_tab_1>" "<old_tab_2>=<new_tab_2>"`


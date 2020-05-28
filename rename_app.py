"""
A Django Management Command to rename existing Django Applications.

See https://github.com/odwyersoftware/django-rename-app
"""

import logging

from django.core.management.base import BaseCommand
from django.db import connection
from django.apps import apps

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = (
        'Renames a Django Application. Usage rename_app [old_name] [new_name]'
    )

    def add_arguments(self, parser):
        parser.add_argument('old_name', nargs=1, type=str)
        parser.add_argument('new_name', nargs=1, type=str)

    def handle(self, old_name, new_name, *args, **options):
        with connection.cursor() as cursor:
            old_name = old_name[0]
            new_name = new_name[0]

            cursor.execute(
                "SELECT * FROM django_content_type "
                f"where app_label='{new_name}'"
            )
            has_already_been_ran = cursor.fetchone()
            if has_already_been_ran:
                logger.info(
                    'Rename has already been done, exiting without '
                    'making any changes'
                )
                return None

            cursor.execute(
                f"UPDATE django_content_type SET app_label='{new_name}' "
                f"WHERE app_label='{old_name}'"
            )
            cursor.execute(
                f"UPDATE django_migrations SET app='{new_name}' "
                f"WHERE app='{old_name}'"
            )
            models = apps.all_models[new_name]
            models.update(apps.all_models[old_name])
            for model_name in models:
                query = (
                    f"ALTER TABLE {old_name}_{model_name} "
                    f"RENAME TO {new_name}_{model_name}"
                )
                cursor.execute(query)

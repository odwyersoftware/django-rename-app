"""
A Django Management Command to rename existing Django Applications.

See https://github.com/odwyersoftware/django-rename-app
"""

import logging

from django.core.management.base import BaseCommand
from django.db import connection, ProgrammingError
from django.db.backends.utils import truncate_name
from django.apps import apps

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = (
        'Renames a Django Application. Usage rename_app [old_app_name] [new_app_name]'
    )

    def add_arguments(self, parser):
        parser.add_argument('old_app_name', nargs=1, type=str)
        parser.add_argument('new_app_name', nargs=1, type=str)

    def handle(self, old_app_name, new_app_name, *args, **options):
        with connection.cursor() as cursor:
            old_app_name = old_app_name[0]
            new_app_name = new_app_name[0]

            cursor.execute(
                "SELECT * FROM django_content_type "
                f"where app_label='{new_app_name}'"
            )
            has_already_been_ran = cursor.fetchone()
            if has_already_been_ran:
                logger.info(
                    'Rename has already been done, exiting without '
                    'making any changes'
                )
                return None

            cursor.execute(
                f"UPDATE django_content_type SET app_label='{new_app_name}' "
                f"WHERE app_label='{old_app_name}'"
            )
            cursor.execute(
                f"UPDATE django_migrations SET app='{new_app_name}' "
                f"WHERE app='{old_app_name}'"
            )
            models = apps.all_models[new_app_name]
            models.update(apps.all_models[old_app_name])
            for model_name in models:
                old_table_name = truncate_name(
                    f"{old_app_name}_{model_name}",
                    connection.ops.max_name_length()
                )
                new_table_name = truncate_name(
                    f"{new_app_name}_{model_name}",
                    connection.ops.max_name_length()
                )

                query = (
                    f"ALTER TABLE {old_table_name} "
                    f"RENAME TO {new_table_name}"
                )
                try:
                    cursor.execute(query)
                except ProgrammingError:
                    logger.warning(
                        'Rename query failed: "%s"', query, exc_info=True
                    )

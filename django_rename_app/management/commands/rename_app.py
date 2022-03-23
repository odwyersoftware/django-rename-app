"""
A Django Management Command to rename existing Django Applications.
See https://github.com/odwyersoftware/django-rename-app
"""

import logging
from typing import Dict, List, Optional

from django.apps import apps
from django.core.management.base import BaseCommand
from django.db import ProgrammingError, connection
from django.db.backends.utils import truncate_name

logger = logging.getLogger(__name__)


def parse_new_tab_name_mapper(args: Optional[List[str]]) -> Dict[str, str]:
    """
    Parse --map-new-tab-name argument.

    Args:
        args (Optional[List[str]]): arguments to parse, something like: ['<old_tab_1>=<new_tab_1>','<old_tab_2>=<new_tab_2>']

    Returns:
        Dict[str, str]: Return a dict mapping new tab names to old tab names, something like:
        {<old_tab_1>: <new_tab_1>, <old_tab_2>: <new_tab_2>}
    """

    if not args:
        return {}
    res = {}
    for a in args:
        old_tab_name, new_tab_name = a.split('=')
        res[new_tab_name] = old_tab_name
    return res


class Command(BaseCommand):
    help = 'Renames a Django Application. Usage rename_app [old_app_name] [new_app_name]'

    def add_arguments(self, parser):
        parser.add_argument('old_app_name', nargs=1, type=str)
        parser.add_argument('new_app_name', nargs=1, type=str)
        parser.add_argument(
            '-m',
            '--map-new-tab-name',
            nargs='*',
            type=str,
            help='Map new db_tables to the old db_tables.'
            'Required only for models with custom db_table attribute.'
            'Example: --map-new-tab-name <old_tab_1>=<name_tab_1> <old_tab_2>=<new_tab_2> ...',
        )

    def handle(self, old_app_name: str, new_app_name: str, *args, **options):  # type: ignore
        with connection.cursor() as cursor:
            old_app_name = old_app_name[0]
            new_app_name = new_app_name[0]
            table_names_mapper: Dict[str, str] = parse_new_tab_name_mapper(options.get('map_new_tab_name'))

            cursor.execute("SELECT * FROM django_content_type " f"where app_label='{new_app_name}'")
            has_already_been_ran = cursor.fetchone()
            if has_already_been_ran:
                logger.info('Rename has already been done, exiting without ' 'making any changes')
                return None

            cursor.execute(
                f"UPDATE django_content_type SET app_label='{new_app_name}' " f"WHERE app_label='{old_app_name}'"
            )
            cursor.execute(f"UPDATE django_migrations SET app='{new_app_name}' " f"WHERE app='{old_app_name}'")

            models = apps.all_models[new_app_name]
            models.update(apps.all_models[old_app_name])
            for model_name, model in models.items():
                old_table_name = truncate_name(f"{old_app_name}_{model_name}", connection.ops.max_name_length())  # type: ignore
                new_table_name = truncate_name(f"{new_app_name}_{model_name}", connection.ops.max_name_length())  # type: ignore

                # Use a custom mapping for the current model table if set (required only for models with db_table set)
                if (
                    getattr(model, '_meta', None)
                    and getattr(model._meta, 'db_table', None)
                    and model._meta.db_table in table_names_mapper
                ):
                    old_table_name = table_names_mapper[model._meta.db_table]
                    new_table_name = model._meta.db_table

                query = f"ALTER TABLE {old_table_name} " f"RENAME TO {new_table_name}"
                try:
                    cursor.execute(query)
                except ProgrammingError:
                    logger.warning('Rename query failed: "%s"', query, exc_info=True)

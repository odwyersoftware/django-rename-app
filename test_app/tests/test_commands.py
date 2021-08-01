from io import StringIO

import pytest
from django.core.management import call_command
from django.db import OperationalError
from django.test import override_settings

from test_app.old_app.models import TestModel as OldModel


@pytest.mark.django_db()
class TestRenameApp:
    @staticmethod
    def call_command(*args, **kwargs):
        call_command(
            "rename_app",
            *args,
            **kwargs,
        )

    def test_rename_app(self):
        old_obj = OldModel.objects.create()
        out = StringIO()
        call_command("showmigrations", stdout=out)
        assert "old_app" in out.getvalue()

        installed_apps = [
            "django.contrib.contenttypes",
            "test_app.new_app.apps.NewAppConfig",  # change to the new app
            "django_rename_app",
        ]

        with override_settings(INSTALLED_APPS=installed_apps):
            self.call_command("old_app", "new_app")

            with pytest.raises(OperationalError) as err:
                old_obj.refresh_from_db()
            assert str(err.value) == "no such table: old_app_testmodel"

            from test_app.new_app.models import TestModel as NewModel

            new_obj = NewModel.objects.get()
            assert new_obj.uuid == old_obj.uuid

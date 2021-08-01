import uuid as uuid
from django.db import models


class TestModel(models.Model):
    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
    )

from django.db import models


class Task(models.Model):
    CREATED = "created"
    PROCESSING = "processing"
    COMPLETE = "complete"

    choices = [
        (CREATED, "created",),
        (PROCESSING, "processing",),
        (COMPLETE, "complete",),
    ]

    status = models.CharField(
        max_length=30,
        choices=choices,
        default=CREATED,
        null=False,
    )

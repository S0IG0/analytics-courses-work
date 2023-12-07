from django.db import models


# TODO add foreign-key on model
class Task(models.Model):
    CREATED = "created"
    PROCESSING = "processing"
    COMPLETE = "complete"
    ERROR = "error"

    choices = [
        (CREATED, "created",),
        (PROCESSING, "processing",),
        (COMPLETE, "complete",),
        (ERROR, "error",),
    ]

    status = models.CharField(
        max_length=30,
        choices=choices,
        default=CREATED,
        null=False,
    )

    files = models.ManyToManyField('files.File', related_name='tasks')

import time

from tasks.models import Task
from celery import shared_task


@shared_task
def analytics(pk):
    task = Task.objects.get(pk=pk)
    task.status = task.PROCESSING
    task.save()

    # TODO add pandas analytics
    time.sleep(20)

    task.status = task.COMPLETE
    task.save()

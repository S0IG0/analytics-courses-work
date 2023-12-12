import csv

from celery import shared_task

from files.models import File
from files.serializers import MacaroniSerializer


@shared_task
def save_rows(pk_file):
    file_instance = File.objects.get(pk=pk_file)
    csv_file = file_instance.file.path
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            row['file'] = file_instance.id
            macaroni_serializer = MacaroniSerializer(data=row)
            if macaroni_serializer.is_valid():
                macaroni_serializer.save()

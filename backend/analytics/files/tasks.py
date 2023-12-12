import csv

from celery import shared_task

from files.models import File
from files.serializers import MacaroniSerializer


# Словарь для соответствия имен столбцов CSV и полей в сериализаторе
column_mapping = {
    'Дата': 'date',
    'Время покупки': 'time_of_purchase',
    'Номер Карты': 'card_number',
    'Код товара': 'product_code',
    'Наименование товара': 'product_name',
    'Товарная группа': 'product_group',
    'Номер кассы': 'cash_register_number',
    'Количество': 'quantity',
    'Сумма по прейскуранту': 'price_list_amount',
    'Сумма к оплате': 'total_amount_due',
}


@shared_task
def save_rows(pk_file):
    file_instance = File.objects.get(pk=pk_file)
    csv_file = file_instance.file.path
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            row = {column_mapping[key]: value for key, value in row.items()}
            row['file'] = file_instance.id
            macaroni_serializer = MacaroniSerializer(data=row)
            if macaroni_serializer.is_valid():
                macaroni_serializer.save()

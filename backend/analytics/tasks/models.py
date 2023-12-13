from django.db import models


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
    delivery = models.BooleanField(default=False, null=False)


class Supply(models.Model):
    # Наименование товара
    name = models.TextField()
    # Дата
    date = models.DateField()
    # Поставка
    supply = models.FloatField()
    # Остаток на начало недели
    balance_first = models.FloatField()
    # Продажи за неделю
    sell = models.FloatField()
    # Остаток на складе
    balance_storage = models.FloatField()
    # Стоимость хранения за неделю
    price_storage = models.FloatField()
    # Прибыль от продаж
    profit = models.FloatField()
    # Чистая прибыль
    profit_clean = models.FloatField()
    # Упущенная выручка
    profit_missed = models.FloatField()

    # Каждая запись привязана к задаче
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

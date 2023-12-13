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
    date = models.DateTimeField()
    # Поставка
    supply = models.FloatField(null=False, default=0.0)
    # Остаток на начало недели
    balance_first = models.FloatField(null=False, default=0.0)
    # Продажи за неделю
    sell = models.FloatField(null=False, default=0.0)
    # Остаток на складе
    balance_storage = models.FloatField(null=False, default=0.0)
    # Стоимость хранения за неделю
    price_storage = models.FloatField(null=False, default=0.0)
    # Прибыль от продаж
    profit = models.FloatField(null=False, default=0.0)
    # Чистая прибыль
    profit_clean = models.FloatField(null=False, default=0.0)
    # Упущенная выручка
    profit_missed = models.FloatField(null=False, default=0.0)

    # Каждая запись привязана к задаче
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

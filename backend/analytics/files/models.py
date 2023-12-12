from django.db import models


class File(models.Model):
    file = models.FileField(upload_to='uploads/')
    description = models.TextField(null=True)
    title = models.TextField(null=True)


class Macaroni(models.Model):
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    date = models.DateField()
    time_of_purchase = models.CharField(max_length=20)
    card_number = models.CharField(max_length=20, null=True)
    product_code = models.CharField(max_length=20)
    product_name = models.CharField(max_length=255)
    product_group = models.CharField(max_length=50)
    cash_register_number = models.IntegerField()
    quantity = models.FloatField()
    price_list_amount = models.FloatField()
    total_amount_due = models.FloatField()

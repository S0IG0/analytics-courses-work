# Generated by Django 4.2.6 on 2023-12-09 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='description',
            field=models.TextField(null=True),
        ),
    ]
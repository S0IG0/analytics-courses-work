# Generated by Django 4.2.6 on 2023-12-11 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0002_file_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='title',
            field=models.TextField(null=True),
        ),
    ]

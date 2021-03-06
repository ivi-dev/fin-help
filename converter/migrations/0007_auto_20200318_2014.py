# Generated by Django 3.0.4 on 2020-03-18 18:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('converter', '0006_auto_20200318_1152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currency',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 18, 20, 14, 5, 590158)),
        ),
        migrations.AlterField(
            model_name='currency',
            name='latest_rate_update',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 18, 20, 14, 5, 590158)),
        ),
        migrations.AlterField(
            model_name='currency',
            name='symbol',
            field=models.CharField(default='', max_length=5),
        ),
    ]

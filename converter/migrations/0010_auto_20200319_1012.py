# Generated by Django 3.0.4 on 2020-03-19 08:12

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('converter', '0009_auto_20200319_1009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currency',
            name='date_valid',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]

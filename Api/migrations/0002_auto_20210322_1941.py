# Generated by Django 2.2b1 on 2021-03-22 18:41

import datetime
import django.core.validators
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournament',
            name='data',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 22, 19, 41, 7, 140404), validators=[django.core.validators.MinValueValidator(datetime.datetime(2021, 3, 22, 18, 41, 7, 140403, tzinfo=utc))]),
        ),
    ]

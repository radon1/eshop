# Generated by Django 2.1 on 2019-07-20 10:52

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_auto_20190627_1929'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 20, 10, 52, 1, 886185, tzinfo=utc), verbose_name='Дата'),
        ),
    ]

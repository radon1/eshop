# Generated by Django 2.1 on 2019-09-22 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_auto_20190908_1019'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total',
            field=models.PositiveIntegerField(default=0, verbose_name='Общая сумма'),
        ),
    ]

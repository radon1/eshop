# Generated by Django 2.1 on 2019-08-25 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_auto_20190824_1115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='country',
            field=models.CharField(choices=[('1', 'Russia'), ('2', 'Usa'), ('3', 'Ukraine'), ('4', 'Belarus')], default='', max_length=120, verbose_name='Страна'),
        ),
    ]

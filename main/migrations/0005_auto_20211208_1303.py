# Generated by Django 2.2.19 on 2021-12-08 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20211208_1257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seller',
            name='count',
            field=models.PositiveIntegerField(null=True, verbose_name='Количество объявлений'),
        ),
    ]

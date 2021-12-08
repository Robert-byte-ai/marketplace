# Generated by Django 2.2.19 on 2021-12-08 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_ad_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArchiveAds',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('main.ad',),
        ),
        migrations.AddField(
            model_name='ad',
            name='is_archive',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='ad',
            name='name',
            field=models.CharField(db_index=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(db_index=True, max_length=200),
        ),
    ]

# Generated by Django 2.0 on 2018-06-23 01:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20180622_2223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='canal',
            name='nome_canal',
            field=models.CharField(blank=True, max_length=30, unique=True),
        ),
    ]
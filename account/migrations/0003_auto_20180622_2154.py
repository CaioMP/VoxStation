# Generated by Django 2.0 on 2018-06-23 00:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20180620_1749'),
    ]

    operations = [
        migrations.AlterField(
            model_name='canal',
            name='nome_canal',
            field=models.CharField(blank=True, max_length=30, unique=True),
        ),
    ]
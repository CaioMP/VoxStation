# Generated by Django 2.0 on 2018-10-11 17:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('channel', '0041_auto_20181011_1434'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='aparicoes',
        ),
    ]
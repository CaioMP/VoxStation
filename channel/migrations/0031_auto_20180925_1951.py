# Generated by Django 2.0 on 2018-09-25 22:51

import channel.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('channel', '0030_auto_20180924_1446'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audio',
            name='duracao',
            field=models.CharField(blank=True, default=channel.models.Audio.get_duration, max_length=15, null=True),
        ),
    ]

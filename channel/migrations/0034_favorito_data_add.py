# Generated by Django 2.0 on 2018-10-02 21:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('channel', '0033_audio_duracao'),
    ]

    operations = [
        migrations.AddField(
            model_name='favorito',
            name='data_add',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
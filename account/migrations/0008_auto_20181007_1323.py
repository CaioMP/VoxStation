# Generated by Django 2.0 on 2018-10-07 16:23

import account.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_auto_20180921_1748'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='img_perfil',
            field=models.ImageField(blank=True, default='static\\images\\default-user.png', null=True, upload_to=account.models.MyUser.user_directory_path),
        ),
    ]

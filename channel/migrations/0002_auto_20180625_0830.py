# Generated by Django 2.0 on 2018-06-25 11:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_auto_20180622_2316'),
        ('channel', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='audio',
            name='canal_proprietario',
        ),
        migrations.AddField(
            model_name='audio',
            name='canal_proprietario',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='canal_proprietario', to='account.Canal'),
        ),
    ]
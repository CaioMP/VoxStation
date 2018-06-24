# Generated by Django 2.0 on 2018-06-20 01:17

import account.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, default='', max_length=128)),
                ('genero', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], default='M', max_length=1, verbose_name='gender')),
                ('pais', django_countries.fields.CountryField(blank=True, max_length=2)),
                ('sobre', models.TextField(blank=True, null=True)),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('first_name', models.CharField(blank=True, max_length=32, validators=[django.core.validators.RegexValidator(code='invalid_first_name', message='O primeiro nome deve ser alfanumérico ou conter números.', regex='^[a-zA-Z0-9.+-]*$')], verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=32, validators=[django.core.validators.RegexValidator(code='invalid_last_name', message='O sobrenome deve ser alfanumérico ou conter números.', regex='^[a-zA-Z0-9.+-]*$')], verbose_name='last name')),
                ('username', models.CharField(max_length=300, unique=True, validators=[django.core.validators.RegexValidator(code='invalid_username', message='O nome de usuário deve ser alfanumérico ou conter números.', regex='^[a-zA-Z0-9.+-]*$')], verbose_name='username')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email')),
                ('img_perfil', models.ImageField(blank=True, null=True, upload_to=account.models.MyUser.user_directory_path)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Anuncio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=15)),
                ('exibicoes', models.IntegerField()),
                ('link', models.CharField(max_length=100)),
                ('caminho', models.CharField(max_length=150)),
                ('tempo', models.CharField(max_length=15)),
                ('descricao', models.TextField()),
                ('anunciante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Canal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prop_key', models.IntegerField(null=True)),
                ('nome_canal', models.CharField(max_length=30, unique=True)),
                ('foto_canal', models.ImageField(blank=True, null=True, upload_to=account.models.Canal.foto_canal_path)),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('capa', models.ImageField(blank=True, upload_to=account.models.Canal.capa_path)),
                ('audio_fundo', models.FileField(blank=True, upload_to=account.models.Canal.audio_fundo_path)),
                ('descricao', models.TextField(blank=True, null=True)),
                ('proprietario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('conteudo', models.TextField()),
                ('likes', models.IntegerField()),
                ('deslikes', models.IntegerField()),
                ('comentarista', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Resposta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('conteudo', models.TextField()),
                ('likes', models.IntegerField()),
                ('deslikes', models.IntegerField()),
                ('comentario_em_questao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Comentario')),
                ('comentarista', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Seg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.CharField(choices=[(0, 'normal'), (1, 'bloqueado')], max_length=10)),
                ('seguidores', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sendo_seguido_por', to=settings.AUTH_USER_MODEL)),
                ('seguindo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seguindo', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='canal',
            name='seguidor',
            field=models.ManyToManyField(blank=True, related_name='segue', through='account.Seg', to='account.Canal'),
        ),
    ]

from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import ugettext_lazy as _

USERNAME_REGEX = '^[a-zA-Z0-9.+-]*$'


class MyUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=username,
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(username, email, password=password)
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    def user_directory_path(instance, filename):
        # A foto de perfil irá para MEDIA_ROOT/user_<id>/img_perfil/<filename>
        return 'contas/user_{0}/img_perfil/{1}'.format(instance.pk, filename)

    def user_audio_path(instance, filename):
        return 'contas/user_{0}/audios/{1}'.format(instance.pk, filename)

    def user_audio_capa_path(instance, filename):
        return "contas/user_{0}/capas_audios/{1}".format(instance.pk, filename)

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    )

    phone = PhoneNumberField(default="", blank=True)
    genero = models.CharField('gender', choices=GENDER_CHOICES, max_length=1, default='M')
    pais = CountryField(blank=True)
    sobre = models.TextField(null=True, blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    first_name = models.CharField('first name', max_length=32,
                                  validators=[
                                      RegexValidator(regex=USERNAME_REGEX,
                                                     message=_('O primeiro nome deve ser alfanumérico ou conter números.'),
                                                     code='invalid_first_name'
                                                     )], blank=True)

    last_name = models.CharField('last name', max_length=32,
                                 validators=[
                                      RegexValidator(regex=USERNAME_REGEX,
                                                     message=_('O sobrenome deve ser alfanumérico ou conter números.'),
                                                     code='invalid_last_name'
                                                     )], blank=True)

    username = models.CharField(
        'username', max_length=300,
        validators=[
            RegexValidator(regex=USERNAME_REGEX,
                           message=_('O nome de usuário deve ser alfanumérico ou conter números.'),
                           code='invalid_username'
                           )], unique=True
    )

    email = models.EmailField(
        'email',
        max_length=255,
        unique=True,
    )

    img_perfil = models.ImageField(upload_to=user_directory_path, blank=True, null=True)

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class Canal(models.Model):
    def foto_canal_path(instance, filename):
        # A foto do canal irá para MEDIA_ROOT/user_<pk>/canal_id/fotos/<filename>
        return 'contas/user_{0}/canal_{1}/fotos/{2}'.format(instance.prop_key, instance.nome_canal, filename)

    def capa_path(instance, filename):
        # A capa do canal irá para MEDIA_ROOT/user_<pk_do_canal>/canal_<nome>/capas/<filename>
        return 'contas/user_{0}/canal_{1}/capas/{2}'.format(instance.prop_key, instance.nome_canal, filename)

    def audio_fundo_path(instance, filename):
        # O áudio de fundo do canal irá para MEDIA_ROOT/user_<pk_do_canal>/canal_<nome>/audios/<filename>
        return 'contas/user_{0}/canal_{1}/audios/{2}'.format(instance.prop_key, instance.nome_canal, filename)

    prop_key = models.IntegerField(null=True)
    proprietario = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    nome_canal = models.CharField(max_length=30, blank=False,
                                  validators=[
                                      RegexValidator(regex=USERNAME_REGEX,
                                                     message=_('O nome do canal deve ser alfanumérico ou conter números.'),
                                                     code='invalid_username'
                                                     )], unique=True, null=False)
    foto_canal = models.ImageField(upload_to=foto_canal_path, blank=True, null=True, default="static/images/default-user.png")
    data_criacao = models.DateTimeField(auto_now_add=True)
    capa = models.ImageField(upload_to=capa_path, blank=True, null=True)
    audio_fundo = models.FileField(upload_to=audio_fundo_path, blank=True, null=True)
    seguidor = models.ManyToManyField(MyUser, blank=True, related_name="segue", symmetrical=False, through="Seg")
    descricao = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nome_canal


class Anuncio(models.Model):

    titulo = models.CharField(max_length=15)
    exibicoes = models.IntegerField()
    link = models.CharField(max_length=100)
    caminho = models.CharField(max_length=150)
    tempo = models.CharField(max_length=15)
    descricao = models.TextField()
    anunciante = models.ForeignKey(MyUser, on_delete=models.CASCADE)


class Comentario(models.Model):
    conteudo = models.TextField()
    likes = models.IntegerField()
    deslikes = models.IntegerField()
    comentarista = models.ForeignKey(MyUser, on_delete=models.CASCADE)


class Resposta(models.Model):

    conteudo = models.TextField()
    likes = models.IntegerField()
    deslikes = models.IntegerField()
    comentarista = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    comentario_em_questao = models.ForeignKey(Comentario, on_delete=models.CASCADE)


class Seg(models.Model):
    estado_choices = ((0, "normal"), (1, "bloqueado"))
    seguidores = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name="sendo_seguido_por", default=None)
    canal_seguido = models.ForeignKey(Canal, on_delete=models.CASCADE, related_name="seguido",default=None )
    estado = models.CharField(max_length=10, choices=estado_choices)

    def __str__(self):
        return self.canal_seguido.nome_canal+"_"+self.seguidores.username

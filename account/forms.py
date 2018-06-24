from django.contrib.auth import get_user_model

from django.contrib.auth.forms import PasswordChangeForm
from django import forms
from django.utils.translation import ugettext_lazy as _
from django_countries.widgets import CountrySelectWidget
from django_countries import Countries
from phonenumber_field.formfields import PhoneNumberField
from .validators import (validate_domain_email, validate_username,
                         validate_password, validate_password2)
from channel.models import Audio
from .models import Canal
User = get_user_model()


class UserCreationForm(forms.ModelForm):
    username = forms.CharField(validators=[validate_username])
    email = forms.EmailField(validators=[validate_domain_email],
                             error_messages={'unique': _('Um usuário com esse email já existe.')})
    password1 = forms.CharField(validators=[validate_password])
    password2 = forms.CharField(validators=[validate_password2])

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password1',
            'password2'
        ]


class UserLoginForm(forms.Form):
    global has_error

    query = forms.CharField(label=_('Nome de Usuário ou Email'))
    password = forms.CharField(label=_('Senha'), widget=forms.PasswordInput)


class ChangePasswordForm(PasswordChangeForm):
    new_password1 = forms.CharField(label=_('Nova senha'), widget=forms.PasswordInput,
                                    max_length=32, validators=[validate_password])

    new_password2 = forms.CharField(label=_('Digite-a novamente'), widget=forms.PasswordInput,
                                    max_length=32, validators=[validate_password2])

    class Meta:
        model = User
        fields = '__all__'

    def clean_old_password(self):
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(_("Sua senha antiga não é essa."))

        return old_password


# Formulário com as informações básicas da conta (email, senha, país, telefone e gênero)
class EditBasicForm(forms.ModelForm):
    GENDER_CHOICES = (
        ('M', _('Masculino')),
        ('F', _('Feminino')),
        ('O', _('Outro'))
    )

    phone = PhoneNumberField(label=_('Telefone'), required=False, help_text=_('(Opcional)'))
    email = forms.EmailField(label=_('Endereço de Email'), validators=[validate_domain_email],
                             error_messages={'unique': _('Um usuário com esse email já existe.')})
    pais = forms.ChoiceField(widget=CountrySelectWidget, label=_('País'), choices=Countries)
    genero = forms.ChoiceField(widget=forms.RadioSelect, choices=GENDER_CHOICES, label=_('Gênero'))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'pw-change'}), label=_('Senha'), required=False, max_length=32)

    class Meta:
        model = User
        fields = [
            'email',
            'phone',
            'pais',
            'genero',
            'password1'
        ]


# Formulário criado antes da imagem de perfil
class EditProfileForm(forms.ModelForm):
    first_name = forms.CharField(label=_('Nome'), required=True)
    last_name = forms.CharField(label=_('Sobrenome'), required=True)
    img_perfil = forms.ImageField(widget=forms.FileInput(attrs={'id': 'troca-foto'}), label=_('Imagem'), required=False)

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'img_perfil'
        ]


# Formulário auxiliar criado após a imagem de perfil
class AuxForm(forms.ModelForm):
    username = forms.CharField(label=_('Nome de usuário'), error_messages={'unique': _('Um usuário com esse nome já existe.')},
                               required=True)

    sobre = forms.CharField(widget=forms.Textarea, label=_('Sobre você'), required=False)

    def valid_old_username(self, new_username):
        old_username = self.instance

        # Verifica se o novo nome de usuário é igual ao antigo (para o caso do usuário não ter trocado esse campo)
        if new_username == old_username:
            validate_username(new_username)  # Agora é verificado se esse novo nome de usuário já existe

    class Meta:
        model = User
        fields = [
            'username',
            'sobre'
        ]


class AudioForm(forms.ModelForm):
    audio = forms.FileField(widget=forms.FileInput)
    capa = forms.ImageField(widget=forms.FileInput,)
    titulo = forms.CharField()
    descricao = forms.Textarea()

    class Meta:
        model = Audio
        fields = [
            'audio',
            'capa',
            'titulo',
            'descricao'
        ]


class NewChannelForm(forms.ModelForm):
    foto_canal = forms.FileField(widget=forms.FileInput(attrs={'id': 'foto-canal'}), required=False)
    capa = forms.FileField(widget=forms.FileInput(attrs={'id': 'fundo'}), required=False)
    audio_fundo = forms.FileField(widget=forms.FileInput(attrs={'id': 'audio'}), required=False)
    nome_canal = forms.CharField(error_messages={'unique': _('Um canal com esse nome já existe.')}, required=False)

    class Meta:
        model = Canal
        fields = [
            'nome_canal', 'foto_canal', 'capa',
            'audio_fundo', 'descricao'
        ]





























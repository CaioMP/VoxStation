from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _


User = get_user_model()


# Método para verificar se o domínio do email existe
def validate_domain_email(value):
    if not value.endswith('.com'):
        raise ValidationError(_('Informe um endereço de email válido.'))
    if not "@gmail.com" in value:
        if not "@live.com" in value:
            if not "@outlook.com" in value:
                if not "@hotmail.com" in value:
                    if not "@yahoo.com" in value:
                        if not "@ymail.com" in value:
                            if not "@uol.com" in value:
                                if not "@protonmail.com" in value:
                                    raise ValidationError(_('Informe um endereço de email válido.'))
    return value


def validate_username(username):
    username_qs = User.objects.filter(username=username)

    if username_qs.exists():
        raise ValidationError(_('Um usuário com esse nome já existe.'))
    return username


aux = ''


def validate_password(password):
    global aux

    msg = ''
    aux = password

    # --> Verifica o tamanho da senha
    if len(password) < 8:
        msg = _('A senha deve conter no mínimo 8 caracteres.')
        raise ValidationError(msg)

    if msg == '':
        # --> Verifica se há números na senha
        if sum(c.isdigit() for c in password) < 1:
            msg = _('A senha deve conter no mínimo 1 número.')
            raise ValidationError(msg)

    if msg == '':
        # --> Verifica se há letras maiúsculas na senha
        if not any(c.isupper() for c in password):
            msg = _('A senha deve conter letras maiúsculas e minúsculas.')
            raise ValidationError(msg)

    if msg == '':
        # --> Verifica se há letras minúsculas na senha
        if not any(c.islower() for c in password):
            msg = _('A senha deve conter letras maiúsculas e minúsculas.')
            raise ValidationError(msg)

    return aux


def validate_password2(password2):
    global aux

    if aux != password2:
        raise ValidationError(_('As senhas devem ser iguais.'))

    if len(password2) < 8 or sum(c.isdigit() for c in password2) < 1 or \
            not any(c.isupper() for c in password2) or \
            not any(c.islower() for c in password2):
        raise ValidationError('')  # --> Esse if foi necessário para não mostrar um mesmo erro duas vezes no cadastro

    return aux

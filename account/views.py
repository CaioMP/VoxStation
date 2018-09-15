from django.shortcuts import render, redirect,HttpResponse
from django.contrib.auth import (
    login as auth_login,
    get_user_model,
    authenticate
)
from channel.models import Audio, Playlist, Canal
from django.contrib.auth import update_session_auth_hash
from django.db.models import Q
from .forms import (UserCreationForm, UserLoginForm, EditBasicForm, NewChannelForm,
                    EditProfileForm, AuxForm, ChangePasswordForm, AudioForm)
from django.contrib import messages
from django.contrib.auth.views import logout
from django.utils.translation import ugettext_lazy as _

User = get_user_model()


def RegisterView(request):
    if not request.user.is_authenticated:
        account = UserCreationForm(request.POST or None)

        if account.is_valid():
            account.save(commit=False)

            password = account.cleaned_data['password2']

            profile = User()
            profile.first_name = account.cleaned_data['first_name']
            profile.last_name = account.cleaned_data['last_name']
            profile.username = account.cleaned_data['username']
            profile.email = account.cleaned_data['email']
            profile.set_password(password)
            profile.save()

            new_user = authenticate(
                username=account.cleaned_data['email'],
                password=password
            )
            auth_login(request, new_user, backend='django.contrib.auth.backends.ModelBackend')

            return redirect('/')
        else:
            first_name = 'first_name'
            last_name = 'last_name'
            email = 'email'
            username = 'username'
            password1 = 'password1'
            password2 = 'password2'

            for field in account:
                if not field.errors:
                    if field.name == first_name:  # Verifica se o campo first_name não tem erros
                        first_name = request.POST.get(field.name)  # Pega o valor do campo first_name

                    elif field.name == last_name:  # Verifica se o campo last_name não tem erros
                        last_name = request.POST.get(field.name)  # Pega o valor do campo last_name

                    elif field.name == email:  # Verifica se o campo email não tem erros
                        email = request.POST.get(field.name)  # Pega o valor do campo email

                    elif field.name == username:  # Verifica se o campo username não tem erros
                        username = request.POST.get(field.name)  # Pega o valor do campo username

                    elif field.name == password1:  # Verifica se o campo password1 não tem erros
                        password1 = request.POST.get(field.name)  # Pega o valor do campo password1

                    elif field.name == password2:  # Verifica se o campo password2 não tem erros
                        password2 = request.POST.get(field.name)  # Pega o valor do campo password2

            # Caso exista algum erro em um campo, ele será limpo
            if first_name == 'first_name':
                first_name = ''

            if last_name == 'last_name':
                last_name = ''

            if email == 'email':
                email = ''

            if username == 'username':
                username = ''

            if password1 == 'password1':
                password1 = ''

            if password2 == 'password2':
                password2 = ''

            context = {"account": account, "first_name": first_name, "last_name": last_name,
                       "email": email, "username": username, "password1": password1, "password2": password2}

            return render(request, './account/register.html', context)
    else:
        return redirect('/')


def LoginView(request):
    if not request.user.is_authenticated:
        form = UserLoginForm(request.POST or None)

        if form.is_valid():
            query = form.cleaned_data.get('query')  # Username or Email
            password = form.cleaned_data.get('password')

            user_qs_final = User.objects.filter(
                Q(username__iexact=query) |
                Q(email__iexact=query)
            ).distinct()  # Verifica se existe algum usuário com o username ou email descrito

            user_obj = user_qs_final.first()  # Retorna o email encontrado

            if not user_obj:
                messages.error(request, _('Nome de usuário ou senha incorretos'))
            else:
                user = User.objects.get(email=user_obj.email)
                if user.check_password(password):
                    auth_login(request, user_obj, backend='django.contrib.auth.backends.ModelBackend')
                    return redirect('/')
                else:
                    messages.error(request, _('Nome de usuário ou senha incorretos'))
    else:
        return redirect('/')  # Caso o usuário tente fazer login estando logado

    return render(request, "./account/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect('/')


edited_password = False  # Variável para verificar e mostrar se a senha foi editada


def edit_profile(request):
    global edited_password

    edited = False  # Variável para verificar e mostrar se algo foi editado com sucesso
    has_error = False  # Váriavel para verificar e mostrar se ocorreu algum erro ao salvar
    footer = True  # Váriavel para colocar o footer no final da base2.tml

    if request.method == 'POST':
        basicform = EditBasicForm(request.POST, instance=request.user)
        profileform = EditProfileForm(request.POST, request.FILES, instance=request.user)
        auxform = AuxForm(request.POST, instance=request.user)

        auxform.valid_old_username(new_username=request.POST['username'])

        if basicform.is_valid() and profileform.is_valid() and auxform.is_valid():
            basicform.save()
            profileform.save()
            auxform.save()

            edited = True
        else:
            has_error = True
            request.user.email = request.POST['email']
            request.user.username = request.POST['username']
    else:
        basicform = EditBasicForm(instance=request.user)
        profileform = EditProfileForm(instance=request.user)
        auxform = AuxForm(instance=request.user)

    context = {"basicform": basicform, "profileform": profileform, "auxform": auxform, "footer": footer, "logado": request.user.is_active,
               "has_error": has_error, "edited": edited, "edited_password": edited_password, "user": request.user}

    if edited_password:
        edited_password = False

    return render(request, './account/edit_account.html', context)


def change_password(request):
    global edited_password

    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            edited_password = True

            return redirect('/profile/edit/')
        else:
            old_password = 'old_password'
            new_password1 = 'new_password1'
            new_password2 = 'new_password2'

            for field in form:
                if not field.errors:
                    if field.name == old_password:  # Verifica se o campo 'Senha antiga' não tem erros
                        old_password = request.POST.get(field.name)  # Pega o valor do campo senha antiga

                    elif field.name == new_password1:  # Verifica se o campo 'Nova senha' não tem erros
                        new_password1 = request.POST.get(field.name)  # Pega o valor do campo 'Nova senha'

                    elif field.name == new_password2:  # Verifica se o campo 'Digite-a novamente' não tem erros
                        new_password2 = request.POST.get(field.name)  # Pega o valor do campo 'Digite-a novamente'

            # Caso exista algum erro em um campo, ele será limpo
            if old_password == 'old_password':
                old_password = ''

            if new_password1 == 'new_password1':
                new_password1 = ''

            if new_password2 == 'new_password2':
                new_password2 = ''

            context = {'form': form, 'old_password': old_password, 'logado': request.user.is_active,
                       'new_password1': new_password1, 'new_password2': new_password2}

            return render(request, './account/change_password.html', context)

    else:
        edited_password = False
        form = ChangePasswordForm(request.user)
    return render(request, './account/change_password.html', {'form': form, 'logado': request.user.is_active})


def NewChannelView(request):
    form = NewChannelForm(request.POST, request.FILES or None)
    error_nome_canal = ""
    nome_canal = ""

    if request.method == 'POST':
        if form.is_valid():
            instance = form.save(commit=False)
            instance.proprietario = request.user
            instance.prop_key = request.user.pk
            instance.save()
            return redirect('/')  # Dps arrumar pra ir pra tela do canal
        else:
            if form.errors:
                for field in form:
                    for error in field.errors:
                        nome_canal = request.POST['nome_canal']
                        error_nome_canal = error
            form = NewChannelForm()

    context = {'form': form, 'error_nome_canal': error_nome_canal, 'nome_canal': nome_canal,
               'user': request.user, 'logado': request.user.is_active}

    return render(request, './account/new_channel.html', context)


def historic(request):
    contexto = {}

    if request.user.is_active:
        contexto['play_side'] = Playlist.objects.filter(proprietario=request.user)
        contexto['canal_side'] = Canal.objects.filter(seguidor=request.user)
    contexto['logado'] = request.user.is_active
    return render(request, './account/historic.html', contexto)

import os
from hashlib import sha256

from django.conf import settings
from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .models import Ativacao
from .utils import (email_html, email_is_valid, password_is_valid,
                    username_is_valid)

# Create your views here.


def cadastro(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/')

        return render(request, 'cadastro.html')

    elif request.method == 'POST':
        usuario = request.POST['usuario']
        email = request.POST['email']
        senha = request.POST['senha']
        confirmar_senha = request.POST['confirmar_senha']

        if not username_is_valid(request, usuario):
            return redirect('/auth/cadastro')

        if not email_is_valid(request, email):
            return redirect('/auth/cadastro')

        if not password_is_valid(request, senha, confirmar_senha):
            return redirect('/auth/cadastro')

        # Verifica se o nome de usuário já está cadastrado:
        user = User.objects.filter(username=usuario)

        if user.exists():
            messages.add_message(request, constants.ERROR,
                                 'Este nome de usuário já está cadastrado.')
            return redirect('/auth/cadastro')

        try:
            user = User.objects.create_user(username=usuario,
                                            email=email,
                                            password=senha,
                                            is_active=False)
            user.save()

            # Após o cadastro, será gerado um token para ativação da conta:
            token = sha256(f'{usuario}{email}'.encode()).hexdigest()
            ativacao = Ativacao(token=token, user=user)
            ativacao.save()

            # Em seguida, será enviado um código de ativação da conta para o email do novo usuário:
            path_template = os.path.join(
                settings.BASE_DIR,
                'autenticacao/templates/emails/cadastro_confirmado.html'
            )
            email_html(
                path_template=path_template,
                assunto='Cadastro confirmado',
                para=[email, ],
                username=usuario,
                link_ativacao=f"127.0.0.1:8000/auth/ativar_conta/{token}"
            )

            messages.add_message(request, constants.SUCCESS,
                                 'Usuário criado com sucesso.')
            messages.add_message(request, constants.WARNING,
                                 'Foi enviado um link de ativação para o seu E-mail.')
            return redirect('/auth/logar')

        except:
            messages.add_message(request, constants.ERROR,
                                 'Erro interno do sistema.')
            return redirect('/auth/cadastro')


def logar(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/')

        return render(request, 'logar.html')

    elif request.method == 'POST':
        username = request.POST['usuario']
        senha = request.POST['senha']

        usuario = auth.authenticate(username=username, password=senha)

        if not usuario:
            messages.add_message(request, constants.ERROR,
                                 'Nome de usuário ou Senha inválidos')
            return redirect('/auth/logar')
        else:
            auth.login(request, usuario)
            return redirect('/')


def sair(request):
    auth.logout(request)
    return redirect('/auth/logar')


def ativar_conta(request, token):
    token = get_object_or_404(Ativacao, token=token)

    # caso a conta já tenha sido ativada:
    if token.ativo:
        messages.add_message(request, constants.WARNING,
                             'Este token já foi usado.')
        return redirect('/auth/logar')

    user = User.objects.get(username=token.user.username)
    user.is_active = True
    user.save()
    token.ativo = True
    token.save()

    messages.add_message(request, constants.SUCCESS,
                         'Conta ativada com sucesso!')
    return redirect('/auth/logar')

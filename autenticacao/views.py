from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .utils import email_is_valid, password_is_valid, username_is_valid

# Create your views here.


def cadastro(request):
    if request.method == 'GET':
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
                                 f'Esse nome de usuário já está cadastrado')
            return redirect('/auth/cadastro')

        try:
            user = User.objects.create_user(username=usuario,
                                            email=email,
                                            password=senha,
                                            is_active=False)
            user.save()
            messages.add_message(request, constants.SUCCESS,
                                 'Usuário criado com sucesso.')
            return redirect('/auth/logar')

        except:
            messages.add_message(request, constants.ERROR,
                                 'Erro interno do sistema.')
            return redirect('/auth/cadastro')


def logar(request):
    return HttpResponse('Página de login')

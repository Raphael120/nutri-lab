from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages import constants
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .utils import paciente_is_valid

from plataforma.models import Paciente

# Create your views here.


@login_required(login_url='/auth/logar')
def pacientes(request):
    if request.method == 'GET':
        pacientes = Paciente.objects.filter(nutricionista=request.user)
        return render(request, 'pacientes.html', {'pacientes': pacientes})

    elif request.method == 'POST':
        nome = request.POST['nome']
        sobrenome = request.POST['sobrenome']
        sexo = request.POST['sexo']
        idade = request.POST['idade']
        email = request.POST['email']
        telefone = request.POST['telefone']

        if not paciente_is_valid(request, nome, sobrenome, sexo, idade, email, telefone):
            return redirect('/pacientes/')

        try:
            p = Paciente(
                nome=nome,
                sobrenome=sobrenome,
                sexo=sexo,
                idade=idade,
                email=email,
                telefone=telefone,
                nutricionista=request.user
            )
            p.save()

            messages.add_message(
                request=request,
                level=constants.SUCCESS,
                message='Paciente cadastrado com sucesso'
            )
            return redirect('/pacientes/')

        except:
            messages.add_message(
                request=request,
                level=constants.ERROR,
                message='Erro interno do sistema'
            )
            return redirect('/pacientes/')

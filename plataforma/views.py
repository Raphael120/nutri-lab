from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages import constants
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt

from plataforma.models import DadosPaciente, Paciente

from .utils import dados_paciente_is_valid, paciente_is_valid

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


@login_required(login_url='/auth/logar')
def listar_dados_paciente(request):
    if request.method == 'GET':
        pacientes = Paciente.objects.filter(nutricionista=request.user)
        return render(request, 'listar_dados_paciente.html', {'pacientes': pacientes})


@login_required(login_url='/auth/logar')
def dados_paciente(request, id):
    paciente = get_object_or_404(Paciente, id=id)

    if not paciente.nutricionista == request.user:
        messages.add_message(
            request=request,
            level=constants.ERROR,
            message='Esse paciente não é seu'
        )
        return redirect('/dados_paciente/')

    if request.method == 'GET':
        dados_do_paciente = DadosPaciente.objects.filter(paciente=paciente)

        context = {
            'paciente': paciente,
            'dados_do_paciente': dados_do_paciente
        }

        return render(request, 'dados_paciente.html', context)

    elif request.method == 'POST':
        # Dados do paciente:
        peso = request.POST['peso']
        altura = request.POST['altura']
        gordura = request.POST['gordura']
        musculo = request.POST['musculo']

        # Dados laboratoriais:
        hdl = request.POST['hdl']
        ldl = request.POST['ldl']
        colesterol_total = request.POST['ctotal']
        triglicerideos = request.POST['triglicerídeos']

        if not dados_paciente_is_valid(request, peso, altura, gordura, musculo, hdl, ldl, colesterol_total, triglicerideos):
            return redirect(f'/dados_paciente/{paciente.pk} ')

        try:
            dp = DadosPaciente(
                paciente=paciente,
                data=datetime.now(),
                peso=peso,
                altura=altura,
                percentual_gordura=gordura,
                percentual_musculo=musculo,
                colesterol_hdl=hdl,
                colesterol_ldl=ldl,
                colesterol_total=colesterol_total,
                triglicerideos=triglicerideos
            )
            dp.save()

            messages.add_message(
                request=request,
                level=constants.SUCCESS,
                message='Dados cadastrados com sucesso'
            )
            return redirect('/dados_paciente/')

        except:
            messages.add_message(
                request=request,
                level=constants.ERROR,
                message='Erro interno do sistema'
            )
            return redirect('/dados_paciente/')


@login_required(login_url='/auth/logar')
@csrf_exempt
def grafico_paciente(request, id):
    paciente = Paciente.objects.get(id=id)
    dados = DadosPaciente.objects.filter(paciente=paciente).order_by('data')

    pesos = [dado.peso for dado in dados]
    percentual_gordura = [dado.percentual_gordura for dado in dados]
    percentual_musculo = [dado.percentual_musculo for dado in dados]
    labels = list(range(1, len(pesos) + 1))
    data = {
        'peso': pesos,
        'gordura': percentual_gordura,
        'musculo': percentual_musculo,
        'labels': labels
    }
    return JsonResponse(data)

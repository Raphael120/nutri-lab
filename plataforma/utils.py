from django.contrib import messages
from django.contrib.messages import constants

from .models import Paciente


def paciente_is_valid(request, nome, sobrenome, sexo, idade, email, telefone):
    """verifica se o paciente cadastrado é válido"""
    if (len(nome.strip()) == 0) or (len(sobrenome.strip()) == 0) or (len(sexo.strip()) == 0) or (len(idade.strip()) == 0) or (len(email.strip()) == 0) or (len(telefone.strip()) == 0):
        messages.add_message(
            request=request,
            level=constants.ERROR,
            message='Preencha todos os campos'
        )
        return False

    if not str(idade).isnumeric():
        messages.add_message(
            request=request,
            level=constants.ERROR,
            message='Digite uma idade válida'
        )
        return False

    if not str(telefone).isnumeric():
        messages.add_message(
            request=request,
            level=constants.ERROR,
            message='Digite um número de telefone válido'
        )
        return False

    paciente = Paciente.objects.filter(email=email)

    if paciente.exists():
        messages.add_message(
            request=request,
            level=constants.ERROR,
            message='Já existe um paciente com esse E-mail'
        )
        return False

    return True


def dados_paciente_is_valid(request, peso, altura, gordura, musculo, hdl, ldl, colesterol_total, triglicerideos):
    """verifica se os dados do paciente são válidos"""
    if (len(peso.strip()) == 0) or (len(altura.strip()) == 0) or (len(gordura.strip()) == 0) or (len(musculo.strip()) == 0) or (len(hdl.strip()) == 0) or (len(ldl.strip()) == 0) or (len(colesterol_total.strip()) == 0) or (len(triglicerideos.strip()) == 0):
        messages.add_message(
            request=request,
            level=constants.ERROR,
            message='Preencha todos os campos'
        )
        return False

    if not str(peso).isnumeric():
        messages.add_message(
            request=request,
            level=constants.ERROR,
            message='Você inseriu um dado inválido -> Peso'
            
        )
        return False

    if not str(altura).isnumeric():
        messages.add_message(
            request=request,
            level=constants.ERROR,
            message='Você inseriu um dado inválido -> Altura'
        )
        return False

    if not str(gordura).isnumeric():
        messages.add_message(
            request=request,
            level=constants.ERROR,
            message='Você inseriu um dado inválido -> Percentual de gordura'
        )
        return False

    if not str(musculo).isnumeric():
        messages.add_message(
            request=request,
            level=constants.ERROR,
            message='Você inseriu um dado inválido -> Percentual de músculo'
        )
        return False

    if not str(hdl).isnumeric():
        messages.add_message(
            request=request,
            level=constants.ERROR,
            message='Você inseriu um dado inválido -> Colesterol HDL'
        )
        return False

    if not str(ldl).isnumeric():
        messages.add_message(
            request=request,
            level=constants.ERROR,
            message='Você inseriu um dado inválido -> Colesterol LDL'
        )
        return False

    if not str(colesterol_total).isnumeric():
        messages.add_message(
            request=request,
            level=constants.ERROR,
            message='Você inseriu um dado inválido -> Colesterol total'
        )
        return False

    if not str(triglicerideos).isnumeric():
        messages.add_message(
            request=request,
            level=constants.ERROR,
            message='Você inseriu um dado inválido -> Triglicerídeos'
        )
        return False
    
    return True
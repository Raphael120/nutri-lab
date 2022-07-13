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

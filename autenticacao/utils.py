import re

from django.conf import settings
from django.contrib import messages
from django.contrib.messages import constants
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def username_is_valid(request, usuario):
    """verifica se o campo de nome de usuário está vazio"""
    if len(usuario.strip()) == 0:
        messages.add_message(request, constants.ERROR,
                             'O campo "Nome de usuário" está vazio')
        return False

    return True


def email_is_valid(request, email):
    """verifica se o campo e-mail está vazio"""
    if len(email.strip()) == 0:
        messages.add_message(request, constants.ERROR,
                             'O campo "E-mail" está vazio')
        return False

    return True


def password_is_valid(request, senha, confirmar_senha):
    """verifica se a senha é válida."""

    if len(senha.strip()) == 0 or len(confirmar_senha.strip()) == 0:
        messages.add_message(request, constants.ERROR,
                             'Os campos "Senha" e "Confirmar senha" são obrigatórios')

    if len(senha) < 6:
        messages.add_message(request, constants.ERROR,
                             'Sua senha deve conter 6 ou mais caracteres')
        return False

    if not senha == confirmar_senha:
        messages.add_message(request, constants.ERROR,
                             'As senhas não coincidem!')
        return False

    if not re.search('[A-Z]', senha):
        messages.add_message(request, constants.ERROR,
                             'Sua senha não contém letras maiúsculas')
        return False

    if not re.search('[a-z]', senha):
        messages.add_message(request, constants.ERROR,
                             'Sua senha não contém letras minúsculas')
        return False

    if not re.search('[0-9]', senha):
        messages.add_message(request, constants.ERROR,
                             'Sua senha não contém números')
        return False

    return True


def email_html(path_template: str, assunto: str, para: list, **kwargs) -> dict:
    """função para enviar e-mail"""
    html_content = render_to_string(path_template, kwargs)
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        assunto, text_content, settings.EMAIL_HOST_USER, para)

    email.attach_alternative(html_content, 'text/html')
    email.send()
    return{'status': 1}

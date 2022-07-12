from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Paciente(models.Model):
    choices_sexo = (
        ('F', 'Feminino'),
        ('M', 'Masculino')
    )

    nome = models.CharField(max_length=50)
    sobrenome = models.CharField(max_length=50)
    sexo = models.CharField(max_length=1, choices=choices_sexo)
    idade = models.IntegerField()
    email = models.EmailField()
    telefone = models.CharField(max_length=19)
    nutricionista = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.nome} {self.sobrenome}'

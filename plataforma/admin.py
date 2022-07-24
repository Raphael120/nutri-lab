from django.contrib import admin

from .models import DadosPaciente, Opcao, Paciente, Refeicao

# Register your models here.

admin.site.register(Paciente)
admin.site.register(DadosPaciente)
admin.site.register(Refeicao)
admin.site.register(Opcao)

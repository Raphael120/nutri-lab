from django.contrib import admin

from .models import DadosPaciente, Paciente

# Register your models here.

admin.site.register(Paciente)
admin.site.register(DadosPaciente)

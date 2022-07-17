from django.urls import path
from . import views

urlpatterns = [
    path('pacientes/', views.pacientes, name='pacientes'),
    path('dados_paciente/', views.listar_dados_paciente, name='listar_dados_paciente'),
    path('dados_paciente/<str:id>/', views.dados_paciente, name='dados_paciente'),
    path('grafico_paciente/<str:id>/', views.grafico_paciente, name='grafico_paciente')
]

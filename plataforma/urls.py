from django.urls import path
from . import views

urlpatterns = [
    path('pacientes/', views.pacientes, name='pacientes'),
    path('dados_paciente/', views.listar_dados_paciente, name='listar_dados_paciente'),
    path('dados_paciente/<str:id>/', views.dados_paciente, name='dados_paciente'),
    path('grafico_paciente/<str:id>/', views.grafico_paciente, name='grafico_paciente'),
    path('plano_alimentar/', views.listar_plano_alimentar, name='listar_plano_alimentar'),
    path('plano_alimentar/<str:id>/', views.plano_alimentar, name='plano_alimentar'),
    path('refeicao/<str:id_paciente>/', views.refeicao, name='refeicao'),
    path('opcao/<str:id_paciente>/', views.opcao, name='opcao')
]

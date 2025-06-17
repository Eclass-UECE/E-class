from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.paginaProfessor, name='pagProf'),
    path('diario/', views.diario, name='diario'),
    path('midTerm/<int:id_turma>', views.midTerm, name='midTerm'),
    path('finalExam/<int:id_turma>', views.finalExam, name='finalExam'),
    path('media/', views.media, name='media'),
    path('notas/<int:id_turma>', views.notas, name='notas'),
    path('aulas/<int:id_turma>', views.aulas, name='aulas'), 
    path('aulas/<int:id_turma>/frequencia/', views.frequencia, name='frequencia'),
    path('entregaDiario/', views.entregaDiario, name='entregaDiario'),
    path('aulas/editar_aula/', views.editar_aula, name='editar_aula'),
    path('aulas/excluir_aula/', views.excluir_aula, name='excluir_aula'),
    path('aulas/salvar_faltas/', views.salvar_faltas, name='salvar_faltas'),


    # path('adicionar_aula/<int:id_turma>',views.adicionar_aula, name='adicionar_aula'),
]   
from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.paginaProfessor, name='pagProf'),
    path('diario/', views.diario, name='diario'),
    path('midTerm/', views.midTerm, name='midTerm'),
    path('finalExam/', views.finalExam, name='finalExam'),
    path('media/', views.media, name='media'),
    path('notas/', views.notas, name='notas'),
    path('aulas/<int:id_turma>', views.aulas, name='aulas'), 
    path('frequencia/', views.frequencia, name='frequencia'),
    path('entregaDiario/', views.entregaDiario, name='entregaDiario'),
    path('editar_aula/<int:id_turma>/<int:id_aulas>', views.editar_aula, name='editar_aula'),
    path('excluir/<int:id_turma>/<int:id_aulas>', views.excluir_aula, name='excluir_aula'),

    # path('adicionar_aula/<int:id_turma>',views.adicionar_aula, name='adicionar_aula'),
]   
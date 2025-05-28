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
    path('aulas/', views.aulas, name='aulas'),
    path('frequencia/', views.frequencia, name='frequencia'),
    path('entregaDiario/', views.entregaDiario, name='entregaDiario'),
]
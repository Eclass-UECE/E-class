from django.urls import path
from . import views

urlpatterns = [
    path('', views.paginaProfessor, name='pagProf'),
    path('diario/', views.diario, name='diario'),
    path('midTerm/', views.midTerm, name='midTerm'),
    path('aulas/', views.aulas, name='aulas'),
    path('frequencia/', views.frequencia, name='frequencia'),
    path('adicionar_aula/',views.adicionar_aula, name='adicionar_aula'),
]   
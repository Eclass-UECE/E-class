from django.shortcuts import render
from preLogin.models import *

def paginaProfessor(request):
    return render(request, 'prof/pagProf.html')

def diario(request):
    return render(request, 'prof/diario.html')

def midTerm(request):
    return render(request, 'prof/provas/midTerm.html')

def aulas(request):
    # Dados fictícios 
    lista_aulas = [
        {'data': '2025-05-10', 'conteudo': 'Introdução ao Django', 'duracao': '1h30'},
        {'data': '2025-05-11', 'conteudo': 'Modelos e Migrations', 'duracao': '2h00'},
        {'data': '2025-05-12', 'conteudo': 'Templates e Views', 'duracao': '1h45'},
    ] # Mudar isso para dados do banco
    
    return render(request, 'prof/aulas/aulas.html', {'aulas': lista_aulas})

def frequencia(request):
    return render(request, 'prof/aulas/frequencia.html')

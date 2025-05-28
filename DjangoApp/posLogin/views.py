from django.shortcuts import render
from collections import defaultdict

def paginaProfessor(request):
    return render(request, 'prof/pagProf.html')

def diario(request):
    return render(request, 'prof/diario.html')

def aulas(request):
    return render(request, 'prof/aulas/aulas.html')

def frequencia(request):
    return render(request, 'prof/aulas/frequencia.html')

def midTerm(request):
    return render(request, 'prof/provas/midTerm.html')

def finalExam(request):
    return render(request, 'prof/provas/finalExam.html')

def media(request):
    return render(request, 'prof/provas/media.html')

def notas(request):
    return render(request, 'prof/provas/notas.html')

def entregaDiario(request):
    return render(request, 'prof/entregaDiario.html')
from django.shortcuts import render,get_object_or_404
from collections import defaultdict
from django.shortcuts import render,get_object_or_404
from preLogin.models import *

def paginaProfessor(request):
    return render(request, 'prof/pagProf.html')

def diario(request):
    professor = request.session.get('professor_nome_completo')
    print(professor)

    professor_turmas = Turmas.objects.filter(professor__nome_completo=professor)
    print(professor_turmas)
    return render(request, 'prof/diario.html', {'professor': professor, 'turmas': professor_turmas})

def aulas(request):
    aulas = Aulas.objects.all().order_by('-data')
    return render(request, 'prof/aulas/aulas.html',{'aulas': aulas})


def adicionar_aula(request):
     if request.method == 'POST':
        data = request.POST.get('data')
        conteudo = request.POST.get('conteudo')
        Aulas.objects.create(data=data, conteudo=conteudo, turma=turma)

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
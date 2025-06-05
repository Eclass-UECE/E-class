import datetime
from django.contrib import messages
from django.shortcuts import redirect, render,get_object_or_404
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

def aulas(request, id_turma):
    print(id_turma)
    turma = get_object_or_404(Turmas, id_turma=id_turma)
    aula = Aulas.objects.filter(turma_id=id_turma).order_by('-data')
    print(aula)

    if request.method == 'POST':
        data = request.POST.get('data')
        data_formatada = datetime.datetime.strptime(data, '%Y-%m-%d').strftime('%d/%m/%Y')
    
        conteudo = request.POST.get('conteudo')
        observação = request.POST.get('observação')
        turma = get_object_or_404(Turmas, id_turma=id_turma)

        observacao = Aulas.objects.filter(turma_id=id_turma).order_by('-data')

        if not Aulas.objects.filter(data=data, turma=turma).exists():
            Aulas.objects.create(
                data=data, 
                conteudo=conteudo, 
                objetivos=observação, 
                turma=turma
        ) 
            messages.success(request, f"Aula do dia {data_formatada} cadastrada com sucesso!")
        else:
            messages.error(request, f"Já existe uma aula cadastrada para o dia {data_formatada}.")

         
        # REDIRECIONAMENTO para evitar reenvio se o usuário atualizar
        return redirect('aulas', id_turma=id_turma)
  
    return render(request, 'prof/aulas/aulas.html', {'turma': turma, 'aulas': aula})

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

def editar_aula(request, id_turma, id_aulas):
    aula = get_object_or_404(Aulas, pk=id_aulas, turma_id=id_turma)

    if request.method == 'POST':
        aula.data = request.POST.get('data')
        aula.objetivos = request.POST.get('observação')
        aula.save()
        return redirect('aulas', id_turma=id_turma)

def excluir_aula(request, id):
    aula = get_object_or_404(Aulas, id=id)
    turma_id = aula.turma.id_turma  # pegamos o ID da turma para redirecionar depois

    if request.method == 'POST':
        aula.delete()
        messages.success(request, "Aula excluída com sucesso.")
    
    return redirect('aulas', id_turma=turma_id)

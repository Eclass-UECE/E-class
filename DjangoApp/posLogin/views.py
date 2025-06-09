import datetime
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
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

@csrf_exempt  # Use @csrf_exempt só para testes, o ideal é passar o token CSRF via JS
def editar_aula(request):
    if request.method == "POST":
        data = json.loads(request.body)
        id_aula = data.get('id')
        nova_data = data.get('data')
        novo_valor = data.get('valor')
        tabela = data.get('tabela')

        # Converte string data para datetime
        nova_data_obj = datetime.strptime(nova_data, "%Y-%m-%d").date()

        try:
            aula = Aulas.objects.get(id=id_aula)
            aula.data = nova_data_obj
            if tabela == 1:
                aula.conteudo = novo_valor
            else:
                aula.objetivos = novo_valor
            aula.save()

            data_formatada = aula.data.strftime("%-d de %B de %Y")  # formato que você usa no template

            return JsonResponse({
                "status": "sucesso",
                "data_formatada": data_formatada,
                "valor": novo_valor
            })

        except Aulas.DoesNotExist:
            return JsonResponse({"status": "erro", "mensagem": "Aula não encontrada."}, status=404)

    return JsonResponse({"status": "erro", "mensagem": "Método inválido."}, status=405)


def excluir_aula(request, id):
    aula = get_object_or_404(Aulas, id=id)
    turma_id = aula.turma.id_turma  # pegamos o ID da turma para redirecionar depois

    if request.method == 'POST':
        aula.delete()
        messages.success(request, "Aula excluída com sucesso.")
    
    return redirect('aulas', id_turma=turma_id)

from collections import defaultdict
import calendar
import datetime
import json
import locale
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.shortcuts import redirect, render,get_object_or_404
from collections import defaultdict
from django.shortcuts import render,get_object_or_404
from preLogin.models import *


def paginaProfessor(request):
    return render(request, 'prof/professor/pagProf.html')

def diario(request):
    professor = request.session.get('professor_nome_completo')
    # print(professor)

    professor_turmas = Turmas.objects.filter(professor__nome_completo=professor)
    print(professor_turmas)
    
    return render(request, 'prof/professor/diario.html', {'professor': professor, 'turmas': professor_turmas})

def aulas(request, id_turma):
    # print(id_turma)
    turma = get_object_or_404(Turmas, id_turma=id_turma)
    aula = Aulas.objects.filter(turma_id=id_turma).order_by('-data')
    # print(aula)

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

def frequencia(request, id_turma):
    turma = get_object_or_404(Turmas, id_turma=id_turma)
    alunos_turma = Alunos.objects.filter(turma_id = turma).order_by('matricula')
    aulas_turma = Aulas.objects.filter(turma_id = turma)
    frequencias = Frequencia.objects.filter(turma_id=turma).order_by('aluno_id')

    print(frequencias)
    
    aulas_por_mes = defaultdict(list)
    for aula in aulas_turma:
        key = aula.data.strftime('%Y-%m')  # Ex: '2025-06'
        aulas_por_mes[key].append(aula)

    # Agrupar por mês/ano
    aulas_agrupadas = []

    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

    for key in sorted(aulas_por_mes):  # <- Aqui sorted está sendo chamado corretamente
        ano, mes = key.split('-')
        nome_mes = calendar.month_name[int(mes)].capitalize()
        aulas_agrupadas.append({
            'mes': nome_mes,
            'ano': ano,
            'dias': aulas_por_mes[key],
        })

    presencas_dict = {
        f"{f.aluno.matricula}_{f.aula.id_aulas}": f.falta for f in frequencias
}   
    for k, v in presencas_dict.items():
        
        print(f"Chave gerada: {k} -> Valor: {v}")
    for aluno in alunos_turma:
        aluno.falta = presencas_dict.get(str(aluno.matricula), 0)
        print("ALUNO TESTE", aluno, aula.id_aulas, aluno.falta)
        
    context = {
        'turma': turma,
        'alunos': alunos_turma,
        'aulas': aulas_turma,
        'aulas_agrupadas': aulas_agrupadas,
        'presencas_dict': presencas_dict,
        'frequencias': frequencias
    }
    
    print("turma atual", alunos_turma)

    return render(request, 'prof/aulas/frequencia.html', context)

@csrf_exempt
def salvar_faltas(request):
    if request.method == "POST":
        body = json.loads(request.body)
        presencas = body.get("dados", [])

        for p in presencas:

            aluno_id = p.get("aluno_id")
            aula_id = p.get("aula_id")
            id_turma = p.get("id_turma")
            count_faltas = p.get("total_faltas")
            falta = p.get("falta")  
            print(count_faltas)
            registro = Frequencia.objects.filter(aluno_id=aluno_id, aula_id=aula_id)

            # Verifica se há registro do aluno naquela turma
        
            if registro.exists():
                    x = Frequencia.objects.get(aluno_id=aluno_id, aula_id=aula_id)
                    Frequencia.objects.update_or_create(
                        aluno_id=aluno_id,
                        turma_id=id_turma,
                        aula_id=aula_id,
                        defaults={
                            'falta': falta,
                        }
                    )
            else:
                    Frequencia.objects.update_or_create(
                        aluno_id=aluno_id,
                        turma_id=id_turma,
                        aula_id=aula_id,
                        defaults={
                            'falta': falta,
                        }
                    )
     
        return JsonResponse({"status": "ok"})

    return JsonResponse({"error": "método inválido"}, status=405)

def midTerm(request, id_turma):
    turma = get_object_or_404(Turmas, id_turma=id_turma)
    prova = Provas.objects.filter(turma_id=id_turma, etapa="Mid Term").order_by('-data')

    if request.method == 'POST':
        data = request.POST.get('data')
        data_formatada = datetime.datetime.strptime(data, '%Y-%m-%d').strftime('%d/%m/%Y')
        tipo = request.POST.get('avaliação')
        etapa = request.POST.get('etapa')
        turma = get_object_or_404(Turmas, id_turma=id_turma)

        if not Provas.objects.filter(tipo=tipo, turma=turma, etapa=etapa).exists():
            Provas.objects.create(
                data=data, 
                tipo=tipo, 
                turma=turma,
                etapa=etapa
        ) 
            messages.success(request, f"Prova de {tipo} cadastrada com sucesso!")
        else:
            messages.error(request, f"A prova de {tipo} já existe!")

         
        # REDIRECIONAMENTO para evitar reenvio se o usuário atualizar
        return redirect('midTerm', id_turma=id_turma)
  
    return render(request, 'prof/provas/midTerm.html', {'turma': turma, 'provas': prova})
    
def finalExam(request, id_turma):
    turma = get_object_or_404(Turmas, id_turma=id_turma)
    prova = Provas.objects.filter(turma_id=id_turma, etapa="Final Exam").order_by('-data')

    if request.method == 'POST':
        data = request.POST.get('data')
        data_formatada = datetime.datetime.strptime(data, '%Y-%m-%d').strftime('%d/%m/%Y')
        tipo = request.POST.get('avaliação')
        etapa = request.POST.get('etapa')
        turma = get_object_or_404(Turmas, id_turma=id_turma)

        if not Provas.objects.filter(tipo=tipo, turma=turma, etapa=etapa).exists():
            Provas.objects.create(
                data=data, 
                tipo=tipo, 
                turma=turma,
                etapa=etapa
        ) 
            messages.success(request, f"Prova de {tipo} cadastrada com sucesso!")
        else:
            messages.error(request, f"A prova de {tipo} já existe!")

         
        # REDIRECIONAMENTO para evitar reenvio se o usuário atualizar
        return redirect('finalExam', id_turma=id_turma)
  
    return render(request, 'prof/provas/finalExam.html', {'turma': turma, 'provas': prova})

def media(request):
    return render(request, 'prof/provas/media.html')

def notas(request, id_turma, etapa, prova_id):
    print(etapa)
    turma = get_object_or_404(Turmas, id_turma=id_turma)
    alunos_turma = Alunos.objects.filter(turma_id = turma).order_by('matricula')
    prova = Provas.objects.get(turma_id=turma, etapa=etapa, id_prova=prova_id)
    alunos_prova = AlunosProvas.objects.filter(turma_id=turma, prova_id=prova_id).order_by('-aluno_id')

    alunos_provas_dict = {aluno.aluno_id: aluno.nota for aluno in alunos_prova}

    print(turma)
    return render(request, 'prof/provas/notas.html', {'turma': turma, 'alunos_turma': alunos_turma, 
                                              'provas': prova, 'alunos_provas_dicts': alunos_provas_dict})

@csrf_exempt
def salvar_nota(request):
     if request.method == "POST":
        body = json.loads(request.body)
        presencas = body.get("dados", [])

        for p in presencas:

            nota_str = p.get("nota")
            aluno_id = p.get("aluno_id")
            prova_id = p.get("prova_id")
            turma_id = p.get("turma_id")
            print('aluno',aluno_id)
            print('prova',prova_id)
            print('turma',turma_id)

            nota_str = nota_str.replace(',', '.')  # troca vírgula por ponto
            nota = float(nota_str) 
            
            registro = AlunosProvas.objects.filter(aluno_id=aluno_id, turma_id=turma_id)

            # Verifica se há registro do aluno naquela turma
        
            if registro.exists():
                    AlunosProvas.objects.update_or_create(
                        aluno_id=aluno_id,
                        turma_id=turma_id,
                        prova_id=prova_id,
                        defaults={
                            'nota': nota,
                        }
                    )
            else:
                    AlunosProvas.objects.update_or_create(
                        aluno_id=aluno_id,
                        turma_id=turma_id,
                        prova_id=prova_id,
                        defaults={
                            'nota': nota,
                        }
                    )

                   
        return JsonResponse({"status": "ok"})

     return JsonResponse({"error": "método inválido"}, status=405)

def entregaDiario(request):
    return render(request, 'prof/professor/entregaDiario.html')

@csrf_exempt
def editar_aula(request):
    if request.method == "POST":
        try:
            dados = json.loads(request.body)
            id_aulas = dados.get("id_aulas")
            nova_data = dados.get("data")
            novo_valor = dados.get("linhaX")
            campo = dados.get('campo')
            
            aula = Aulas.objects.get(id_aulas=id_aulas)
            aula.data = nova_data
            if campo == 'conteudo':
                aula.conteudo = novo_valor
            elif campo == 'objetivos':
                aula.objetivos = novo_valor
            else:
                return JsonResponse({'erro': 'Campo inválido'}, status=400)
            aula.save()

            return JsonResponse({"status": "ok"})
        except Exception as e:
            return JsonResponse({"status": "erro", "mensagem": str(e)}, status=400)
    return JsonResponse({"erro": "Método não permitido"}, status=405)

@csrf_exempt
def excluir_aula(request):
    if request.method == 'POST':
        try:
            dados = json.loads(request.body)
            id_aulas = dados.get("id_aulas")
                   
            aula = Aulas.objects.get(id_aulas=id_aulas)
            aula.delete()
            
            return JsonResponse({"status": "ok"})
        except Exception as e:
            return JsonResponse({"status": "erro", "mensagem": str(e)}, status=400)
    return JsonResponse({"erro": "Método não permitido"}, status=405)

@csrf_exempt
def excluir_prova(request):
    if request.method == 'POST':
        try:
            dados = json.loads(request.body)
            id_prova = dados.get("id_prova")
                   
            prova = Provas.objects.get(id_prova=id_prova)
            prova.delete()
            
            return JsonResponse({"status": "ok"})
        except Exception as e:
            return JsonResponse({"status": "erro", "mensagem": str(e)}, status=400)
    return JsonResponse({"erro": "Método não permitido"}, status=405)

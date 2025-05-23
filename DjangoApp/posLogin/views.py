from django.shortcuts import render, redirect
from preLogin.models import Alunos, Turmas, Aulas, Frequencia
from django.utils.dateparse import parse_date
from collections import defaultdict
from calendar import month_name

def paginaProfessor(request):
    return render(request, 'prof/pagProf.html')

def diario(request):
    return render(request, 'prof/diario.html')

def midTerm(request):
    return render(request, 'prof/provas/midTerm.html')

def aulas(request):
    lista_aulas = Aulas.objects.all()
    return render(request, 'prof/aulas/aulas.html', {'aulas': lista_aulas})

def frequencia(request, id_turma):
    turma = Turmas.objects.get(id_turma=id_turma)
    alunos = Alunos.objects.filter(turma=turma).order_by('nome_completo')
    aulas = Aulas.objects.filter(turma=turma).order_by('data')

    if request.method == 'POST':
        data_aula = request.POST.get('data')
        aula, created = Aulas.objects.get_or_create(
            turma=turma,
            data=parse_date(data_aula),
            defaults={'conteudo': '', 'objetivos': ''}
        )

        for aluno in alunos:
            presenca_key = f'presenca_{aluno.matricula}'
            presenca = request.POST.get(presenca_key) == '1'
            Frequencia.objects.update_or_create(
                aluno=aluno,
                aula=aula,
                defaults={'presenca': presenca}
            )
        return redirect('frequencia', id_turma=turma.id_turma)

    # Organizar aulas por mês e dia
    meses = []
    dias_por_mes = defaultdict(list)
    for aula in aulas:
        mes_nome = month_name[aula.data.month]
        if mes_nome not in meses:
            meses.append(mes_nome)
        dias_por_mes[mes_nome].append(aula)

    # Organizar presença por aluno e aula
    presencas = {}
    faltas_por_aluno = defaultdict(int)

    for aluno in alunos:
        presencas[aluno.matricula] = {}
        for aula in aulas:
            freq = Frequencia.objects.filter(aluno=aluno, aula=aula).first()
            presencas[aluno.matricula][aula.id_aulas] = freq.presenca if freq else False
            if freq and not freq.presenca:
                faltas_por_aluno[aluno.matricula] += 1
            elif not freq:
                faltas_por_aluno[aluno.matricula] += 1

    context = {
        'turma': turma,
        'alunos': alunos,
        'aulas': aulas,
        'meses': meses,
        'dias_por_mes': dias_por_mes,
        'presencas': presencas,
        'faltas_por_aluno': faltas_por_aluno,
    }

    return render(request, 'prof/frequencia.html', context)
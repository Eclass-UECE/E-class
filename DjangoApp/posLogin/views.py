from django.shortcuts import render

def paginaProfessor(request):
    return render(request, 'prof/pagProf.html')

def diario(request):
    return render(request, 'prof/diario.html')

def midTerm(request):
    return render(request, 'prof/provas/midTerm.html')


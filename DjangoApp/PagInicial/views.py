from django.shortcuts import render
from django.http import HttpResponse

def pag_inicial(request):
    return render(request,'PagInicial/pag_inicial.html')
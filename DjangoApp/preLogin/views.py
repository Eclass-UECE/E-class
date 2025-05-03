from django.shortcuts import render
from django.http import HttpResponse

def pagInicial(request):
    return render(request, 'preLogin/pagInicial.html')

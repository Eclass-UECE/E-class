from django.shortcuts import render

def pagInicial(request):
    return render(request, 'preLogin/pagInicial.html')

from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from preLogin.models import *
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponse

def login_view(request):
    if request.method == 'POST':
        matricula = request.POST.get('matricula')
        senha = request.POST.get('senha')
                
         # Validar diretamente no banco de dados
        try:
            # Verifica se o usuário existe no banco

            user = get_object_or_404(Professores, matricula=matricula)
            print("prof", user)
          
            # Checa a senha diretamente
            print('bd= ', user.senha)
            print('form= ', senha)
            print('acess=' ,user.primeiro_acesso)

            if user.primeiro_acesso is None:
               return HttpResponse("Primeiro Acesso! Redefina sua senha para prosseguir.")

            if user.senha==senha:
                print('correto')
                return HttpResponse(f"Usuário {user.nome_completo} autenticado com sucesso!")
            else:
                print('senha errada')
                return HttpResponse("Senha incorreta.")
        except Professores.DoesNotExist:
            print('execao')
            return HttpResponse("Usuário não encontrado.")
        
    return render(request, 'Login/pagLogin.html')


from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from preLogin.models import *
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages


def login_view(request):
    if request.method == 'POST':
        matricula = request.POST.get('matricula')
        senha = request.POST.get('senha')
                
        # Validar diretamente no banco de dados
        # Verifica se o usuário existe no banco
        user = Professores.objects.filter(matricula=matricula).exists()
          
        # Checa a senha diretamente no banco
        if user:
            user = Professores.objects.get(matricula=matricula)

            if user.primeiro_acesso is True:
                messages.success(request, "Primeiro acesso detectado. Redefina sua senha clicando no botão 'Esqueci a senha' e tente acessar novamente!")
            
            elif user.senha==senha:
                request.session['professor_nome_completo'] = user.nome_completo
                return render(request, 'prof/professor/pagProf.html')
            else:
                messages.success(request, "Senha incorreta! Tente novamente.")

        else:
            messages.success(request, "Usuário não cadastrado no sistema.")
        
    return render(request, 'Login/pagLogin.html')


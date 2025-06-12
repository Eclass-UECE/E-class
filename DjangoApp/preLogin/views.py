from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import InscricaoForm, TestedenivelForm
from .models import Inscricao, AnexosInscricao
import os
import pickle
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect

class CustomPasswordResetView(PasswordResetView):
    template_name = 'preLogin/password_reset.html'
    success_url = reverse_lazy('password_reset_done')
    email_template_name = 'preLogin/password_reset_email.html'
    
    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        if not User.objects.filter(email=email).exists():
            messages.error(request, "Este e-mail não está registrado.")
            return redirect('password_reset')
        return super().post(request, *args, **kwargs)


def pagInicial(request):
    return render(request, 'preLogin/pagInicial.html')

def inscricao_view(request):
    if request.method == 'POST':
        inscricao_form = InscricaoForm(request.POST, request.FILES)

        if inscricao_form.is_valid():
            inscricao = inscricao_form.save()
            return HttpResponseRedirect(reverse('anexos', kwargs={'inscricao_id': inscricao.pk}))

    else:
        inscricao_form = InscricaoForm()

    return render(request, 'preLogin/Inscricao/inscricao.html', {
        'inscricao_form': inscricao_form,
    })

def anexos_view(request, inscricao_id):
    inscricao = get_object_or_404(Inscricao, id_inscricao=inscricao_id)
    
    if request.method == 'POST':
        files = request.FILES.getlist('arquivo')
        
        if files:
            for file in files:
                AnexosInscricao.objects.create(
                    inscricao=inscricao,
                    arquivo=file
                )
            anexos_existentes = AnexosInscricao.objects.filter(inscricao=inscricao)

            if Inscricao.turma_entrada == 'testenivel':
                return render(request, 'preLogin/Inscricao/anexos.html', {
                    'inscricao': inscricao,
                    'anexos_existentes': anexos_existentes,
                    'teste_nivel_condicao': 'teste_de_nivel',
                    'mensagem_sucesso': f'{len(files)} arquivo(s) enviado(s) com sucesso!'
                })
            
            else:
                return render(request, 'preLogin/Inscricao/anexos.html', {
                    'inscricao': inscricao,
                    'anexos_existentes': anexos_existentes,
                    'teste_nivel_condicao': 'pagina_de_sucesso',
                    'mensagem_sucesso': f'{len(files)} arquivo(s) enviado(s) com sucesso!'
                })
    
    anexos_existentes = AnexosInscricao.objects.filter(inscricao=inscricao)
    return render(request, 'preLogin/Inscricao/anexos.html', {
        'inscricao': inscricao,
        'anexos_existentes': anexos_existentes
    })


def testedenivel_view(request, inscricao_id):
    inscricao = get_object_or_404(Inscricao, id_inscricao=inscricao_id)
    
    if request.method == 'POST':
        testenivel_form = TestedenivelForm(request.POST, instance=inscricao)
        
        if testenivel_form.is_valid():
            testenivel_form.save()
            return HttpResponseRedirect(reverse('pagina_de_sucesso', kwargs={'inscricao_id': inscricao.id_inscricao}))
    else:
        testenivel_form = TestedenivelForm(instance=inscricao)
    
    return render(request, 'preLogin/Inscricao/teste_de_nivel.html', {
        'inscricao': inscricao,
        'form': testenivel_form  # Note que mudei o nome para 'form' para ficar mais genérico
    })

def sucesso_view(request, inscricao_id):
    inscricao = get_object_or_404(Inscricao, id_inscricao=inscricao_id)
    return render(request, 'preLogin/Inscricao/pagina_de_sucesso.html', {
        'inscricao': inscricao
    })

@csrf_exempt
def coordenador_view(request):
    if request.method == 'POST':
        turmas_selecionadas = request.POST.getlist('turmas')
        
        # Verifica se há turmas selecionadas
        if not turmas_selecionadas:
            return render(request, 'preLogin/coordenador.html', {
                'mensagem_erro': 'Selecione pelo menos uma turma!'
            })

        caminho_arquivo = os.path.join(settings.BASE_DIR, 'turmas_escolhidas.pkl')
        with open(caminho_arquivo, 'wb') as f:
            pickle.dump(turmas_selecionadas, f)

        return render(request, 'preLogin/coordenador.html', {
            'mensagem': 'Turmas salvas com sucesso!',
            'turmas_salvas': turmas_selecionadas
        })

    return render(request, 'preLogin/coordenador.html')

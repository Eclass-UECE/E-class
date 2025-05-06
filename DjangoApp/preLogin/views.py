from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .forms import InscricaoForm, TesteDeNivelForm
from django.urls import reverse
from .models import Inscricao, AnexosInscricao

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
    inscricao = get_object_or_404(Inscricao, cpf=inscricao_id)
    
    if request.method == 'POST':
        files = request.FILES.getlist('arquivo')
        
        if files:
            for file in files:
                AnexosInscricao.objects.create(
                    inscricao=inscricao,
                    arquivo=file
                )
            
            # Mantém o usuário na mesma página com mensagem de sucesso
            anexos_existentes = AnexosInscricao.objects.filter(inscricao=inscricao)
            return render(request, 'preLogin/Inscricao/anexos.html', {
                'inscricao': inscricao,
                'anexos_existentes': anexos_existentes,
                'mensagem_sucesso': f'{len(files)} arquivo(s) enviado(s) com sucesso!'
            })
    
    anexos_existentes = AnexosInscricao.objects.filter(inscricao=inscricao)
    return render(request, 'preLogin/Inscricao/anexos.html', {
        'inscricao': inscricao,
        'anexos_existentes': anexos_existentes
    })

def sucesso_view(request, inscricao_id):
    inscricao = get_object_or_404(Inscricao, cpf=inscricao_id)
    return render(request, 'preLogin/Inscricao/pagina_de_sucesso.html', {
        'inscricao': inscricao
    })

def testedenivel(request, inscricao_id):
    inscricao = get_object_or_404(Inscricao, cpf=inscricao_id)

    if request.method == 'POST':
        testedenivelForm = TesteDeNivelForm(request.POST)

        turma = request.POST.get('turma_teste_de_nivel')

        if testedenivelForm.is_valid():
            inscricao.teste_de_nivel = True
            inscricao.turma_teste_de_nivel = turma
            inscricao.turma_entrada = 'Teste_Nivel'
            inscricao.save()

            # Aqui renderiza a mensagem de sucesso na mesma página, sem redirecionar
            return render(request, 'preLogin/Inscricao/testedenivel.html', {
                'inscricao': inscricao,
                'form': TesteDeNivelForm(),  # formulário limpo após envio
                'mensagem': 'Inscrição e Pedido de teste de nível enviados com sucesso'
            })
    else:
        testedenivelForm = TesteDeNivelForm()

    return render(request, 'preLogin/Inscricao/testedenivel.html', {
        'inscricao': inscricao,
        'form': testedenivelForm
    })


            

        

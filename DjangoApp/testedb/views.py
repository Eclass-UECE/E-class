from django.shortcuts import render, redirect
from .models import Inscricao, AnexosInscricao
from .forms import InscricaoForm, MultiFileForm

# views.py

def upload_files(request, inscrição_id):
    teste =  Inscricao.objects.get(pk=inscrição_id)

    if request.method == "POST":
        form = MultiFileForm(request.POST, request.FILES)
        if form.is_valid():
            files = form.cleaned_data["arquivo"]
            for file in files:
                AnexosInscricao.objects.create(teste=teste, file=file)

def thanks(request):
    return render(request, "teste/thanks.html")


def teste(request):
    if request.method == 'POST':
        form = InscricaoForm(request.POST)
        file_form = MultiFileForm(request.POST, request.FILES)

        if form.is_valid() and file_form.is_valid():
            inscricao = form.save()

            arquivos = request.FILES.getlist('arquivos')
            for arquivo in arquivos:
                AnexosInscricao.objects.create(inscricao=inscricao, arquivo=arquivo)

            return redirect('thanks')
    else:
        form = InscricaoForm()
        file_form = MultiFileForm()

    return render(request, 'teste/teste.html', {'form': form, 'file_form': file_form})

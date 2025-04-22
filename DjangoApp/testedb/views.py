from django.http import HttpResponse
from django.template import loader
from .models import alunos, professores
from .forms import inscricao

def teste(request):
  template = loader.get_template('teste/teste.html')
  
  alunoss = alunos.objects.all().values()
  professoress = professores.objects.all().values()

  context ={
    'alunos': alunoss,
    'professores': professoress,
    'form': inscricao
  }
  return HttpResponse(template.render(context,request))
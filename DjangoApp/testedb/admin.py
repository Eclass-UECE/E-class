from django.contrib import admin
from .models import Alunos, Professores, Coordenadores, Inscricao, Turmas, Provas, AnexosInscricao, AlunosProvas, Aulas, Frequencia, DadosBancarios
# Register your models here.

admin.site.register(Inscricao)
admin.site.register(Alunos)
admin.site.register(Professores)
admin.site.register(Coordenadores)
admin.site.register(Turmas)
admin.site.register(Provas)
admin.site.register(AnexosInscricao)
admin.site.register(AlunosProvas)
admin.site.register(Aulas)
admin.site.register(Frequencia)
admin.site.register(DadosBancarios)
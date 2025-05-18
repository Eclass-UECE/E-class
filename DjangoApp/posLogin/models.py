from django.db import models

class Aula(models.Model):
    data = models.DateField()
    conteudo = models.TextField()
    duracao = models.IntegerField()
    #loucura

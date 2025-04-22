from django.db import models

class alunos(models.Model):
  nome = models.CharField(max_length=255)
  sobrenome = models.CharField(max_length=255)
  idade = models.IntegerField(null= True)

class professores(models.Model):
  nome = models.CharField(max_length=255)
  sobrenome = models.CharField(max_length=255)
  idade = models.IntegerField(null= True)

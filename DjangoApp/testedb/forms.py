from django import forms

class inscricao(forms.Form):
    nome = forms.CharField(max_length=255)
    sobrenome = forms.CharField(max_length=255)
    idade = forms.IntegerField(help_text = "Digite sua idade")


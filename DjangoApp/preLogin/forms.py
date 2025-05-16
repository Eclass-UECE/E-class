from django import forms
from .models import Inscricao, AnexosInscricao

class InscricaoForm(forms.ModelForm):

    dt_nasc = forms.DateField(
        label='Data de nascimento',
        input_formats=['%d/%m/%Y'],
        widget=forms.DateInput(
            attrs={
                'placeholder': '01/01/2000',
                'id': 'campo-data',
                'type': 'text'
            }
        )
    )

    

    telefone = forms.CharField(
        label='Telefone',
        max_length=12,
        widget=forms.TextInput(attrs={
            'placeholder': '11 912345678',
            'id': 'campo-telefone'
        })
    )

    email = forms.CharField(
        label='Email',
        widget=forms.TextInput(attrs={
            'placeholder': 'email@gmail.com',
            'id': 'campo-email'
        })
    )


    class Meta:
        model = Inscricao
        fields = '__all__'

    cpf = forms.CharField(
        label='CPF',
        max_length=14,
        widget=forms.TextInput(attrs={
            'placeholder': '123.456.789-00',
            'id': 'campo-cpf'
        })
    )

class MultiFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultiFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultiFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class AnexosForm(forms.ModelForm):
    arquivo = MultiFileField(label='Selecione os arquivos', required=False)
    
    class Meta:
        model = AnexosInscricao
        fields = ['arquivo']
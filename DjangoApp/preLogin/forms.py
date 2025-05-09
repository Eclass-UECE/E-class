from django import forms
from .models import Inscricao, AnexosInscricao

class InscricaoForm(forms.ModelForm):
    dt_nasc = forms.CharField(
        label='Data de Nascimento',
        max_length=10,
        widget=forms.TextInput(attrs={
            'placeholder': 'dd/mm/aaaa',
            'id': 'campo-data'
        })
    )

    telefone = forms.CharField(
        label='Telefone',
        max_length=15,
        widget=forms.TextInput(attrs={
            'placeholder': '11 91234 5678',
            'id': 'campo-telefone'
        })
    )

    class Meta:
        model = Inscricao
        fields = '__all__'

    def clean_telefone(self):
        telefone = self.cleaned_data['telefone']
        
        # Remove espaços, traços e outros caracteres não numéricos
        telefone = telefone.replace(" ", "").replace("-", "")
        
        # Verifica se o telefone tem 11 dígitos e começa com 9 (telefone celular)
        if len(telefone) != 11 or not telefone.isdigit() or telefone[2] != '9':
            raise forms.ValidationError("Número de telefone inválido. Use o formato 11 91234 5678.")
        
        return telefone


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
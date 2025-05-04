from django import forms
from .models import Inscricao, AnexosInscricao

class InscricaoForm(forms.ModelForm):
    class Meta:
        model = Inscricao
        fields = '__all__'

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
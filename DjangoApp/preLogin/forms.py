from django import forms
from .models import Inscricao, AnexosInscricao

class InscricaoForm(forms.ModelForm):
    class Meta:
        model = Inscricao
        fields = ['nome_completo','nome_social','dt_nasc','cpf','email','telefone','endereco','possui_deficiencia','aluno_uece','como_conheceu','prioridades',
                'ocupacao','motivacao','turma_entrada','foto_frente','foto_verso','diploma_ensino_medio','termo_inscricao']

class MultiFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultiFileField(forms.FileField):
    def _init_(self, *args, **kwargs):
        kwargs.setdefault("widget", MultiFileInput())
        super()._init_(*args, **kwargs)

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

class TesteDeNivelForm(forms.ModelForm):
    class Meta:
        model = Inscricao
        fields = ['turma_teste_de_nivel']
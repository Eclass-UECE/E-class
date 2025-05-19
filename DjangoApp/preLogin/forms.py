from django import forms
from .models import Inscricao, AnexosInscricao
import os
import pickle
from django.conf import settings

def get_turma_choices():
    try:
        caminho = os.path.join(settings.BASE_DIR, 'turmas_escolhidas.pkl')
        with open(caminho, 'rb') as f:
            turmas = pickle.load(f)
        print(">>> Turmas carregadas:", turmas)
        return [(turma, turma) for turma in turmas]
    except Exception as e:
        print("Erro ao carregar turmas:", e)
        return []

class InscricaoForm(forms.ModelForm):
    class Meta:
        model = Inscricao
        fields = ['nome_completo', 'nome_social', 'dt_nasc', 'cpf',
                  'email', 'telefone', 'endereco', 'aluno_uece', 'possui_deficiencia',
                  'qual_deficiencia', 'como_conheceu', 'prioridades', 'ocupacao', 'motivacao',
                  'turma_entrada', 'foto_frente', 'foto_verso', 'diploma_ensino_medio',
                  'termo_inscricao']

class TestedenivelForm(forms.ModelForm):
    teste_nivel = forms.ChoiceField(choices=[], required=False)

    class Meta:
        model = Inscricao
        fields = ['teste_nivel']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        caminho_arquivo = os.path.join(settings.BASE_DIR, 'turmas_escolhidas.pkl')
        if os.path.exists(caminho_arquivo):
            with open(caminho_arquivo, 'rb') as f:
                turmas = pickle.load(f)
            # Define as opções do campo
            self.fields['teste_nivel'].choices = [
                (turma, f"Turma: {turma.upper()}") for turma in turmas  # Exemplo: "s01" → "S01"
            ]
        else:
            self.fields['teste_nivel'].disabled = True

    def clean_teste_nivel(self):
        # Ignora validação do modelo
        return self.cleaned_data['teste_nivel']



class MultiFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultiFileField(forms.FileField):
    def init(self, *args, kwargs):
        kwargs.setdefault("widget", MultiFileInput())
        super().init(*args, **kwargs)

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



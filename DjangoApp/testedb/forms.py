from django import forms
from .models import Inscricao, AnexosInscricao

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class InscricaoForm(forms.ModelForm):
    class Meta():
       model = Inscricao
       fields = "__all__"

class MultiFileForm(forms.ModelForm):
    class Meta:
        model = AnexosInscricao
        fields = ["arquivo"]
 
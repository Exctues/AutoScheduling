from django import forms
from u_csv.models import Document


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('description', 'document', )

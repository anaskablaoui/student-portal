from django import forms
from .models import Rapport, Etudiant
from django.utils import timezone

class RapportForm(forms.ModelForm):
    class Meta:
        model = Rapport
        fields = ['etudiant', 'description', 'date']
        widgets = {
            'etudiant': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Sélectionner un étudiant'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Rédigez votre rapport ici...'
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
        }
        labels = {
            'etudiant': 'Étudiant',
            'description': 'Description du rapport',
            'date': 'Date',
        }

    def __init__(self, *args, **kwargs):
        # On récupère le professeur connecté passé depuis la vue
        self.professeur = kwargs.pop('professeur', None)
        super().__init__(*args, **kwargs)
        self.fields['date'].initial = timezone.now().date()
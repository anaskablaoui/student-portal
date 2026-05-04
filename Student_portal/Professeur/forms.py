from django import forms
from .models import Rapport, Professeur,absence
from django.utils import timezone
from authApp.models import custumUser


class ProfesseurCreationForm(forms.ModelForm):
    # champs du customUser a remplir 
    nom=forms.CharField(label="nom")
    prenom=forms.CharField(label="prenom")
    email=forms.EmailField(label="email", required=False)
    password1 = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)
    password2= forms.CharField(label="Confirmer mots de passe ",widget=forms.PasswordInput)
    matricule = forms.CharField(label="Matricule")

    class Meta :
        model = Professeur
        fields = ['CIN']

    def clean (self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password1")
        p2 = cleaned_data.get("password2")
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")
        return cleaned_data

    def save(self,commit=True):
        #creee le customuser avec le role 'agent'
        user = custumUser.objects.create_user(
            nom=self.cleaned_data['nom'],
            prenom=self.cleaned_data['prenom'],
            email=self.cleaned_data.get('email', ''),
            matricule=self.cleaned_data['matricule'],
            password=self.cleaned_data['password1'],
            role='professeur'
        )

        prof=super().save(commit=False)
        prof.user=user
        if commit:
            prof.save()
        return prof

class ProfesseurChangeForm(forms.ModelForm):
    matricule = forms.CharField()  # custom field, not from Professeur model

    class Meta:
        model = Professeur
        fields = ('user', 'CIN')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['matricule'].initial = self.instance.user.matricule

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
        

class absenceForm(forms.ModelForm):
    class Meta:
        model = absence
        fields = ['seance', 'status', 'etudiant']
        widgets = {
            'status': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            })
           
        }
        labels = {
            
            'status': 'Absent',
            
        }


class messageForm(forms.Form):
    content = forms.CharField(label='Message', widget=forms.Textarea(attrs={
        'class': 'form-control',
        'rows': 5,
        'placeholder': 'Rédigez votre message ici...'
    }))
    
    
class noteForm(forms.Form):
    note = forms.DecimalField(label='Note', max_digits=2, decimal_places=2, widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Entrez la note (ex: 15.5)',
        'min': 0,
        'max': 20,
        'step': 0.01,
    }))
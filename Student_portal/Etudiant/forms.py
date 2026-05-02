from django import forms
from .models import Etudiant
from django.utils import timezone
from authApp.models import custumUser


class EtudiantCreationForm(forms.ModelForm):
    # Champs du customUser
    nom            = forms.CharField(label="Nom")
    prenom         = forms.CharField(label="Prénom")
    email          = forms.EmailField(label="Email", required=False)
    matricule      = forms.CharField(label="Matricule")
    password1      = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)
    password2      = forms.CharField(label="Confirmer mot de passe", widget=forms.PasswordInput)

    class Meta:
        model  = Etudiant
        fields = ['CIN', 'date_naissance', 'groupe']

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password1")
        p2 = cleaned_data.get("password2")
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")
        return cleaned_data

    def save(self, commit=True):
        # Créer le customUser avec le rôle 'etudiant'
        user = custumUser.objects.create_user(
            nom       = self.cleaned_data['nom'],
            prenom    = self.cleaned_data['prenom'],
            email     = self.cleaned_data.get('email', ''),
            matricule = self.cleaned_data['matricule'],
            password  = self.cleaned_data['password1'],
            role      = 'etudiant'
        )

        etudiant = super().save(commit=False)
        etudiant.user = user
        if commit:
            etudiant.save()
        return etudiant


class EtudiantChangeForm(forms.ModelForm):
    class Meta:
        model  = Etudiant
        fields = '__all__'
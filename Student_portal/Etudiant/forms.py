from django import forms
from .models import Etudiant
from django.utils import timezone
from authApp.models import custumUser
from Professeur.models import Message


class EtudiantCreationForm(forms.ModelForm):
    # champs du customUser
    nom = forms.CharField(label="Nom")
    prenom = forms.CharField(label="Prénom")
    email = forms.EmailField(label="Email", required=False)
    password1 = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmer mot de passe", widget=forms.PasswordInput)
    matricule = forms.CharField(label="Matricule")

    class Meta:
        model = Etudiant
        fields = ['CIN', 'date_naissance', 'groupe']  # only Etudiant's own fields

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password1")
        p2 = cleaned_data.get("password2")
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")
        return cleaned_data

    def save(self, commit=True):
        # create the customUser with role 'etudiant'
        user = custumUser.objects.create_user(
            nom=self.cleaned_data['nom'],
            prenom=self.cleaned_data['prenom'],
            email=self.cleaned_data.get('email', ''),
            matricule=self.cleaned_data['matricule'],
            password=self.cleaned_data['password1'],
            role='etudiant'
        )

        etudiant = super().save(commit=False)
        etudiant.user = user
        if commit:
            etudiant.save()
        return etudiant


class EtudiantChangeForm(forms.ModelForm):
    # these live on customUser, not Etudiant, so we declare them manually
    matricule = forms.CharField(label="Matricule")
    nom = forms.CharField(label="Nom")
    prenom = forms.CharField(label="Prénom")
    email = forms.EmailField(label="Email", required=False)

    class Meta:
        model = Etudiant
        fields = ('user', 'CIN', 'date_naissance', 'groupe')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # pre-fill user fields from the related customUser
        if self.instance and self.instance.pk:
            self.fields['matricule'].initial = self.instance.user.matricule
            self.fields['nom'].initial = self.instance.user.nom
            self.fields['prenom'].initial = self.instance.user.prenom
            self.fields['email'].initial = self.instance.user.email

class EtudiantForm(forms.ModelForm):
    description = forms.CharField(
        label="Message",
        widget=forms.Textarea(attrs={
            'rows': 4,
            'placeholder': 'Rédigez votre message ici...',
        })
    )
    class Meta:
        model = Message
        fields = ['description']
from django import forms
from Professeur.models import Professeur
from Etudiant.models import Etudiant



class ProfesseurLoginForm(forms.ModelForm):
    matricule=forms.CharField(widget=forms.TextInput,label="type matricule")
    password=forms.CharField(widget=forms.PasswordInput,label="type password")
    
    class Meta:
        model= Professeur
        fields =['matricule','password']
        
class EtudiantLoginForm(forms.ModelForm):
    matricule=forms.CharField(widget=forms.TextInput,label='type matricule')
    password=forms.CharField(widget=forms.PasswordInput,label='type password')
    
    class Meta:
        model= Professeur
        fields =['matricule','password']
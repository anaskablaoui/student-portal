from django import forms
from Professeur.models import Professeur
from Etudiant.models import Etudiant



class ProfesseurLoginForm(forms.ModelForm):
    matricule=forms.CharField(widget=forms.TextInput(attrs={
                            'class':'input',
                            'placeholder':'entrer votre matricule'
                        }),
                              label="Matricule"
                              
                              )
    password=forms.CharField(widget=forms.PasswordInput(attrs={
                            'class':'input',
                            'placeholder':'entrer votre mot de passe '
                        }),
                             label="type password"
                             )
    
    class Meta:
        model= Professeur
        fields =['matricule','password']
        
class EtudiantLoginForm(forms.ModelForm):
    matricule=forms.CharField(widget=forms.TextInput(attrs={
                            'class':'input',
                            'placeholder':'entrer votre matricule'
                        }),
                              label='type matricule')
    password=forms.CharField(widget=forms.PasswordInput(attrs={
                            'class':'input',
                            'placeholder':'entrer votre mot de passe '
                        }),
                             label='type password')
    
    class Meta:
        model= Etudiant
        fields =['matricule','password']
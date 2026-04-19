from django.db import models
from Administrateur.models import Groupe
# Create your models here.
class Etudiant(models.Model):
    matricule=models.IntegerField(unique=True,primary_key=True)
    nom=models.CharField(max_length=50,unique=False)
    prenom=models.CharField(max_length=50,unique=False)
    CIN=models.CharField(max_length=10,unique=True)
    date_naissance=models.DateField()
    groupe=models.ForeignKey(Groupe,on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return self.nom
from django.db import models
from Administrateur.models import Session,Matiere
from Etudiant.models import Etudiant

# Create your models here.
class Professeur(models.Model):
    matricule=models.CharField(max_length=10,unique=True,primary_key=True)
    nom=models.CharField(max_length=50,unique=False)
    prenom=models.CharField(max_length=50,unique=False)
    CIN=models.CharField(max_length=50,unique=True)

    def __str__(self):
        return self.nom
    
class presence(models.Model):
    id=models.IntegerField(unique=True,primary_key=True)
    seance=models.ForeignKey(Session,on_delete=models.CASCADE,null=False)
    info=models.ForeignKey('Status_presence',on_delete=models.CASCADE,null=False)

    def __str__(self):
        return str(self.id)

class Status_presence(models.Model):
    etudiant=models.ForeignKey(Etudiant,on_delete=models.CASCADE,null=False)
    status=models.BooleanField()

    def __str__(self):
        return super().__str__()
    
class Message(models.Model):
    id=models.IntegerField(unique=True,primary_key=True)
    description=models.CharField(max_length=200)

    def __str__(self):
        return super().__str__()

class Rapport(models.Model):
    id=models.IntegerField(unique=True,primary_key=True)
    etudiant=models.ForeignKey(Etudiant,on_delete=models.CASCADE,null=False)
    description=models.CharField(max_length=200)
    professeur=models.ForeignKey(Professeur,on_delete=models.CASCADE,null=False)

    def __str__(self):
        return super().__str__()

class Note(models.Model):
    id=models.IntegerField(unique=True,primary_key=True)
    note=models.DecimalField(max_digits=2,decimal_places=2)
    matiere=models.ForeignKey(Matiere,on_delete=models.CASCADE,null=False)
    etudiant=models.ForeignKey(Etudiant,on_delete=models.CASCADE,null=False)

    def __str__(self):
        return super().__str__()


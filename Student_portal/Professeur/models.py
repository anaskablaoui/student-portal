from django.db import models
from Administrateur.models import Session,Matiere
from Etudiant.models import Etudiant
from django.contrib.auth.models import AbstractUser,Group,Permission
from authApp.models import custumUser

# Create your models here.
class Professeur(models.Model):
    user = models.OneToOneField(custumUser, on_delete=models.CASCADE)
    CIN=models.CharField(max_length=50,unique=True)
    groupe=models.ManyToManyField('Administrateur.Groupe',related_name='professeurs')
    class Meta:
        verbose_name= 'Professuer'
        verbose_name_plural='Professeurs'
    
    
    
class absence(models.Model):
    id = models.AutoField(primary_key=True)
    seance = models.ForeignKey(Session, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)

    def __str__(self):
        return f"Absence {self.id} - {self.etudiant}"


class Message(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.description


class Rapport(models.Model):
    id = models.AutoField(primary_key=True)
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    professeur = models.ForeignKey(Professeur, on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return f"Rapport {self.id} - {self.etudiant}"


class Note(models.Model):
    id = models.AutoField(primary_key=True)
    note = models.DecimalField(max_digits=4, decimal_places=2)
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)

    def __str__(self):
        return f"Note {self.note} - {self.etudiant}"


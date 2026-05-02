from django.db import models
from Administrateur.models import Groupe
from django.contrib.auth.models import AbstractUser,Group,Permission
from authApp.models import custumUser
# Create your models here.
class Etudiant(models.Model):
    user = models.OneToOneField(custumUser,on_delete=models.CASCADE)

    CIN=models.CharField(max_length=10,unique=True)
    date_naissance=models.DateField()
    groupe=models.ForeignKey(Groupe,on_delete=models.SET_NULL,null=True)

    

    def __str__(self):
        return f"{self.user.nom} {self.user.prenom}"
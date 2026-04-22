from django.db import models
from Administrateur.models import Session,Matiere
from Etudiant.models import Etudiant
from django.contrib.auth.models import AbstractUser,Group,Permission

# Create your models here.
class Professeur(AbstractUser):
    matricule=models.CharField(max_length=10,unique=True,primary_key=True)
    nom=models.CharField(max_length=50,unique=False)
    prenom=models.CharField(max_length=50,unique=False)
    CIN=models.CharField(max_length=50,unique=True)

    class Meta:
        verbose_name= 'Professuer'
        verbose_name_plural='Professeurs'
    
    #redifinition des relation pour eviter les conflits
    groups=models.ManyToManyField(
        Group,
        related_name="professeur_groups",
        related_query_name="professeur",
        blank=True,
        verbose_name='groups',
        help_text='the groups this user belongs to'
    )
    
    user_permissions=models.ManyToManyField(
        Permission,
        related_name="professeur_permission",
        related_query_name="professeur",
        blank=True,
        verbose_name='professeur permissions',
        help_text='Specific permissions for this user'
    )
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


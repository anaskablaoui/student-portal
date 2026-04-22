from django.db import models
from Administrateur.models import Groupe
from django.contrib.auth.models import AbstractUser,Group,Permission
# Create your models here.
class Etudiant(AbstractUser):
    matricule=models.IntegerField(unique=True,primary_key=True)
    nom=models.CharField(max_length=50,unique=False)
    prenom=models.CharField(max_length=50,unique=False)
    CIN=models.CharField(max_length=10,unique=True)
    date_naissance=models.DateField()
    groupe=models.ForeignKey(Groupe,on_delete=models.SET_NULL,null=True)

    class Meta:
        verbose_name='etudiant'
        verbose_name_plural='etudiants'
    #redifinition des relation pour eviter les conflits
    groups=models.ManyToManyField(
        Group,
        related_name="Etudiant_groups",
        related_query_name="etudiant",
        blank=True,
        verbose_name='groups',
        help_text='the groups this user belongs to'
    )
    
    user_permissions=models.ManyToManyField(
        Permission,
        related_name="etudiant_permission",
        related_query_name="etudiant",
        blank=True,
        verbose_name='admin permissions',
        help_text='Specific permissions for this user'
    )
    def __str__(self):
        return self.nom
from django.db import models
from django.contrib.auth.models import AbstractUser,Group,Permission
# Create your models here.

class Administrateur(AbstractUser):
    matricule = models.CharField(max_length=10, unique=True, primary_key=True)
    nom = models.CharField(max_length=20)
    prenom = models.CharField(max_length=20)
    
    USERNAME_FIELD = 'matricule'
    REQUIRED_FIELDS = ['nom', 'prenom', 'email']

    class Meta:
        verbose_name='Administrateur'
        verbose_name_plural='Utilisateur'
        
    #redifinition des relation pour eviter les conflits
    groups=models.ManyToManyField(
        Group,
        related_name="Administrateur_groups",
        related_query_name="administrateur",
        blank=True,
        verbose_name='groups',
        help_text='the groups this user belongs to'
    )
    
    user_permissions=models.ManyToManyField(
        Permission,
        related_name="Administrateur_permission",
        related_query_name="administrateur",
        blank=True,
        verbose_name='admin permissions',
        help_text='Specific permissions for this user'
    )
    def __str__(self):
        return f"{self.nom} {self.prenom}"

class Filier(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=50, unique=True)
    modules = models.ManyToManyField('Module', related_name='filieres')

    def __str__(self):
        return self.nom

class Module(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=50)
    filiere = models.ForeignKey(Filier, on_delete=models.CASCADE, related_name='modules_specific')

    def __str__(self):
        return self.nom

class Groupe(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=6, unique=True)
    filier = models.ForeignKey(Filier, on_delete=models.CASCADE, related_name='groupes')

    def __str__(self):
        return self.nom

class Matiere(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=50)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='matieres')

    def __str__(self):
        return self.nom

class Salle(models.Model):
    num = models.IntegerField(unique=True, primary_key=True)

    def __str__(self):
        return f"Salle {self.num}"

class Session(models.Model):
    id = models.AutoField(primary_key=True)
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)
    date = models.DateField()
    heure_depart = models.TimeField()
    heure_fin = models.TimeField()

    def __str__(self):
        return f"Session {self.id} - {self.matiere.nom}"


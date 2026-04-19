from django.db import models

# Create your models here.

class Administrateur(models.Model):
    matricule = models.CharField(max_length=10, unique=True, primary_key=True)
    nom = models.CharField(max_length=20)
    prenom = models.CharField(max_length=20)

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


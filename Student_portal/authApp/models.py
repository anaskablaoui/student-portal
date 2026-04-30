from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
# Create your models here.

class customUserManager(BaseUserManager):
    """Manager unique qui gère tous les rôles"""
    
    def _create_user(self, matricule=None, email=None, password=None, **extra_fields):
        username_field = extra_fields.get('role')
        if not matricule and not email:
            raise ValueError("Un matricule ou email est obligatoire")
        if email:
            email = self.normalize_email(email)
        user = self.model(matricule=matricule, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, matricule=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(matricule=matricule, email=email, password=password, **extra_fields)

    def create_superuser(self, matricule, email=None,password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'administrateur')
        return self._create_user( matricule=matricule,email=email, password=password, **extra_fields)



class custumUser(AbstractUser):
    username= None

    ROLE_CHOICES = [
        ('etudiant','Etudiant'),
        ('administrateur','Administrateur'),
        ('professeur','Professeur')
    ]
    email      = models.EmailField(max_length=50, unique=True, blank=True,null=True)
    matricule  = models.CharField(max_length=12, unique=True, blank=True)
    nom        = models.CharField(max_length=50)
    prenom     = models.CharField(max_length=50)
    role       = models.CharField(max_length=20, choices=ROLE_CHOICES)
    
    USERNAME_FIELD = 'matricule'
    REQUIRED_FIELDS = ['nom','prenom','role']

    objects = customUserManager()

    class Meta:
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'

    def is_Etudiant(self):
        return self.role == 'etudiant'
    
    def is_Administrateur(self):
        return self.role == 'administrateur'

    def is_Professeur(self):
        return self.role == 'professeur'
    
    def __str__(self):
        return f"{self.nom} {self.prenom} ({self.role})"
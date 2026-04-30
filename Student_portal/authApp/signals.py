from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import custumUser
from Administrateur.models import Administrateur
from Etudiant.models import Etudiant
from Professeur.models import Professeur

@receiver(post_save, sender=custumUser)
def create_profile(sender,instance,created,**kwargs):
    if not created:
        return
    
    profiles ={
        'administrateur':lambda: Administrateur.objects.create(
            user=instance,matricule=instance.matricule or '',prenom=instance.prenom or '',nom=instance.nom or ''
        ),
        'professeur':lambda: Professeur.objects.create(
            user=instance,matricule=instance.matricule or '',prenom=instance.prenom or '',nom=instance.nom or ''
        ),
        'etudiant': lambda:Etudiant.objects.create(
            user=instance,matricule=instance.matricule or '',prenom=instance.prenom or '',nom=instance.nom or ''
        )
    }

    creator = profiles.get(instance.role)
    if creator:
        creator()
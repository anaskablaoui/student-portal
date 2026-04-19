from django.contrib import admin
from Etudiant.models import Etudiant

@admin.register(Etudiant)
class EtudiantAdmin(admin.ModelAdmin):
    list_display = ('matricule', 'nom', 'prenom', 'CIN', 'date_naissance', 'groupe')
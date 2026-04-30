from django.contrib import admin
from Etudiant.models import Etudiant

@admin.register(Etudiant)
class EtudiantAdmin(admin.ModelAdmin):
    list_display = ('get_matricule', 'get_nom', 'get_prenom', 'CIN', 'date_naissance', 'groupe')
    

    def get_matricule(self, obj):
        return obj.user.matricule

    def get_nom(self, obj):
        return obj.user.nom

    def get_prenom(self, obj):
        return obj.user.prenom
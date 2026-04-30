from django.contrib import admin
from Professeur.models import Professeur, presence, Status_presence, Message, Rapport, Note

@admin.register(Professeur)
class ProfesseurAdmin(admin.ModelAdmin):
    list_display = ('get_matricule', 'get_nom', 'get_prenom', 'CIN')
    

    def get_matricule(self, obj):
        return obj.user.matricule

    def get_nom(self, obj):
        return obj.user.nom

    def get_prenom(self, obj):
        return obj.user.prenom

@admin.register(presence)
class PresenceAdmin(admin.ModelAdmin):
    list_display = ('id', 'seance', 'info')

@admin.register(Status_presence)
class StatusPresenceAdmin(admin.ModelAdmin):
    list_display = ('id', 'etudiant', 'status')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'description')

@admin.register(Rapport)
class RapportAdmin(admin.ModelAdmin):
    list_display = ('id', 'etudiant', 'professeur', 'description')

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'note', 'matiere', 'etudiant')
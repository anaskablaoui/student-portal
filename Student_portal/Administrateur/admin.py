from django.contrib import admin
from Administrateur.models import Administrateur, Module, Filier, Groupe, Matiere, Salle, Session

# Register your models here.

@admin.register(Administrateur)
class AdministrateurAdmin(admin.ModelAdmin):
    list_display = ('matricule', 'nom', 'prenom')

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'filiere')

@admin.register(Filier)
class FilierAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom')

@admin.register(Groupe)
class GroupeAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'filier')

@admin.register(Matiere)
class MatiereAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'module')

@admin.register(Salle)
class SalleAdmin(admin.ModelAdmin):
    list_display = ('num',)

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'matiere', 'date', 'heure_depart', 'heure_fin')


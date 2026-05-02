from django.contrib import admin
from Etudiant.models import Etudiant
from .forms import EtudiantChangeForm,EtudiantCreationForm

@admin.register(Etudiant)
class EtudiantAdmin(admin.ModelAdmin):
    list_display = ('get_matricule', 'get_nom', 'get_prenom', 'CIN', 'date_naissance', 'groupe')

    def get_matricule(self, obj):
        return obj.user.matricule

    def get_nom(self, obj):
        return obj.user.nom

    def get_prenom(self, obj):
        return obj.user.prenom

    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            kwargs['form'] = EtudiantCreationForm
        else:
            kwargs['form'] = EtudiantChangeForm
        return super().get_form(request, obj, **kwargs)

    def get_fields(self, request, obj=None):
        if obj is None:
            return ('nom', 'prenom', 'email', 'password1', 'password2', 'matricule', 'CIN', 'date_naissance', 'groupe')
        else:
            return ('user', 'CIN', 'date_naissance', 'groupe')

    def get_matricule(self, obj):
        return obj.user.matricule

    def get_nom(self, obj):
        return obj.user.nom

    def get_prenom(self, obj):
        return obj.user.prenom
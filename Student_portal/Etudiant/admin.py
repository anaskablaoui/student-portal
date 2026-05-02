from django.contrib import admin
from Etudiant.models import Etudiant
from .forms import EtudiantChangeForm,EtudiantCreationForm

@admin.register(Etudiant)
class EtudiantAdmin(admin.ModelAdmin):
    list_display = ('get_matricule', 'get_nom', 'get_prenom', 'CIN', 'date_naissance', 'groupe')

    def get_matricule(self, obj):
        return obj.user.matricule
    get_matricule.short_description = 'Matricule'

    def get_nom(self, obj):
        return obj.user.nom
    get_nom.short_description = 'Nom'

    def get_prenom(self, obj):
        return obj.user.prenom
    get_prenom.short_description = 'Prénom'

    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            kwargs['form'] = EtudiantCreationForm
        else:
            kwargs['form'] = EtudiantChangeForm
        return super().get_form(request, obj, **kwargs)

    def get_fields(self, request, obj=None):
        if obj is None:
            # creation fields
            return ('nom', 'prenom', 'email', 'password1', 'password2', 'matricule', 'CIN', 'date_naissance', 'groupe')
        else:
            # change fields — matricule/nom/prenom/email are custom fields on the form
            return ('user', 'matricule', 'nom', 'prenom', 'email', 'CIN', 'date_naissance', 'groupe')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # save the customUser fields back when editing
        if change:
            obj.user.matricule = form.cleaned_data['matricule']
            obj.user.nom = form.cleaned_data['nom']
            obj.user.prenom = form.cleaned_data['prenom']
            obj.user.email = form.cleaned_data.get('email', '')
            obj.user.save()
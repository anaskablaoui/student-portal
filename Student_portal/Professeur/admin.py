from django.contrib import admin
from Professeur.models import Professeur, absence, Message, Rapport, Note
from .forms import ProfesseurCreationForm,ProfesseurChangeForm
@admin.register(Professeur)
class ProfesseurAdmin(admin.ModelAdmin):
    list_display = ('get_matricule', 'get_nom', 'get_prenom','get_groupe', 'CIN')
    
    def get_matricule(self, obj):
        return obj.user.matricule

    def get_nom(self, obj):
        return obj.user.nom

    def get_prenom(self, obj):
        return obj.user.prenom

    def get_groupe(self, obj):
        return obj.user.groupe.all()
    
    def get_form(self,request,obj=None,**kwargs):

        if obj is None:
            kwargs['form']=ProfesseurCreationForm
        else:
            kwargs['form'] = ProfesseurChangeForm
        return super().get_form(request,obj,**kwargs)

    def get_fields(self,request,obj=None):
        if obj is None:
            return ('nom', 'prenom', 'email', 'password1','groupe','password2', 'matricule', 'CIN')
        else:
            return('user','matricule','groupe','CIN')
        
        
@admin.register(absence)
class AbsenceAdmin(admin.ModelAdmin):
    list_display = ('id', 'seance', 'status', 'etudiant')



@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'description')

@admin.register(Rapport)
class RapportAdmin(admin.ModelAdmin):
    list_display = ('id', 'etudiant', 'professeur', 'description')

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'note', 'matiere', 'etudiant')
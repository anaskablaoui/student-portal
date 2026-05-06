from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from Professeur.models import Note, Rapport,absence
from .models import Etudiant

@login_required(login_url='/login/')
def etudiant_dashboard(request):
    # request.user contient l'etudiant connecté
    etudiant = request.user
    return render(request, 'etudiant.html', {
        'etudiant': etudiant,
    })
    
class listeNotes(ListView):
    model = Note
    template_name = 'etudiant.html'
    context_object_name = 'notes'

    def getProfesseur(self):
        groupe = Etudiant.request.get(user=self.request.user)
        return Note.objects.filter(etudiant=etudiant)
    
    def get_queryset(self):
        etudiant = Etudiant.request.user(user=self.request.user)
        return Note.objects.filter(etudiant=etudiant)
    
class absencesListView(ListView):
    model = absence
    template_name = 'etudiant.html'
    context_object_name = 'absences'

    def get_queryset(self):
        etudiant = Etudiant.request.get(user=self.request.user)
        return absence.objects.filter(etudiant=etudiant)
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from Professeur.models import Note, Rapport,absence,Message
from .models import Etudiant
from .forms import EtudiantForm


@login_required(login_url='/login/')
def etudiant_dashboard(request):
    etudiant = request.user

    if request.method == 'POST':
        form = EtudiantForm(request.POST)
        if form.is_valid():
            message = form.save()
            return redirect('etudiant_dashboard')  # évite la re-soumission du formulaire
    else:
        form = EtudiantForm()

    return render(request, 'etudiant.html', {
        'etudiant': etudiant,
        'form': form,
    })
    
class listeNotes(ListView):
    model = Note
    template_name = 'etudiant.html'
    context_object_name = 'notes'

    
    
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
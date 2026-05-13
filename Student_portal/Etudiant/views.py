from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from Professeur.models import Note, Rapport,absence,Message
from .models import Etudiant
from .forms import EtudiantForm
from django.db.models import Avg
from datetime import datetime
from django.http import JsonResponse
from Administrateur.models import Session,Matiere

@login_required(login_url='/login/')
def etudiant_dashboard(request):
    etudiant = Etudiant.objects.get(user=request.user)
    notes = Note.objects.filter(etudiant=etudiant).select_related(
        'matiere'
    )

    matieres = Matiere.objects.all()

    context = {
        'notes': notes,
        'matieres': matieres,
    }


    
    if request.method == 'POST':
        etudiant = Etudiant.objects.get(user=request.user)
        form = EtudiantForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)  
            message.user = request.user        
            message.save()                     
            return redirect('etudiant_dashboard')  
    else:
        form = EtudiantForm()

    return render(request, 'etudiant.html', {
        'etudiant' : etudiant,
        
        'absences' : absence.objects.filter(etudiant=etudiant),
        'messages' : Message.objects.all(),
        'form'     : form,
        'notes': notes,
        'matieres': matieres,
    })
    
@login_required(login_url='login')
def calendrier_events(request):

    events = []

    sessions = Session.objects.select_related('matiere', 'groupe')

    for session in sessions:

        start = datetime.combine(
            session.date,
            session.heure_depart
        )

        end = datetime.combine(
            session.date,
            session.heure_fin
        )

        events.append({
            "title": session.matiere.nom,
            "start": start.isoformat(),
            "end": end.isoformat(),
            "extendedProps": {
                "groupe": session.groupe.nom if session.groupe else "",
            }
        })

    return JsonResponse(events, safe=False)   
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
    
class messageListView(ListView):
    model = Message
    template_name = 'etudiant.html'
    context_object_name = 'messages'


from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from Professeur.models import Note, Rapport,absence,Message
from .models import Etudiant
from .forms import changerPassword
from django.db.models import Avg
from datetime import datetime
from django.http import JsonResponse
from Administrateur.models import Session,Matiere
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from Professeur.forms import messageForm

@login_required(login_url='/login/')
def etudiant_dashboard(request):
    
    etudiant = Etudiant.objects.get(user=request.user)
    rapport=Rapport.objects.filter(etudiant=etudiant)
    notes = Note.objects.filter(etudiant=etudiant).select_related(
        'matiere'
    )
    PasswordForm=changerPassword()
    form = messageForm()
    matieres = Matiere.objects.all()

    context = {
        'notes': notes,
        'matieres': matieres,
    }

    total_seances = Session.objects.filter(groupe=etudiant.groupe).count()

    # Nombre d'absences de cet étudiant (status=True = absent)
    absences_count = absence.objects.filter(
        etudiant=etudiant,
        status=True
        ).count()

    # Taux de présence
    if total_seances > 0:
        taux_presence = round(((total_seances - absences_count) / total_seances) * 100, 1)
    else:
        taux_presence = 0
    
    if request.method == 'POST':
        if 'submit-demande' in request.POST:
            etudiant = Etudiant.objects.get(user=request.user)
            form = messageForm(request.POST)
            if form.is_valid():
                message = form.save(commit=False)  
                message.user = request.user        
                message.save()                     
                return redirect('etudiant_dashboard')  
        elif 'submit_password' in request.POST:
            PasswordForm = changerPassword(request.POST)
            if PasswordForm.is_valid():
                ancien = PasswordForm.cleaned_data['passwordExistant']
                nouveau = PasswordForm.cleaned_data['nouveauPassword']
        
                if not request.user.check_password(ancien):
                    messages.error(request, "Mot de passe actuel incorrect.")
                else:
                    request.user.set_password(nouveau)
                    request.user.save()
                    update_session_auth_hash(request, request.user)
                    messages.success(request, "Mot de passe modifié avec succès.")
            else:
                messages.error(request, "Formulaire invalide.")
    
            return redirect('etudiant_dashboard')
        

    return render(request, 'etudiant.html', {
        'etudiant' : etudiant,
        'rapport':rapport,
        'absences' : absence.objects.filter(etudiant=etudiant),
        'msgs' : Message.objects.filter(user=request.user),
        'form'     : form,
        'notes': notes,
        'matieres': matieres,
        'presence':taux_presence,
        'PasswordForm':PasswordForm
    })
    
@login_required(login_url='/login/')
def calendrier_events(request):
    etudiant = Etudiant.objects.get(user=request.user)
    sessions = Session.objects.filter(
        groupe=etudiant.groupe
    ).select_related('matiere', 'groupe')

    events = []
    for session in sessions:
        start = datetime.combine(session.date, session.heure_depart)
        end = datetime.combine(session.date, session.heure_fin)
        events.append({
            "title": session.matiere.nom,
            "start": start.isoformat(),
            "end": end.isoformat(),
            "extendedProps": {
                "groupe": session.groupe.nom if session.groupe else "",
            }
        })
    return JsonResponse(events, safe=False)


def Bulletin(request):
    etudiant = Etudiant.objects.get(user=request.user)
    notes=Note.objects.filter(etudiant=etudiant)
    moyenne = notes.aggregate(Avg('note'))['note__avg']
    return render(request,'bulletin.html',{
        'etudiant':etudiant,
        'notes':notes,
        'moyenne':moyenne
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
    
class messageListView(ListView):
    model = Message
    template_name = 'etudiant.html'
    context_object_name = 'messages'

@login_required(login_url='/login/')
def statistiques_notes(request):
    etudiant = Etudiant.objects.get(user=request.user)
    notes = Note.objects.filter(etudiant=etudiant).select_related('matiere')
    
    data = {
        'labels': [note.matiere.nom for note in notes],
        'notes': [float(note.note) for note in notes],
    }
    return JsonResponse(data)
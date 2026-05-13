from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RapportForm, absenceForm, messageForm, noteForm
from .models import Professeur, Rapport, Message, absence, Note
from Etudiant.models import Etudiant
from django.views.generic import ListView
from Administrateur.models import Session
from datetime import datetime
from django.http import JsonResponse


@login_required(login_url='login')
def dashboard(request):

    no

    if request.user.role != 'professeur':
        messages.error(request, "Accès refusé. Vous n'êtes pas un professeur.")
        return redirect('login')  # ou une autre page appropriée
    
    try:
        professeur = Professeur.objects.get(user=request.user)
    except Professeur.DoesNotExist:
        messages.error(request, "Profil professeur non trouvé. Contactez l'administrateur.")
        return redirect('login')
    
    etudiants = Etudiant.objects.filter(groupe__in=professeur.groupe.all()).distinct()
    sessions = Session.objects.filter(groupe__in=professeur.groupe.all()).order_by('date')
    selected_session = None
    form = absenceForm()
    rapportForm = RapportForm()
    mForm = messageForm()
    NoteForm = noteForm()

    if request.method == 'POST':
        session_id = request.POST.get('session_id')
        if session_id:
            selected_session = Session.objects.filter(id=session_id).first()
        if not selected_session and sessions.exists():
            selected_session = sessions.first()

        if 'submit_absence' in request.POST:
            if selected_session:
                for etudiant in etudiants:
                    status = request.POST.get(f'absence_{etudiant.id}') == 'on'
                    absence.objects.update_or_create(
                        seance=selected_session,
                        etudiant=etudiant,
                        defaults={'status': status}
                    )
                messages.success(request, "Absences enregistrées.")
            else:
                messages.error(request, "Aucune séance disponible pour enregistrer l'absence.")
            return redirect('professeur:dashboard')

        elif 'submit_rapport' in request.POST:
            rapportForm = RapportForm(request.POST)
            if rapportForm.is_valid():
                rapportForm.save()
                messages.success(request, "Rapport envoyé.")
                return redirect('professeur:dashboard')

        elif 'submit_message' in request.POST:
            mForm = messageForm(request.POST)
            if mForm.is_valid():
                message = mForm.save(commit=False)  
                message.user = request.user        
                message.save()                     
                return redirect('professeur:dashboard') 

        elif 'submit_note' in request.POST:
            if selected_session:
                for etudiant in etudiants:
                    note_value = request.POST.get(f'note_{etudiant.id}')
                    if note_value is not None and str(note_value).strip() != '':
                        Note.objects.update_or_create(
                            matiere=selected_session.matiere,
                            etudiant=etudiant,
                            defaults={'note': note_value}
                        )
                messages.success(request, "Notes enregistrées.")
            else:
                messages.error(request, "Aucune séance disponible pour enregistrer la note.")
            return redirect('professeur:dashboard')

    if not selected_session and sessions.exists():
        selected_session = sessions.first()

    existing_absences = {}
    existing_notes = {}
    if selected_session:
        existing_absences = {
            absence_obj.etudiant_id: absence_obj.status
            for absence_obj in absence.objects.filter(seance=selected_session, etudiant__in=etudiants)
        }
        existing_notes = {
            note_obj.etudiant_id: note_obj.note
            for note_obj in Note.objects.filter(matiere=selected_session.matiere, etudiant__in=etudiants)
        }

    for etudiant in etudiants:
        etudiant.absent = existing_absences.get(etudiant.id, False)
        etudiant.note_value = existing_notes.get(etudiant.id, '')

    return render(request, 'index.html', {
        'form': form,
        'rapportForm': rapportForm,
        'messageForm': mForm,
        'noteForm': NoteForm,
        'etudiants': etudiants,
        'sessions': sessions,
        'selected_session': selected_session,
    })


def profile(request):
    prof = request.user
    return render(request,'profile.html',{
        'professeur':prof
    })

class EtudiantListView(ListView):
    model = Etudiant
    template_name = 'index.html'
    context_object_name = 'etudiants'

    def dispatch(self, request, *args, **kwargs):
        if request.user.role != 'professeur':
            messages.error(request, "Accès refusé. Vous n'êtes pas un professeur.")
            return redirect('login')
        try:
            Professeur.objects.get(user=request.user)
        except Professeur.DoesNotExist:
            messages.error(request, "Profil professeur non trouvé. Contactez l'administrateur.")
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        session_id = self.kwargs.get('session_id')
        if session_id:
            session = Session.objects.select_related('groupe').get(id=session_id)
            return Etudiant.objects.filter(groupe=session.groupe)
        return Etudiant.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        session_id = self.kwargs.get('session_id')
        if session_id:
            context['session'] = Session.objects.select_related(
                'matiere', 'groupe'
            ).get(id=session_id)
        return context
    
class NoteListView(ListView):
    model = Etudiant
    template_name = 'index.html'
    context_object_name = 'noteEtudiants'
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.role != 'professeur':
            messages.error(request, "Accès refusé. Vous n'êtes pas un professeur.")
            return redirect('login')
        try:
            Professeur.objects.get(user=request.user)
        except Professeur.DoesNotExist:
            messages.error(request, "Profil professeur non trouvé. Contactez l'administrateur.")
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        professeur = Professeur.objects.get(user=self.request.user)
        return Etudiant.objects.filter(groupe__in=professeur.groupe.all())

    
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
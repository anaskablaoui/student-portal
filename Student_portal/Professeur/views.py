from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RapportForm, absenceForm, messageForm, noteForm,changerPassword
from .models import Professeur, Rapport, Message, absence, Note
from Etudiant.models import Etudiant
from django.views.generic import ListView
from Administrateur.models import Session,Matiere,Groupe
from datetime import datetime
from django.http import JsonResponse
from django.contrib.auth import update_session_auth_hash
from django.db.models import Avg


@login_required(login_url='login')
def dashboard(request):
    prof=Professeur.objects.filter(user=request.user).first()
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
    sess = Session.objects.filter(
    groupe__in=professeur.groupe.all(),
    date=datetime.today().date()
)
    selected_session = None
    form = absenceForm()
    rapportForm = RapportForm()
    mForm = messageForm()
    NoteForm = noteForm()
    PasswordForm=changerPassword()
    groupe=professeur.groupe.all()
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
                rapportForm = rapportForm.save(commit=False)
                rapportForm.professeur = professeur
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

    absences_count = absence.objects.filter(
    seance__in=sessions,  # sessions déjà filtré par le prof en haut de ta vue
    status=True
).count()

# Total des présences possibles (nb étudiants × nb séances)
    total_possible = etudiants.count() * sessions.count()

# Taux de présence
    if total_possible > 0:
        taux_presence = round(((total_possible - absences_count) / total_possible) * 100, 1)
    else:
        taux_presence = 0
        

    return render(request, 'index.html', {
        'form': form,
        'rapportForm': rapportForm,
        'messageForm': mForm,
        'noteForm': NoteForm,
        'etudiants': etudiants,
        'sessions': sessions,
        'selected_session': selected_session,
        'prof':prof,
        'groupes':groupe,
        'presence':taux_presence,
        'PasswordForm': PasswordForm,
        'sessAjourd':sess
    })


def profile(request):
    prof = request.user
    return render(request,'profile.html',{
        'professeur':prof
    })


@login_required(login_url='/login/')
def statistiques_groupes(request):

    groupes = Groupe.objects.all()

    labels = []
    moyennes = []

    for groupe in groupes:

        moyenne = Note.objects.filter(
            etudiant__groupe=groupe
        ).aggregate(
            moyenne=Avg('note')
        )['moyenne']

        labels.append(groupe.nom)
        moyennes.append(round(moyenne or 0, 2))

    data = {
        'labels': labels,
        'moyennes': moyennes
    }

    return JsonResponse(data)

@login_required(login_url='/login/')
def doughnat_presance(request):

    groupes = Groupe.objects.filter(
        professeurs__user=request.user
    )

    labels = []
    absences_data = []

    for groupe in groupes:

        nb_absences = absence.objects.filter(
            seance__groupe=groupe,
            status=True
        ).count()

        labels.append(groupe.nom)
        absences_data.append(nb_absences)

    return JsonResponse({
        'labels': labels,
        'absences': absences_data
    })
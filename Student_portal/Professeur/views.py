from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views import View
from .forms import RapportForm,absenceForm,messageForm,noteForm
from .models import Professeur, Rapport,Message
from Etudiant.models import Etudiant
from django.views.generic import ListView
from Administrateur.models import Session



@login_required(login_url='login')
def dashboard(request):
    form=absenceForm()
    rapportForm=RapportForm()
    mForm=messageForm()
    NoteForm=noteForm()
    if request.method == 'POST':
        if 'submit_absence' in request.POST:
            form = absenceForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('professeur:dashboard')
        elif 'submit_rapport' in request.POST:
            rapportForm = RapportForm(request.POST)
            if rapportForm.is_valid():
                rapportForm.save()
                return redirect('professeur:dashboard')
        elif 'submit_message' in request.POST:
            mForm = messageForm(request.POST)
            if mForm.is_valid():
                Message.objects.create(description=mForm.cleaned_data['content'])
                return redirect('professeur:dashboard')
        elif 'submit_note' in request.POST:
            NoteForm = noteForm(request.POST)
            if NoteForm.is_valid():
                # Handle note submission
                pass
    return render(request, 'index.html',
                  {
                        'form':form,
                        'rapportForm':rapportForm,
                        'messageForm':mForm,
                        'noteForm':NoteForm
                  })


class EtudiantListView(ListView):
    model = Etudiant
    template_name = 'index.html'
    context_object_name = 'etudiants'

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
    
    def get_queryset(self):
        professeur = Professeur.objects.get(user=self.request.user)
        return Etudiant.objects.filter(groupe=professeur.group)

    
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from Professeur.models import Note, Rapport,absence,Message
from .models import Etudiant
from .forms import EtudiantForm
from django.db.models import Avg


@login_required(login_url='/login/')
def etudiant_dashboard(request):
    etudiant = Etudiant.objects.get(user=request.user)
    if request.method == 'POST':
        etudiant = Etudiant.objects.get(user=request.user)
        form = EtudiantForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)  # ne pas encore sauvegarder en BDD
            message.user = request.user        # ✅ remplir user automatiquement
            message.save()                     # maintenant on sauvegarde
            return redirect('etudiant_dashboard')  # évite la re-soumission du formulaire
    else:
        form = EtudiantForm()

    return render(request, 'etudiant.html', {
        'etudiant' : etudiant,
        'notes'    : Note.objects.filter(etudiant=etudiant),
        'absences' : absence.objects.filter(etudiant=etudiant),
        'messages' : Message.objects.all(),
        'form'     : form,
    })
    
def statistics(request):
    etudiant = Etudiant.objects.get(user=request.user)
    
    notes = (
        Note.objects
        .filter(etudiant=etudiant)
        .values('matiere__nom')
        .annotate(avg_note=Avg('note'))
    )
    
    # ✅ utilise les clés du dict, pas des attributs d'objet
    labels = [n['matiere__nom'] for n in notes]
    data   = [float(n['avg_note']) for n in notes]

    #  supprime cette boucle — c'est un doublon qui cause l'erreur
    # for note in notes:
    #     labels.append(note.matiere.nom)
    #     data.append(float(note.note))

    return render(request, 'stats.html', {
        'labels': labels,
        'data'  : data,
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


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Professeur, Note, Rapport, presence

@login_required(login_url='/login/')
def professeur_dashboard(request):
    # request.user contient le professeur connecté
    professeur = request.user
    
    # récupère les rapports que ce professeur a créé
    rapports = Rapport.objects.filter(professeur=professeur)
    
    # récupère les notes que ce professeur a donné
    notes = Note.objects.filter(matiere__in=request.user.matieres.all()) \
            if hasattr(request.user, 'matieres') else []

    return render(request, 'professeur/index.html', {
        'professeur': professeur,
        'rapports': rapports,
    })
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from Professeur.models import Note, Rapport

@login_required(login_url='/login/')
def etudiant_dashboard(request):
    # request.user contient l'etudiant connecté
    etudiant = request.user

    # récupère les notes de cet étudiant
    notes = Note.objects.filter(etudiant=etudiant)
    
    # récupère les rapports de cet étudiant
    rapports = Rapport.objects.filter(etudiant=etudiant)

    return render(request, 'etudiant/index.html', {
        'etudiant': etudiant,
        'notes': notes,
        'rapports': rapports,
    })
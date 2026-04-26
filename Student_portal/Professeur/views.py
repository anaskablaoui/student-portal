<<<<<<< HEAD
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
=======
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RapportForm
from .models import Professeur

def rediger_rapport(request):
    # Récupérer le professeur connecté (adapter selon votre auth)
    professeur = Professeur.objects.get(user=request.user)

    if request.method == 'POST':
        form = RapportForm(request.POST, professeur=professeur)
        if form.is_valid():
            rapport = form.save(commit=False)
            rapport.professeur = professeur  # Associer automatiquement le professeur
            rapport.save()
            messages.success(request, 'Rapport rédigé avec succès !')
            return redirect('liste_rapports')  # adapter selon votre URL
    else:
        form = RapportForm(professeur=professeur)

    return render(request, 'professeur/rapport_form.html', {'form': form})
>>>>>>> bc472ec5fdec734df3aae065de484c5e2f6d07b2

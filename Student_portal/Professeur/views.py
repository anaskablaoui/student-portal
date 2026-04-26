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
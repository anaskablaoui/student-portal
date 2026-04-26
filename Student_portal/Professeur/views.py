from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views import View
from authApp.forms import EtudiantLoginForm, ProfesseurLoginForm

def login_view(request):
    etudiant_form = EtudiantLoginForm()
    professeur_form = ProfesseurLoginForm()
    error = None

    if request.method == "POST":
        form_type = request.POST.get("form_type")

        if form_type == "etudiant":
            etudiant_form = EtudiantLoginForm(request.POST)
            if etudiant_form.is_valid():
                matricule = etudiant_form.cleaned_data["matricule"]
                password  = etudiant_form.cleaned_data["password"]
                user = authenticate(request, matricule=matricule, password=password)
                if user is not None:
                    login(request, user)
                    return redirect("etudiant_dashboard")  # → Etudiant/views.py
                else:
                    error = "Matricule ou mot de passe incorrect"

        elif form_type == "professeur":
            professeur_form = ProfesseurLoginForm(request.POST)
            if professeur_form.is_valid():
                matricule = professeur_form.cleaned_data["matricule"]
                password  = professeur_form.cleaned_data["password"]
                user = authenticate(request, matricule=matricule, password=password)
                if user is not None:
                    login(request, user)
                    return redirect("professeur_dashboard")  # → Professeur/views.py
                else:
                    error = "Matricule ou mot de passe incorrect"

    return render(request, 'accounts/login.html', {
        'etudiant_form': etudiant_form,
        'professeur_form': professeur_form,
        'error': error,
    })


def etudiantLogout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('login')
    return redirect('etudiant_dashboard')


def professeurLogout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('login')
    return redirect('professeur_dashboard')

class HomeView(View):
    def get(self,request):
        return render(request,'template/index.html')
    

@login_required(login_url='/login/')
def professeur_dashboard(request):
    professeur = request.user
    rapports = Rapport.objects.filter(professeur=professeur)

    return render(request, 'professeur/index.html', {
        'professeur': professeur,
        'rapports': rapports,
    })
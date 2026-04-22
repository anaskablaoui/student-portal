from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .forms import EtudiantLoginForm,ProfesseurLoginForm

# Create your views here.
#etudiant login views
def login_view(request):
    etudiant_form = EtudiantLoginForm()
    professeur_form = ProfesseurLoginForm()

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
                    return redirect("home")

        elif form_type == "professeur":
            professeur_form = ProfesseurLoginForm(request.POST)
            if professeur_form.is_valid():
                matricule = professeur_form.cleaned_data["matricule"]
                password  = professeur_form.cleaned_data["password"]
                user = authenticate(request, matricule=matricule, password=password)
                if user is not None:
                    login(request, user)
                    return redirect("home")

    return render(request, 'accounts/login.html', {
        'etudiant_form': etudiant_form,
        'professeur_form': professeur_form,
    })
    
def etudiantLogout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('login')
    else:
        return redirect('home')

#professeur login views




def professeurLogout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("login")
    return redirect("home")




#homeView
@login_required
def home_view(request):
    return render(request, 'home/home.html')

# protected View

class ProtectedView(LoginRequiredMixin,View):
    login_url = '/login/'
    
    redirect_field_name='redirected_to'
    
    def get(self,request):
        return render(request, 'registration/protected.html')
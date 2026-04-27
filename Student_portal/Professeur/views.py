from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views import View
from authApp.forms import EtudiantLoginForm, ProfesseurLoginForm

def dashboard(request):
    return render(request, 'professeur/dashboard.html')
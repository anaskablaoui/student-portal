from django.urls import path
from . import views
from authApp import views as authentification
urlpatterns = [
    path('Dashboard/', views.dashboard, name='dashboard'),
    path('login/',authentification.login_view ,name='login')
]
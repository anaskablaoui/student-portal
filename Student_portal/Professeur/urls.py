from django.urls import path
from . import views
from authApp import views as authentification

app_name = 'professeur'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', authentification.professeurLogout_view, name='logout'),
    path('sessions-json/', views.calendrier_events, name='sessions_json'),
]
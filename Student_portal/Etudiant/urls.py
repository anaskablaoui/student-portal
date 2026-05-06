from django.urls import path
from . import views
from authApp.views import professeurLogout_view
urlpatterns = [
    path('dashboard/', views.etudiant_dashboard, name='etudiant_dashboard'),
    path('dashboard/logout',professeurLogout_view,name='logout'),
    #('sessions_json/', views.sessions_json, name='sessions_json'),
    path('statistics/', views.statistics, name='statistics'),
]
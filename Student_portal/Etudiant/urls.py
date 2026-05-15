from django.urls import path
from . import views
from authApp.views import professeurLogout_view
urlpatterns = [
    path('dashboard/', views.etudiant_dashboard, name='etudiant_dashboard'),
    path('dashboard/logout',professeurLogout_view,name='logout'),
    path('events/', views.calendrier_events, name='etudiant_events'),
    path('bulltinNote/',views.Bulletin,name="imprimerBultin"),
    path('statistiques/', views.statistiques_notes, name='etudiant_stats'),
]
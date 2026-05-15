from django.urls import path
from . import views
from authApp import views as authentification

app_name = 'professeur'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', authentification.professeurLogout_view, name='logout'),
    path('statistiques-groupes/',views.statistiques_groupes,name='statistiques_groupes'),
    path('doughnot-data/', views.doughnat_presance, name='doughnut_data'),  
]
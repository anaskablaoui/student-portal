from django.urls import path
from . import views
from Professeur.views import dashboard

urlpatterns = [
    path('',views.login_view,name="login"),
    path('logout/etudiant/', views.etudiantLogout_view, name='etudiantLogout'),
    path('professeur/dashboard',dashboard,name="dashboard")
]

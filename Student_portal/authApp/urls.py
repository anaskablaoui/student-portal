from django.urls import path
from . import views

urlpatterns = [
    path('',views.login_view,name="login"),
    path('logout/etudiant/', views.etudiantLogout_view, name='etudiantLogout'),
]

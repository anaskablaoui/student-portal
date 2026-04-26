from Etudiant.models import Etudiant
from Professeur.models import Professeur

class EtudiantBackend:
    def authenticate(self, request, matricule=None, password=None, **kwargs):
        try:
            user = Etudiant.objects.get(matricule=matricule)
            if user.check_password(password):
                return user
        except Etudiant.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Etudiant.objects.get(pk=user_id)
        except Etudiant.DoesNotExist:
            return None


class ProfesseurBackend:
    def authenticate(self, request, matricule=None, password=None, **kwargs):
        try:
            user = Professeur.objects.get(matricule=matricule)
            if user.check_password(password):
                return user
        except Professeur.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Professeur.objects.get(pk=user_id)
        except Professeur.DoesNotExist:
            return None
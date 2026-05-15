from django.core.management.base import BaseCommand
from faker import Faker
import random
from datetime import datetime, date, timedelta

# Models
from Administrateur.models import Filier, Module, Groupe, Matiere, Salle, Session, Administrateur
from authApp.models import custumUser
from Etudiant.models import Etudiant
from Professeur.models import Professeur, absence, Message, Rapport, Note

class Command(BaseCommand):
    help = 'Génère de fausses données de test (20 étudiants, 9 groupes, 10 professeurs, 3 filières, séances en 2026, mot de passe password)'

    def handle(self, *args, **kwargs):
        faker = Faker('fr_FR')

        # 1. Filières
        self.stdout.write("Création des Filières...")
        filieres_names = [
            'Informatique et Réseaux',
            'Gestion des Entreprises',
            'Sciences et Technologies'
        ]
        filieres = []
        for nom in filieres_names:
            filieres.append(Filier.objects.create(nom=nom))

        # 2. Modules
        self.stdout.write("Création des Modules...")
        modules = []
        module_names = [
            'Programmation Avancée',
            'Base de Données',
            'Analyse Financière',
            'Marketing Digital',
            'Mathématiques Appliquées',
            'Physique Informatique',
            'Systèmes d’Information',
            'Économie d’Entreprise',
            'Sécurité des Réseaux'
        ]
        for i, nom in enumerate(module_names):
            module = Module.objects.create(
                nom=nom,
                filiere=filieres[i % len(filieres)]
            )
            modules.append(module)

        # 3. Matières
        self.stdout.write("Création des Matières...")
        matiere_names = [
            'Développement web',
            'Structures de données',
            'Systèmes d’exploitation',
            'Administration des bases de données',
            'Gestion de projet',
            'Comptabilité',
            'Statistiques',
            'Mathématiques financières',
            'Physique appliquée',
            'Algèbre linéaire',
            'Réseau et sécurité',
            'Intelligence artificielle',
            'Design d’interface',
            'Droit du numérique',
            'Entrepreneuriat'
        ]
        matieres = []
        for i, nom in enumerate(matiere_names):
            matieres.append(Matiere.objects.create(
                nom=nom,
                module=modules[i % len(modules)]
            ))

        # 4. Groupes
        self.stdout.write("Création des Groupes...")
        groupes = []
        groupe_labels = [
            'G1A', 'G1B', 'G1C',
            'G2A', 'G2B', 'G2C',
            'G3A', 'G3B', 'G3C'
        ]
        for i, label in enumerate(groupe_labels):
            groupes.append(Groupe.objects.create(
                nom=label,
                filier=filieres[i % len(filieres)]
            ))

        # 5. Salles
        self.stdout.write("Création des Salles...")
        salles = []
        for i in range(1, 11):
            salles.append(Salle.objects.create(num=100 + i))

        # 6. Utilisateurs et rôles
        self.stdout.write("Création des Utilisateurs et Rôles...")

        self.stdout.write("  Création des Administrateurs...")
        admins = []
        for i in range(3):
            user = custumUser.objects.create_user(
                matricule=f'A-{faker.unique.numerify(text="#######")}',
                email=faker.unique.email()[:50],
                password='password',
                nom=faker.last_name()[:50],
                prenom=faker.first_name()[:50],
                role='administrateur'
            )
            a = Administrateur.objects.create(
                user=user,
                niveau_acces=random.randint(1, 5)
            )
            admins.append(a)

        self.stdout.write("  Création des Professeurs...")
        professeurs = []
        for i in range(10):
            user = custumUser.objects.create_user(
                matricule=f'P-{faker.unique.numerify(text="#######")}',
                email=faker.unique.email()[:50],
                password='password',
                nom=faker.last_name()[:50],
                prenom=faker.first_name()[:50],
                role='professeur'
            )
            p = Professeur.objects.create(
                user=user,
                CIN=faker.unique.lexify(text='??######').upper()
            )
            p.groupe.add(*random.sample(groupes, random.randint(1, 3)))
            professeurs.append(p)

        self.stdout.write("  Création des Étudiants...")
        etudiants = []
        for i in range(20):
            user = custumUser.objects.create_user(
                matricule=f'E-{faker.unique.numerify(text="#######")}',
                email=faker.unique.email()[:50],
                password='password',
                nom=faker.last_name()[:50],
                prenom=faker.first_name()[:50],
                role='etudiant'
            )
            etudiants.append(Etudiant.objects.create(
                user=user,
                CIN=faker.unique.lexify(text='??######').upper(),
                date_naissance=faker.date_of_birth(minimum_age=18, maximum_age=24),
                groupe=random.choice(groupes)
            ))

        all_users = list(custumUser.objects.all())

        # 7. Sessions en 2026
        self.stdout.write("Création des Sessions 2026...")
        sessions = []
        for i in range(20):
            start_hour = random.randint(8, 16)
            start_minute = random.choice([0, 15, 30, 45])
            heure_depart = datetime(2026, 1, 1, start_hour, start_minute).time()
            duree = random.choice([1, 2, 3])
            heure_fin = (datetime(2026, 1, 1, start_hour, start_minute) + timedelta(hours=duree)).time()
            date_session = faker.date_between(start_date=date(2026, 1, 1), end_date=date(2026, 12, 31))
            sessions.append(Session.objects.create(
                matiere=random.choice(matieres),
                groupe=random.choice(groupes),
                date=date_session,
                heure_depart=heure_depart,
                heure_fin=heure_fin
            ))

        # 8. Absences
        self.stdout.write("Création des Absences...")
        for i in range(30):
            absence.objects.create(
                seance=random.choice(sessions),
                etudiant=random.choice(etudiants),
                status=random.choice([True, False])
            )

        # 9. Messages
        self.stdout.write("Création des Messages...")
        for i in range(20):
            Message.objects.create(
                user=random.choice(all_users),
                description=faker.sentence(nb_words=12)[:200],
                type=random.choice(['question', 'annonce', 'demande']),
                obj=faker.sentence(nb_words=4)[:150]
            )

        # 10. Rapports
        self.stdout.write("Création des Rapports...")
        for i in range(20):
            Rapport.objects.create(
                etudiant=random.choice(etudiants),
                professeur=random.choice(professeurs),
                description=faker.paragraph(nb_sentences=2)[:200],
                date=faker.date_between(start_date=date(2026, 1, 1), end_date=date(2026, 12, 31))
            )

        # 11. Notes
        self.stdout.write("Création des Notes...")
        for i in range(30):
            Note.objects.create(
                etudiant=random.choice(etudiants),
                matiere=random.choice(matieres),
                note=round(random.uniform(5, 20), 2)
            )

        self.stdout.write(self.style.SUCCESS('Les données de test ont été générées avec succès !'))

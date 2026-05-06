from django.core.management.base import BaseCommand
from faker import Faker
import random
from datetime import timedelta

# Models
from Administrateur.models import Filier, Module, Groupe, Matiere, Salle, Session, Administrateur
from authApp.models import custumUser
from Etudiant.models import Etudiant
from Professeur.models import Professeur, absence, Message, Rapport, Note

class Command(BaseCommand):
    help = 'Génère 10 fausses données par classe avec le mot de passe "password"'

    def handle(self, *args, **kwargs):
        faker = Faker('fr_FR')

        # 1. Filier
        self.stdout.write("Création des Filières...")
        filieres = []
        for i in range(10):
            f = Filier.objects.create(nom=faker.unique.job()[:50])
            filieres.append(f)
        
        # 2. Salle
        self.stdout.write("Création des Salles...")
        salles = []
        for i in range(10):
            s = Salle.objects.create(num=faker.unique.random_int(min=1, max=9999))
            salles.append(s)

        # 3. Module
        self.stdout.write("Création des Modules...")
        modules = []
        for i in range(10):
            m = Module.objects.create(
                nom=faker.word()[:50],
                filiere=random.choice(filieres)
            )
            modules.append(m)

        # 4. Groupe
        self.stdout.write("Création des Groupes...")
        groupes = []
        for i in range(10):
            g = Groupe.objects.create(
                nom=faker.unique.lexify(text='??????').upper(),
                filier=random.choice(filieres)
            )
            groupes.append(g)

        # 5. Matiere
        self.stdout.write("Création des Matières...")
        matieres = []
        for i in range(10):
            mat = Matiere.objects.create(
                nom=faker.word()[:50],
                module=random.choice(modules)
            )
            matieres.append(mat)

        # Users and Roles
        self.stdout.write("Création des Utilisateurs et Rôles...")
        # 10 Administrateurs
        admins = []
        for i in range(10):
            user = custumUser.objects.create_user(
                matricule=faker.unique.numerify(text='M-#######'),
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

        # 10 Etudiants
        etudiants = []
        for i in range(10):
            user = custumUser.objects.create_user(
                matricule=faker.unique.numerify(text='E-#######'),
                email=faker.unique.email()[:50],
                password='password',
                nom=faker.last_name()[:50],
                prenom=faker.first_name()[:50],
                role='etudiant'
            )
            e = Etudiant.objects.create(
                user=user,
                CIN=faker.unique.lexify(text='??######').upper(),
                date_naissance=faker.date_of_birth(minimum_age=18, maximum_age=30),
                groupe=random.choice(groupes)
            )
            etudiants.append(e)

        # 10 Professeurs
        professeurs = []
        for i in range(10):
            user = custumUser.objects.create_user(
                matricule=faker.unique.numerify(text='P-#######'),
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
            p.groupe.add(*random.sample(groupes, random.randint(1, min(3, len(groupes)))))
            professeurs.append(p)

        all_users = list(custumUser.objects.all())

        # 6. Session
        self.stdout.write("Création des Sessions...")
        sessions = []
        for i in range(10):
            heure_depart = faker.time_object()
            heure_fin = (faker.date_time() + timedelta(hours=2)).time()
            s = Session.objects.create(
                matiere=random.choice(matieres),
                groupe=random.choice(groupes),
                date=faker.date_between(start_date='-1y', end_date='today'),
                heure_depart=heure_depart,
                heure_fin=heure_fin
            )
            sessions.append(s)

        # 7. Absence
        self.stdout.write("Création des Absences...")
        for i in range(10):
            absence.objects.create(
                seance=random.choice(sessions),
                etudiant=random.choice(etudiants),
                status=faker.boolean()
            )

        # 8. Message
        self.stdout.write("Création des Messages...")
        for i in range(10):
            Message.objects.create(
                user=random.choice(all_users),
                description=faker.sentence()[:200]
            )

        # 9. Rapport
        self.stdout.write("Création des Rapports...")
        for i in range(10):
            Rapport.objects.create(
                etudiant=random.choice(etudiants),
                professeur=random.choice(professeurs),
                description=faker.sentence()[:200],
                date=faker.date_between(start_date='-1y', end_date='today')
            )

        # 10. Note
        self.stdout.write("Création des Notes...")
        for i in range(10):
            Note.objects.create(
                etudiant=random.choice(etudiants),
                matiere=random.choice(matieres),
                note=round(random.uniform(0, 20), 2)
            )

        self.stdout.write(self.style.SUCCESS('Les données ont été générées avec succès !'))
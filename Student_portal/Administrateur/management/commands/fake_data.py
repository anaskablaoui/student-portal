from django.core.management.base import BaseCommand
from faker import Faker
from Administrateur.models import *
import random

class Filier(BaseCommand):
    help='genere les donne de filiere'

    def hadle(self,*args,**options):
        faker=Faker('fr_FR')

        filieres=[]

        for _ in range(3)
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.conf import settings
from djongo import models
from pymongo import MongoClient

# MODELS (simples, inline pour la commande, à remplacer par de vraies apps/models.py si besoin)
from django.db import models as dj_models

class Team(dj_models.Model):
    name = dj_models.CharField(max_length=100, unique=True)
    class Meta:
        app_label = 'octofit_tracker'

class Activity(dj_models.Model):
    user = dj_models.CharField(max_length=100)
    type = dj_models.CharField(max_length=100)
    duration = dj_models.IntegerField()
    class Meta:
        app_label = 'octofit_tracker'

class Leaderboard(dj_models.Model):
    user = dj_models.CharField(max_length=100)
    score = dj_models.IntegerField()
    class Meta:
        app_label = 'octofit_tracker'

class Workout(dj_models.Model):
    name = dj_models.CharField(max_length=100)
    description = dj_models.TextField()
    class Meta:
        app_label = 'octofit_tracker'

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Nettoyage
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()

        # Création des équipes
        marvel = Team.objects.create(name='Marvel')
        dc = Team.objects.create(name='DC')

        # Utilisateurs super héros
        users = [
            {'username': 'ironman', 'email': 'ironman@marvel.com', 'team': marvel},
            {'username': 'spiderman', 'email': 'spiderman@marvel.com', 'team': marvel},
            {'username': 'batman', 'email': 'batman@dc.com', 'team': dc},
            {'username': 'superman', 'email': 'superman@dc.com', 'team': dc},
        ]
        user_objs = []
        for u in users:
            user = User.objects.create_user(username=u['username'], email=u['email'], password='password123')
            user_objs.append(user)

        # Création d'un index unique sur le champ email de la collection users
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']
        db['auth_user'].create_index([('email', 1)], unique=True)
        client.close()

        # Activités
        Activity.objects.create(user='ironman', type='run', duration=30)
        Activity.objects.create(user='spiderman', type='swim', duration=45)
        Activity.objects.create(user='batman', type='cycle', duration=60)
        Activity.objects.create(user='superman', type='fly', duration=120)

        # Leaderboard
        Leaderboard.objects.create(user='ironman', score=100)
        Leaderboard.objects.create(user='spiderman', score=80)
        Leaderboard.objects.create(user='batman', score=90)
        Leaderboard.objects.create(user='superman', score=110)

        # Workouts
        Workout.objects.create(name='Cardio Blast', description='High intensity cardio workout')
        Workout.objects.create(name='Strength Training', description='Full body strength routine')

        self.stdout.write(self.style.SUCCESS('octofit_db has been populated with test data.'))

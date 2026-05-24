from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from octofit_tracker.models import Team, Activity, Leaderboard, Workout


class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Clear existing data
        Leaderboard.objects.all().delete()
        Activity.objects.all().delete()
        Workout.objects.all().delete()
        Team.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()

        # Create teams
        team_marvel = Team.objects.create(name='Team Marvel', description='Marvel superheroes fitness team')
        team_dc = Team.objects.create(name='Team DC', description='DC superheroes fitness team')

        # Create users (superheroes)
        heroes = [
            {'username': 'ironman',    'email': 'ironman@marvel.com',    'first_name': 'Tony',   'last_name': 'Stark',   'team': team_marvel},
            {'username': 'spiderman',  'email': 'spiderman@marvel.com',  'first_name': 'Peter',  'last_name': 'Parker',  'team': team_marvel},
            {'username': 'thor',       'email': 'thor@marvel.com',       'first_name': 'Thor',   'last_name': 'Odinson', 'team': team_marvel},
            {'username': 'batman',     'email': 'batman@dc.com',         'first_name': 'Bruce',  'last_name': 'Wayne',   'team': team_dc},
            {'username': 'superman',   'email': 'superman@dc.com',       'first_name': 'Clark',  'last_name': 'Kent',    'team': team_dc},
            {'username': 'wonderwoman','email': 'wonderwoman@dc.com',    'first_name': 'Diana',  'last_name': 'Prince',  'team': team_dc},
        ]

        for hero in heroes:
            team = hero.pop('team')
            user = User.objects.create_user(
                username=hero['username'],
                email=hero['email'],
                password='octofit2024',
                first_name=hero['first_name'],
                last_name=hero['last_name'],
            )
            # Create activities for each hero
            Activity.objects.create(user=user, team=team, type='run',      duration=30, points=30)
            Activity.objects.create(user=user, team=team, type='strength', duration=45, points=45)

        # Create workouts
        Workout.objects.create(name='Morning Run',    description='5km morning run for cardio')
        Workout.objects.create(name='Strength Training', description='Full body strength workout')
        Workout.objects.create(name='Yoga Flow',      description='Relaxing yoga session for flexibility')

        # Create leaderboard entries
        marvel_points = sum(
            Activity.objects.filter(team=team_marvel).values_list('points', flat=True)
        )
        dc_points = sum(
            Activity.objects.filter(team=team_dc).values_list('points', flat=True)
        )
        Leaderboard.objects.create(team=team_marvel, total_points=marvel_points, month='2024-05')
        Leaderboard.objects.create(team=team_dc,     total_points=dc_points,     month='2024-05')

        self.stdout.write(self.style.SUCCESS('Successfully populated octofit_db with test data!'))

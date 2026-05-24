from django.db import models
from django.contrib.auth.models import User

class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    def __str__(self):
        return self.name

class Workout(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    # Optionally, suggested_for = models.ManyToManyField(Team, blank=True)
    def __str__(self):
        return self.name

class Activity(models.Model):
    ACTIVITY_TYPES = [
        ('run', 'Run'),
        ('walk', 'Walk'),
        ('strength', 'Strength'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    date = models.DateTimeField(auto_now_add=True)
    points = models.IntegerField(default=0)
    def __str__(self):
        return f"{self.user.username} - {self.type} - {self.duration}min"

class Leaderboard(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    total_points = models.IntegerField(default=0)
    month = models.CharField(max_length=20)
    def __str__(self):
        return f"{self.team.name} - {self.month}"

from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import connection
from djongo import models

# Sample data for population
USERS = [
    {"name": "Superman", "email": "superman@dc.com", "team": "dc"},
    {"name": "Batman", "email": "batman@dc.com", "team": "dc"},
    {"name": "Wonder Woman", "email": "wonderwoman@dc.com", "team": "dc"},
    {"name": "Iron Man", "email": "ironman@marvel.com", "team": "marvel"},
    {"name": "Captain America", "email": "cap@marvel.com", "team": "marvel"},
    {"name": "Black Widow", "email": "widow@marvel.com", "team": "marvel"},
]
TEAMS = [
    {"name": "marvel"},
    {"name": "dc"},
]
ACTIVITIES = [
    {"user": "superman@dc.com", "activity": "flight", "duration": 60},
    {"user": "ironman@marvel.com", "activity": "fly suit", "duration": 45},
]
LEADERBOARD = [
    {"user": "superman@dc.com", "score": 100},
    {"user": "ironman@marvel.com", "score": 95},
]
WORKOUTS = [
    {"name": "Strength Training", "suggested_for": "dc"},
    {"name": "Tech Circuit", "suggested_for": "marvel"},
]

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        db = connection.cursor().db_conn
        # Drop collections if they exist
        for col in ["users", "teams", "activities", "leaderboard", "workouts"]:
            db[col].drop()
        # Insert test data
        db["users"].insert_many(USERS)
        db["teams"].insert_many(TEAMS)
        db["activities"].insert_many(ACTIVITIES)
        db["leaderboard"].insert_many(LEADERBOARD)
        db["workouts"].insert_many(WORKOUTS)
        # Unique index on email
        db["users"].create_index([("email", 1)], unique=True)
        self.stdout.write(self.style.SUCCESS('octofit_db populated with test data'))

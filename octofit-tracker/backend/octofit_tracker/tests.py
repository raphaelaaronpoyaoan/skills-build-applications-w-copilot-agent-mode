from django.test import TestCase
from .models import User, Team, Activity, Workout, Leaderboard

class ModelSmokeTest(TestCase):
    def test_team_create(self):
        team = Team.objects.create(name='Test Team')
        self.assertEqual(str(team), 'Test Team')

    def test_user_create(self):
        team = Team.objects.create(name='Test Team')
        user = User.objects.create_user(username='testuser', email='test@example.com', password='pass', team=team)
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.team, team)

    def test_activity_create(self):
        team = Team.objects.create(name='Test Team')
        user = User.objects.create_user(username='testuser', email='test@example.com', password='pass', team=team)
        activity = Activity.objects.create(user=user, type='run', duration=10, distance=2.5)
        self.assertEqual(activity.type, 'run')

    def test_workout_create(self):
        workout = Workout.objects.create(name='Test Workout', description='desc')
        self.assertEqual(workout.name, 'Test Workout')

    def test_leaderboard_create(self):
        team = Team.objects.create(name='Test Team')
        user = User.objects.create_user(username='testuser', email='test@example.com', password='pass', team=team)
        lb = Leaderboard.objects.create(user=user, score=42)
        self.assertEqual(lb.score, 42)

    def test_api_root_uses_codespace_https(self):
        """When CODESPACE_NAME is set, the API root should return HTTPS URLs pointing to the Codespace public host."""
        import os
        from django.test import Client

        os.environ['CODESPACE_NAME'] = 'my-fake-codespace'
        client = Client()
        resp = client.get('/api/')
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue(data['users'].startswith('https://my-fake-codespace-8000.app.github.dev'))

"""octofit_tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

import os
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.response import Response
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'teams', views.TeamViewSet, basename='team')
router.register(r'activities', views.ActivityViewSet, basename='activity')
router.register(r'workouts', views.WorkoutViewSet, basename='workout')
router.register(r'leaderboard', views.LeaderboardViewSet, basename='leaderboard')


def _base_url(request=None):
    """Return the base URL for API links.

    Priority:
      1. Use CODESPACE_NAME env var if present
      2. Use the request Host header if it looks like an app.github.dev host
      3. Fallback to http://localhost:8000
    """
    codespace = os.environ.get('CODESPACE_NAME')
    if codespace:
        return f"https://{codespace}-8000.app.github.dev"

    # If a request is available and its Host header looks like a Codespace forwarded host,
    # prefer that host (keeps URLs accurate when accessed via the Codespace public hostname).
    if request:
        host = request.get_host()
        if host.endswith('app.github.dev'):
            # Use https scheme for Codespace public hosts
            return f"https://{host}"

    # Fallback to local development
    return "http://localhost:8000"


def custom_api_root(request, format=None):
    base = _base_url(request)
    return Response({
        'users': f"{base}/api/users/",
        'teams': f"{base}/api/teams/",
        'activities': f"{base}/api/activities/",
        'workouts': f"{base}/api/workouts/",
        'leaderboard': f"{base}/api/leaderboard/",
    })


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/', custom_api_root, name='api-root'),
    path('', custom_api_root, name='root'),
]

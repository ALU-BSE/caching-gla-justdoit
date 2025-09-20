from django.urls import path, include
from rest_framework import routers

from users.views import UserViewSet
from users.cache_views import cache_stats

router = routers.DefaultRouter()
router.register(r'', UserViewSet)

urlpatterns = [
    path('cache-stats/', cache_stats, name='cache-stats'),
] + router.urls
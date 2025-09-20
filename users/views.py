from django.shortcuts import render
from django.core.cache import cache
from django.conf import settings
from rest_framework import viewsets
from rest_framework.response import Response

from users.models import User
from users.serializers import UserSerializer
from users.cache_utils import cache_performance


# Create your views here.

def get_cache_key(prefix, identifier=None):
    if identifier:
        return f"{prefix}_{identifier}"
    return prefix


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @cache_performance("user_list_cache")
    def list(self, request, *args, **kwargs):
        cache_key = get_cache_key('user_list')
        cached_data = cache.get(cache_key)
        
        if cached_data is not None:
            return Response(cached_data)
        
        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=settings.CACHE_TTL)
        
        return response

    @cache_performance("user_detail_cache")
    def retrieve(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        cache_key = get_cache_key('user', user_id)
        cached_data = cache.get(cache_key)
        
        if cached_data is not None:
            return Response(cached_data)
        
        response = super().retrieve(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=settings.CACHE_TTL)
        
        return response

    def perform_create(self, serializer):
        cache.delete('user_list')
        super().perform_create(serializer)

    def perform_update(self, serializer):
        user_id = serializer.instance.id
        cache.delete('user_list')
        cache.delete(f'user_{user_id}')
        super().perform_update(serializer)

    def perform_destroy(self, instance):
        user_id = instance.id
        cache.delete('user_list')
        cache.delete(f'user_{user_id}')
        super().perform_destroy(instance)
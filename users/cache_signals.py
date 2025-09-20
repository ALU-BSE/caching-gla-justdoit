
from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import User

@receiver(post_save, sender=User)
def invalidate_user_cache(sender, instance, **kwargs):
    """Clear user caches when a user is created or updated"""
    # Clear list cache
    cache.delete('user_list')
    # Clear individual user cache
    cache.delete(f'user_{instance.id}')

@receiver(post_delete, sender=User)  
def invalidate_user_cache_on_delete(sender, instance, **kwargs):
    """Clear user caches when a user is deleted"""
    # Clear list cache
    cache.delete('user_list')
    # Clear individual user cache
    cache.delete(f'user_{instance.id}')

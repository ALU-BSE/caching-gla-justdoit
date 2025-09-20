from django.core.management.base import BaseCommand
from django.core.cache import cache
from django.conf import settings
from users.models import User
from users.serializers import UserSerializer

class Command(BaseCommand):
    help = 'Warm up the cache with frequently accessed data'

    def handle(self, *args, **options):
        self.stdout.write('Starting cache warming...')
        
        try:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            cache.set('user_list', serializer.data, timeout=3600)
            self.stdout.write(f'Cached user list with {len(users)} users')
            
            cached_users = 0
            for user in users:
                user_data = UserSerializer(user).data
                cache.set(f'user_{user.id}', user_data, timeout=3600)
                cached_users += 1
            
            self.stdout.write(f'Cached {cached_users} individual users')
            self.stdout.write(
                self.style.SUCCESS(f'Successfully warmed cache with {len(users)} users')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error warming cache: {str(e)}')
            )

from django.core.cache import cache
from rest_framework.decorators import api_view
from rest_framework.response import Response
import redis

@api_view(['GET'])
def cache_stats(request):
    try:
        r = redis.Redis(host='127.0.0.1', port=6379, db=1)
        cache_keys = r.keys('*')
        cache_keys_str = [key.decode('utf-8') for key in cache_keys]
        info = r.info()
        
        return Response({
            'cache_keys': cache_keys_str,
            'total_keys': len(cache_keys_str),
            'redis_version': info.get('redis_version', 'Unknown'),
            'used_memory': info.get('used_memory_human', 'Unknown'),
            'connected_clients': info.get('connected_clients', 0),
            'total_commands_processed': info.get('total_commands_processed', 0),
            'keyspace_hits': info.get('keyspace_hits', 0),
            'keyspace_misses': info.get('keyspace_misses', 0),
        })
    except Exception as e:
        return Response({
            'error': f'Unable to connect to Redis: {str(e)}',
            'cache_keys': [],
            'total_keys': 0
        })

#!/usr/bin/env python3
import requests
import time
import sys

def test_cache_performance():
    url = "http://localhost:8000/api/users/"
    
    print("Testing cache performance...")
    print("=" * 50)
    
    try:
        print("Making first API call (cache miss)...")
        start = time.time()
        response1 = requests.get(url)
        time1 = time.time() - start
        
        if response1.status_code != 200:
            print(f"Error: API returned status code {response1.status_code}")
            return
            
        print("Making second API call (cache hit)...")
        start = time.time()
        response2 = requests.get(url)
        time2 = time.time() - start
        
        if response2.status_code != 200:
            print(f"Error: API returned status code {response2.status_code}")
            return
        
        speedup = time1 / time2 if time2 > 0 else float('inf')
        
        print("\nResults:")
        print(f"First call (cache miss):  {time1:.4f}s")
        print(f"Second call (cache hit):  {time2:.4f}s")
        print(f"Speedup:                  {speedup:.2f}x")
        
        if speedup > 1.5:
            print("✅ Cache is working effectively!")
        else:
            print("⚠️  Cache may not be working as expected")
            
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API. Make sure Django server is running on http://localhost:8000")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_cache_performance()

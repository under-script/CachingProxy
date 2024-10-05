from django.http import JsonResponse
import requests
import os
import json
import logging
from urllib.parse import urlparse, urljoin
import hashlib

# Set up logging
logging.basicConfig(level=logging.INFO)

# Directory for caching
CACHE_DIR = 'cache'

# Ensure cache directory exists
os.makedirs(CACHE_DIR, exist_ok=True)


def get_cache_file_path(path, origin_url):
    """Generate a file path for the cached JSON content based on the request path and origin."""
    sanitized_origin = urlparse(origin_url).netloc.replace(':', '_')
    # Use a hash of the path to avoid excessively long file names
    hash_name = hashlib.md5(path.encode('utf-8')).hexdigest()
    return os.path.join(CACHE_DIR, sanitized_origin, f'{hash_name}.json')


def cache_view(request):
    current_path = request.path
    origin_url = os.environ.get('ORIGIN_URL', '')

    # Get the cache file path for the current request, including the origin
    cache_file_path = get_cache_file_path(current_path, origin_url)

    # Ensure the directory for the current origin exists
    os.makedirs(os.path.dirname(cache_file_path), exist_ok=True)

    # Check if the cache file exists
    if os.path.exists(cache_file_path):
        logging.info(f'Cache HIT for {current_path} from origin {origin_url}')
        with open(cache_file_path, 'r', encoding='utf-8') as cache_file:
            content = json.load(cache_file)
            return JsonResponse(content, safe=False, headers={'X-Cache': 'HIT'})

    # If not cached, fetch the data from the origin server
    source_url = f'{origin_url}{current_path}'
    try:
        response = requests.get(source_url)
        response.raise_for_status()  # Raise an error for bad responses (e.g., 404, 500)
        response_data = response.json()

        # Save JSON data to the cache file
        with open(cache_file_path, 'w', encoding='utf-8') as cache_file:
            json.dump(response_data, cache_file)

        logging.info(f'Cache MISS for {current_path} from origin {origin_url} - Saved as JSON')
        return JsonResponse(response_data, safe=False, headers={'X-Cache': 'MISS'})

    except requests.RequestException as e:
        logging.error(f'Error fetching content from {source_url}: {str(e)}')
        # Return error message in JSON format
        return JsonResponse({'error': f'Error fetching content: {str(e)}'}, status=500)

    except json.JSONDecodeError as e:
        logging.error(f'JSON decode error for {source_url}: {str(e)}')
        # Return JSON decode error in JSON format
        return JsonResponse({'error': f'JSON decode error: {str(e)}'}, status=500)

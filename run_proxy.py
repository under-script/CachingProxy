import argparse
import os
import sys
import shutil  # Import shutil for directory removal
from django.core.management import execute_from_command_line

def clear_cache():
    """Clears the entire cache directory."""
    if os.path.exists('cache'):
        shutil.rmtree('cache')
        print("Cache cleared successfully.")
    else:
        print("No cache directory found to clear.")

def main():
    # Set the default settings module for the Django project
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CachingProxyCLI.settings')  # Replace with your actual project name

    # Set up argument parser
    parser = argparse.ArgumentParser(description='Caching Proxy')
    parser.add_argument('--port', type=int, default=8000, help='Port to run the proxy server')
    parser.add_argument('--origin', type=str, help='Origin server URL to proxy')
    parser.add_argument('--clear-cache', action='store_true', help='Clear the cache')

    args = parser.parse_args()

    # Handle --clear-cache command
    if args.clear_cache:
        clear_cache()
        return

    # Check if origin is provided when running the server
    if not args.origin:
        print("Error: --origin must be provided unless --clear-cache is used.")
        return

    # Set the origin URL as an environment variable
    os.environ['ORIGIN_URL'] = args.origin

    # Run Django's development server on the specified port
    execute_from_command_line([sys.argv[0], 'runserver', f'0.0.0.0:{args.port}'])

if __name__ == '__main__':
    main()

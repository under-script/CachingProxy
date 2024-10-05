from django.urls import re_path

from .views import cache_view

# Debugging
print(f'Type of cache_view: {type(cache_view)}')  # Should be <class 'function'>

urlpatterns = [
    re_path(r'^.*$', cache_view, name='cache'),
]

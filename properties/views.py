from django.shortcuts import render

# Create your views here.
# from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from .models import Property

@cache_page(60 * 15)  # Cache for 15 minutes
def property_list(request):
    """
    Returns all properties as JSON with a top-level "data" key.
    Cached in Redis via settings.CACHES.
    """
    qs = Property.objects.all().values(
        "id", "title", "description", "price", "location", "created_at"
    )
    data = list(qs)
    return JsonResponse({"data": data})

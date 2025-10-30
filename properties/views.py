from django.views.decorators.cache import cache_page
from django.http import JsonResponse
from .utils import get_all_properties

@cache_page(60 * 15)
def property_list(request):
    data = get_all_properties()
    return JsonResponse({'properties': data}, safe=True)



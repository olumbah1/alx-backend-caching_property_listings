# properties/views.py
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Property
from .serializers import PropertySerializer


@api_view(['GET'])
@cache_page(60 * 15)  
def property_list(request):
    properties = Property.objects.all()
    serializer = PropertySerializer(properties, many=True)
    return Response(serializer.data)

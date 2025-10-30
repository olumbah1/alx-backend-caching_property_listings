from rest_framework import serializers
from .models import Property


class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ['property_id','title','description',
                  'price','location','created_at']
        
        
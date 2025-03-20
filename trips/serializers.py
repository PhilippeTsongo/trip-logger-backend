from rest_framework import serializers
from .models import Trip
class LocationSerializer(serializers.Serializer):
    lat = serializers.FloatField()
    lon = serializers.FloatField()

class TripSerializer(serializers.Serializer):
    current_location = LocationSerializer()
    pickup_location = LocationSerializer()
    dropoff_location = LocationSerializer()
    current_cycle_hours = serializers.FloatField()

class TripSerializerList(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = '__all__'

from rest_framework import serializers
from .models import Bike, Rental

class BikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bike
        fields = '__all__'

class RentalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rental
        fields = '__all__'

from rest_framework import serializers

from apps.cars.models import CarModel


class CarSerializers(serializers.ModelSerializer):
    class Meta:
        model = CarModel
        fields = ('id', 'post', 'car_brand', 'car_model', 'car_price', 'car_year', 'created_at', 'updated_at')
        read_only_fields = ('post',)
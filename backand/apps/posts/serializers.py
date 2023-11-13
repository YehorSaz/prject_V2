from django.db.transaction import atomic

from rest_framework import serializers

from apps.cars.models import CarModel
from apps.cars.serializers import CarSerializers, CarSerializersForBase
from apps.posts.models import UserPostsModel


class UserPostSerializer(serializers.ModelSerializer):
    car = CarSerializers()

    class Meta:
        model = UserPostsModel
        fields = (
        'id', 'active_status', 'user', 'region', 'city', 'views_count', 'update_count', 'created_at', 'updated_at',
        'car')
        read_only_fields = ('id', 'status', 'views_count', 'update_count', 'created_at', 'updated_at', 'user')




    @atomic
    def create(self, validated_data: dict):
        car = validated_data.pop('car')
        car = CarModel.objects.create(**car)
        post = UserPostsModel.objects.create(car=car, **validated_data)
        return post

    def update(self, instance, validated_data):
        instance.id = validated_data.get("id", instance.id)
        instance.user = validated_data.get("user", instance.user)
        instance.region = validated_data.get("region", instance.region)
        instance.city = validated_data.get("city", instance.city)
        instance.views_count = validated_data.get("views_count", instance.views_count)
        instance.update_count = validated_data.get("update_count", instance.update_count)
        instance.created_at = validated_data.get("created_at", instance.created_at)
        instance.updated_at = validated_data.get("updated_at", instance.updated_at)
        instance.save()
        return instance

class UserPostSerializerForBase(serializers.ModelSerializer):
    car = CarSerializersForBase()

    class Meta:
        model = UserPostsModel
        fields = (
            'id', 'user', 'region', 'city', 'car')

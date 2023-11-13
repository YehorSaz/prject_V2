from django.contrib.auth import get_user_model
from django.db.transaction import atomic

from rest_framework import serializers

from core.services.email_service import EmailService

from apps.posts.serializers import UserPostSerializer
from apps.users.models import ProfileModel

UserModel = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileModel
        fields = ('id', 'name', 'surname', 'age', 'created_at', 'updated_at')


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    posts = UserPostSerializer(read_only=True, many=True)

    class Meta:
        model = UserModel
        fields = ('id', 'email', 'password', 'account_status', 'is_staff', 'is_superuser', 'is_active', 'last_login', 'created_at',
                  'updated_at', 'profile', 'posts'
                  )
        read_only_fields = ('id', 'account_status', 'is_staff', 'is_superuser', 'is_active', 'last_login', 'created_at', 'updated_at')
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }
    @atomic
    def create(self, validated_data: dict):
        profile = validated_data.pop('profile')
        profile = ProfileModel.objects.create(**profile)
        user = UserModel.objects.create_user(profile=profile, **validated_data)
        EmailService.register_email(user)
        return user

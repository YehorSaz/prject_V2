from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator

from rest_framework import status
from rest_framework.generics import GenericAPIView, ListCreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema

from core.permissions import IsSuperUser, IsSuperUserOrWriteOnly

from apps.users.serializers import UserSerializer

UserModel = get_user_model()


@method_decorator(name='post', decorator=swagger_auto_schema(security=[]))
class UserListCreateView(ListCreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsSuperUserOrWriteOnly,)

    def get_queryset(self):
        return UserModel.objects.exclude(pk=self.request.user.pk)


class DeleteUserView(GenericAPIView):
    """
        Delete User by id
    """

    queryset = UserModel.objects.all()
    permission_classes = (IsSuperUser, IsAdminUser)

    def get_serializer(self, *args, **kwargs):
        pass

    def delete(self, *args, **kwargs):
        user = self.get_object()
        user.delete()
        return Response('The User was deleted', status.HTTP_200_OK)


class UserToAdminView(GenericAPIView):
    queryset = UserModel.objects.all()
    permission_classes = (IsSuperUser,)

    def get_serializer(self, *args, **kwargs):
        pass

    def get_queryset(self):
        return super().get_queryset().exclude(pk=self.request.user.pk)

    def patch(self, *args, **kwargs):
        user = self.get_object()
        if not user.is_staff:
            user.is_staff = True
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)


class AdminToUserView(GenericAPIView):
    """
        Set User permission is_staff: False by id
    """
    queryset = UserModel.objects.all()
    permission_classes = (IsSuperUser,)

    def get_serializer(self, *args, **kwargs):
        pass

    def get_queryset(self):
        return super().get_queryset().exclude(pk=self.request.user.pk)

    def patch(self, *args, **kwargs):
        user = self.get_object()
        if user.is_staff:
            user.is_staff = False
            user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)


class BlockUserView(GenericAPIView):
    """
        Block User by id
    """
    queryset = UserModel.objects.all()
    permission_classes = (IsAdminUser,)

    def get_serializer(self, *args, **kwargs):
        pass

    def get_queryset(self):
        return super().get_queryset().exclude(pk=self.request.user.pk)

    def patch(self, *args, **kwargs):
        print(self.request.user)
        user = self.get_object()

        if user.is_active:
            user.is_active = False
            user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)


class UnBlockUserView(GenericAPIView):
    """
        Unblock User by id
    """
    queryset = UserModel.objects.all()
    permission_classes = (IsAdminUser,)

    def get_serializer(self, *args, **kwargs):
        pass

    def get_queryset(self):
        return super().get_queryset().exclude(pk=self.request.user.pk)

    def patch(self, *args, **kwargs):
        user = self.get_object()

        if not user.is_active:
            user.is_active = True
            user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)


class SetAccountStatusPremiumView(UpdateAPIView):
    queryset = UserModel.objects.all()
    permission_classes = (IsAdminUser,)

    def get_serializer(self, *args, **kwargs):
        pass

    def patch(self, request, *args, **kwargs):
        user = self.get_object()
        user.account_status = 'Premium'
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)


class SetAccountStatusBaseView(UpdateAPIView):
    queryset = UserModel.objects.all()
    permission_classes = (IsAdminUser,)

    def get_serializer(self, *args, **kwargs):
        pass

    def patch(self, request, *args, **kwargs):
        user = self.get_object()
        user.account_status = 'Base'
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)

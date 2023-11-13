from django.contrib.auth.models import AnonymousUser
from django.utils.decorators import method_decorator

from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema

from core.pagination import PagePagination
from core.permissions import IsOwner
from core.services.censor_service.censor_service import censor
from core.services.email_service import EmailService

from apps.cars.models import CarModel
from apps.cars.serializers import CarSerializers
from apps.posts.models import UserPostsModel
from apps.posts.serializers import UserPostSerializer, UserPostSerializerForBase
from apps.users.models import UserModel


@method_decorator(name='get', decorator=swagger_auto_schema(security=[]))
class UserPostListView(ListAPIView):
    """
        Get all posts
    """
    # serializer_class = UserPostSerializer
    pagination_class = PagePagination
    permission_classes = (AllowAny,)

    def get_queryset(self):
        if self.request.user.is_staff:
            queryset = UserPostsModel.objects.all()
        else:
            queryset = UserPostsModel.objects.filter(active_status=True)
        return queryset

    def get_serializer(self, *args, **kwargs):
        if str(self.request.user) == 'AnonymousUser' or self.request.user.account_status == 'base':
            serializer_class = UserPostSerializerForBase
        else:
            serializer_class = UserPostSerializer
        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)


class UserAddPostView(GenericAPIView):
    """
        Create post
    """
    permission_classes = (IsAuthenticated,)

    def get_serializer(self, *args, **kwargs):
        pass

    def get_object(self):
        return UserModel.objects.get(pk=self.request.user.pk)

    def post(self, *args, **kwargs):
        user = self.get_object()

        if user.posts.count() >= 1 and user.account_status == 'base':
            return Response('Only 1 post for Base account', status.HTTP_403_FORBIDDEN)

        data = self.request.data
        serializer = UserPostSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)

        post_id = dict(serializer.data)
        post = UserPostsModel.objects.get(pk=post_id['id'])
        censor_count = censor(self.request.data['city'])
        if censor_count == 0:
            post.active_status = True
            post.save()
        else:
            post.active_status = False
            post.save()
            return Response({
                'error': 'Знайдено підозрілу лексику, відредагуйте оголошення, оголошення не активне',
                'data': serializer.data},
                status.HTTP_201_CREATED)
        return Response(serializer.data, status.HTTP_201_CREATED)


class PostRetriveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """
    get:
        Get post by id
    delete:
        Delete post by id
    put:
        Update post by id
    patch:
        Partial update post by id
    """
    permission_classes = [IsAdminUser | IsOwner]
    serializer_class = UserPostSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            queryset = UserPostsModel.objects.all()
        else:
            queryset = UserPostsModel.objects.filter(active_status=True)
        return queryset

    def get(self, *args, **kwargs):
        post = self.get_object()
        post.views_count += 1
        post.save()
        if self.request.user.account_status == 'base':
            serializer = UserPostSerializerForBase(post)
        else:
            serializer = UserPostSerializer(post)
        return Response(serializer.data, status.HTTP_200_OK)

    def delete(self, *args, **kwargs):
        pk = kwargs['pk']
        post = UserPostsModel.objects.get(pk=pk)
        if not self.request.user.id == post.user_id and not self.request.user.is_staff:
            return Response('Forbidden', status.HTTP_403_FORBIDDEN)
        post.delete()
        return Response('Post was deleted', status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        pk = kwargs['pk']

        post = UserPostsModel.objects.get(pk=pk)
        if not self.request.user.id == post.user_id and not self.request.user.is_staff:
            return Response('Forbidden', status.HTTP_403_FORBIDDEN)
        partial = kwargs.pop('partial', False)

        car = CarModel.objects.get(post=pk)
        car_serializer = CarSerializers(car, data=request.data['car'], partial=partial)
        car_serializer.is_valid(raise_exception=True)
        car_serializer.save()

        serializer = self.get_serializer(post, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if post.update_count >= 3:
            EmailService.email_to_admin(post.id)
            return Response('only 3 times', status.HTTP_403_FORBIDDEN)

        post.save()
        censor_count = censor(self.request.data['city'])
        if censor_count == 0:
            post.active_status = True
            post.save()
        else:
            post.active_status = False
            post.update_count += 1
            post.save()
            return Response('Знайдено підозрілу лексику, відредагуйте оголошення, оголошення не активне',
                            status.HTTP_201_CREATED)
        return Response(serializer.data)


class SetPostActiveView(GenericAPIView):
    """
    Set post status "Active"
    """
    queryset = UserPostsModel.objects.all()
    permission_classes = (IsAdminUser,)

    def get_serializer(self, *args, **kwargs):
        pass

    def patch(self, request, *args, **kwargs):
        post = self.get_object()
        post.active_status = True
        post.save()
        serializer = UserPostSerializer(post)
        return Response(serializer.data, status.HTTP_200_OK)


class SetPostInActiveView(GenericAPIView):
    """
    Set post "inActive"
    """
    queryset = UserPostsModel.objects.all()
    permission_classes = (IsAdminUser,)

    def get_serializer(self, *args, **kwargs):
        pass

    def patch(self, request, *args, **kwargs):
        post = self.get_object()
        post.active_status = False
        post.save()
        serializer = UserPostSerializer(post)
        return Response(serializer.data, status.HTTP_200_OK)

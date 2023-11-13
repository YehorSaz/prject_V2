
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema

from core.services.censor_service.censor_service import censor
from core.services.email_service import EmailService

from apps.users.models import UserModel


class EmailToAdminView(GenericAPIView):
    """
        send message to admin about missing car
    """
    permission_classes = (IsAuthenticated,)

    def get_serializer(self, *args, **kwargs):
        pass

    def get_object(self):
        return UserModel.objects.get(pk=self.request.user.pk)

    @swagger_auto_schema(operation_id='send email')
    def post(self, *args, **kwargs):
        user = self.get_object()
        data = self.request.data
        data = ''.join(data['text'])

        censor_count = censor(data)
        if censor_count > 0:
            return Response('Неприпустима лексика', status.HTTP_403_FORBIDDEN)

        EmailService.missing_car({'message': data, 'user_id': user.id, 'user': user})
        return Response('email was sent', status.HTTP_200_OK)

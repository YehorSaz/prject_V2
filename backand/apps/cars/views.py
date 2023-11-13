from django.utils.decorators import method_decorator

from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from drf_yasg.utils import swagger_auto_schema

from core.pagination import PagePagination

from apps.cars.models import CarModel
from apps.cars.serializers import CarSerializers


@method_decorator(name='get', decorator=swagger_auto_schema(security=[]))
class CarListView(ListAPIView):
    """
        Get all cars
    """
    queryset = CarModel.objects.all()
    serializer_class = CarSerializers
    permission_classes = (AllowAny,)
    pagination_class = PagePagination

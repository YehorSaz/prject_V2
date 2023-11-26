from django.urls import path

from apps.cars.views import CarListView

urlpatterns = [
    path('', CarListView.as_view(), name='cars_list')
]

from django.core import validators as V
from django.db import models

from core.enums.regex_enum import RegExEnum
from core.models import BaseModel

from apps.cars.models import CarModel
from apps.posts.choices.region_choices import RegionChoices
from apps.users.models import UserModel


class VisitModel(models.Model):
    class Meta:
        db_table = 'visits'
        ordering = ['id']

    endpoint = models.CharField(max_length=255)
    count = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)


class UserPostsModel(BaseModel):
    class Meta:
        db_table = 'posts'
        ordering = ['id']

    active_status = models.BooleanField(default=False)
    region = models.CharField(max_length=30, choices=RegionChoices.choices)
    city = models.CharField(max_length=30, validators=[
        V.RegexValidator(RegExEnum.CITY.pattern, RegExEnum.CITY.msg)
    ])
    views_count = models.IntegerField(default=0)
    update_count = models.IntegerField(default=0)

    car = models.OneToOneField(CarModel, on_delete=models.CASCADE, related_name='post')
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='posts')

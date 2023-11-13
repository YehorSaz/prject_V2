from datetime import datetime

from django.core import validators as V
from django.db import models

from apps.cars.choices.brand_choices import BrandChoices
from core.enums.regex_enum import RegExEnum
from core.models import BaseModel


class CarModel(BaseModel):
    class Meta:
        db_table = 'cars'
        ordering = ['id']

    car_brand = models.CharField(max_length=30, choices=BrandChoices.choices, validators=[
        V.RegexValidator(RegExEnum.BRAND.pattern, RegExEnum.BRAND.msg)
    ])
    car_model = models.CharField(max_length=30, blank=True)
    car_price = models.IntegerField(validators=[
        V.MinValueValidator(0),
        V.MaxValueValidator(100000000)
    ])
    car_year = models.IntegerField(validators=[
        V.MinValueValidator(1900),
        V.MaxValueValidator(datetime.now().year)
    ])

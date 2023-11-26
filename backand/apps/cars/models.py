from datetime import datetime

from django.core import validators as V
from django.db import models

from core.enums.regex_enum import RegExEnum
from core.models import BaseModel

from apps.cars.choices.brand_choices import BrandChoices
from apps.cars.choices.currencies_choices import CurrenciesChoices


class CarModel(BaseModel):
    class Meta:
        db_table = 'cars'
        ordering = ['id']

    car_brand = models.CharField(max_length=30, choices=BrandChoices.choices, validators=[
        V.RegexValidator(RegExEnum.BRAND.pattern, RegExEnum.BRAND.msg)
    ])
    car_model = models.CharField(max_length=30, blank=True)
    currency = models.CharField(max_length=3, choices=CurrenciesChoices.choices)
    car_price = models.IntegerField(validators=[
        V.MinValueValidator(0),
        V.MaxValueValidator(100000000)
    ])
    price_EUR = models.FloatField(null=True, blank=True, validators=[V.DecimalValidator(10, 2)])
    price_USD = models.FloatField(null=True, blank=True, validators=[V.DecimalValidator(10, 2)])
    price_UAH = models.FloatField(null=True, blank=True, validators=[V.DecimalValidator(10, 2)])
    car_year = models.IntegerField(validators=[
        V.MinValueValidator(1900),
        V.MaxValueValidator(datetime.now().year)
    ])

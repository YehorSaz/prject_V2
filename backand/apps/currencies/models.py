from django.db import models

from core.models import BaseModel


class CurrenciesModel(BaseModel):
    class Meta:
        db_table = 'currencies'
        ordering = ['id']

    EUR = models.FloatField()
    USD = models.FloatField()

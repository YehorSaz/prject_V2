from django.db import models


class CurrenciesChoices(models.TextChoices):
    USD = 'USD',
    EUR = 'EUR',
    UAH = 'UAH'

import requests
from configs.celery import app

# from apps.currencies.models import CurrenciesModel


class CurrenciesService:
    @staticmethod
    @app.task
    def get_currencies():
        url = 'https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5'
        data = requests.get(url).json()
        print(data)


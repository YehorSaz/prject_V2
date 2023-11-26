import requests
from configs.celery import app

from apps.cars.models import CarModel
from apps.currencies.models import CurrenciesModel


class CurrenciesService:
    @staticmethod
    @app.task
    def get_courses():
        url = 'https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5'
        data = requests.get(url).json()
        currencies_obj = CurrenciesModel.objects.all()
        if currencies_obj.count() == 0:
            CurrenciesModel.objects.create(id=1, EUR=data[0]['buy'], USD=data[1]['buy'])
        else:
            currencies_obj.delete()
            CurrenciesModel.objects.create(id=1, EUR=data[0]['buy'], USD=data[1]['buy'])

    @staticmethod
    def update_price_by_id(car_id):
        car = CarModel.objects.get(id=car_id)
        if not CurrenciesModel.objects.filter(id=1).exists():
            CurrenciesService.get_courses()
        course = CurrenciesModel.objects.get(id=1)

        match car.currency:
            case 'USD':
                car.price_EUR = round((course.USD / course.EUR) * car.car_price, 2)
                car.price_USD = round(car.car_price, 2)
                car.price_UAH = round(car.car_price * course.USD, 2)
                car.save()
                return car
            case 'EUR':
                car.price_EUR = round(car.car_price, 2)
                car.price_USD = round((course.EUR / course.USD) * car.car_price, 2)
                car.price_UAH = round(car.car_price * course.EUR, 2)
                car.save()
                return car
            case 'UAH':
                car.price_EUR = round(car.car_price / course.EUR, 2)
                car.price_USD = round(car.car_price / course.USD, 2)
                car.price_UAH = round(car.car_price, 2)
                car.save()
                return car

    @staticmethod
    @app.task
    def auto_update_price():
        if CarModel.objects.all().exists():
            cars = CarModel.objects.all()
            if not CurrenciesModel.objects.filter(id=1).exists():
                CurrenciesService.get_courses()
            for car in cars:
                CurrenciesService.update_price_by_id(car.id)

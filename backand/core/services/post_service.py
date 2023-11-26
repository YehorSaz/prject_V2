class GetAvgPrice:
    @staticmethod
    def get_avg_price(posts, car_brand):
        avg_price_uah = 0
        avg_price_eur = 0
        avg_price_usd = 0
        price_count = 0
        for post in posts:
            if post.car.car_brand == car_brand:
                price_count += 1
                avg_price_uah += post.car.price_UAH
                avg_price_eur += post.car.price_EUR
                avg_price_usd += post.car.price_USD
        try:
            avg_price_uah = round(avg_price_uah / price_count, 2)
            avg_price_eur = round(avg_price_eur / price_count, 2)
            avg_price_usd = round(avg_price_usd / price_count, 2)
        except Exception as e:
            return e
        return {
            'avg_price_uah': avg_price_uah,
            'avg_price_eur': avg_price_eur,
            'avg_price_usd': avg_price_usd
        }



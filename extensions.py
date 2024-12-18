import requests
import json
from config import API_KEY


class APIException(Exception):
    '''Исключение для ошибок API.'''
    pass


class CryptoConverter:
    @staticmethod
    def get_price(base, quote, amount):
        ''' Метод для получения курса валют.
         base: Валюта, цену которой нужно узнать (например, USD).
         quote: Валюта, в которую нужно перевести (например, EUR).
         amount: Количество базовой валюты (например, 10).
         return: Переведенная сумма в валюте quote.
        '''

        url = f'https://min-api.cryptocompare.com/data/price?fsym={base}&tsyms={quote}&api_key={API_KEY}'

        try:
            # Отправка GET запроса на API
            response = requests.get(url)

            # Проверка успешного получения данных
            if response.status_code != 200:
                raise APIException("Ошибка при получении данных с API.")

            # Преобразование строки JSON в Python-словарь
            data = json.loads(response.text)

            # Если валюта не найдена, возвращаем ошибку
            if quote not in data:
                raise APIException(f"Не удалось найти информацию о валюте {quote}")

            # Получаем цену
            price = data[quote]
            return price * amount

        except Exception as e:
            raise APIException(f"Ошибка при запросе: {str(e)}")
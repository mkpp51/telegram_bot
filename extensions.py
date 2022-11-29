import requests
import json
from config import currs


class APIException(Exception):
    pass


class CurrencyExchange:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):

        if quote == base:
            raise APIException(f'Одинаковые валюты!{quote}')

        try:
            quote_ticker = currs[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}!')

        try:
            base_ticker = currs[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}!')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}!')

        r = requests.get(f'https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies/{quote_ticker}/{base_ticker}.json')
        respond = json.loads(r.content)[currs[base]]
        total_base = respond * amount
        total_base = round(total_base, 2)

        return total_base

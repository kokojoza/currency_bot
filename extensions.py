import requests
import config
import json


class APIException(Exception):
    pass


class СurrencyСonverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):

        if quote == base:
            raise APIException('Ну зачем! Одинаковое жеж')

        if int(amount) == 0:
            raise APIException('Количество равно 0')

        try:
            quote_cur = config.currency[quote]
            base_cur = config.currency[base]
            amount = float(amount)
        except KeyError as e:
            raise APIException(f'Не удалось обработать валюту {e.args[0]}')
        except ValueError:
            raise APIException(f'Не удалось обработать кол-во {amount}')

        url_apilayer = f"https://api.apilayer.com/exchangerates_data/convert?to={quote_cur}&from={base_cur}&amount={amount}"
        response = requests.request("GET", url_apilayer, headers=config.headers_apilayer)

        status_code = response.status_code
        if status_code == 200:
            return json.loads(response.content)['result']
        else:
            raise APIException(f'Что-то с apilayer')

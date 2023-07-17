from integration_utils.bitrix_robots.models import BaseRobot
import requests as req
from datetime import datetime


class CurrencyRobot(BaseRobot):
    CODE = 'currency_robot'
    NAME = 'Робот возвращает текущий курс валюты по ЦБРФ'

    PROPERTIES = {
        'user': {
            'Name': {'ru': 'Получатель'},
            'Value': {'ru': 'Ответственный'},
            'Type': 'user',
            'Required': 'Y',
        },
        'valute': {
            'Name': {'ru': 'Валюты'},
            'Type': 'select',
            'Options': {'USD/EUR': 'Доллар/Евро',
                        'CNY/USD': 'Юань/Доллар',
                        'CNY/EUR': 'Юань/Евро'},
            'Required': 'Y',
        },
    }

    RETURN_PROPERTIES = {
        'ok': {
            'Name': {'ru': 'ok'},
            'Type': 'bool',
            'Required': 'Y',
        },
        'error': {
            'Name': {'ru': 'error'},
            'Type': 'string',
            'Required': 'N',
        },
    }

    def process(self) -> dict:
        try:
            date = datetime.now()
            data = req.get('https://www.cbr-xml-daily.ru/daily_json.js').json()

            user_id = self.props['user'].split('_')[-1]
            valute = self.props['valute']
            match valute:
                case 'USD/EUR':
                    message = f"Курсы валют на {date.strftime('%d.%m.%Y %H:%M')}\n{data['Valute']['USD']['Name']}: {data['Valute']['USD']['Value']} руб\n{data['Valute']['EUR']['Name']}: {data['Valute']['EUR']['Value']} руб\n"
                    self.dynamic_token.call_api_method('im.notify.personal.add',
                                                       {'USER_ID': user_id, 'MESSAGE': message})
                case 'CNY/USD':
                    message = f"Курсы валют на {date.strftime('%d.%m.%Y %H:%M')}\n{data['Valute']['CNY']['Name']}: {data['Valute']['CNY']['Value']} руб\n{data['Valute']['USD']['Name']}: {data['Valute']['USD']['Value']} руб\n"
                    self.dynamic_token.call_api_method('im.notify.personal.add',
                                                       {'USER_ID': user_id, 'MESSAGE': message})
                case 'CNY/EUR':
                    message = f"Курсы валют на {date.strftime('%d.%m.%Y %H:%M')}\n{data['Valute']['CNY']['Name']}: {data['Valute']['CNY']['Value']} руб\n{data['Valute']['EUR']['Name']}: {data['Valute']['EUR']['Value']} руб\n"
                    self.dynamic_token.call_api_method('im.notify.personal.add',
                                                       {'USER_ID': user_id, 'MESSAGE': message})

        except Exception as exc:
            return dict(ok=False, error=str(exc))

        return dict(ok=True)

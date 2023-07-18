from integration_utils.bitrix_robots.models import BaseRobot
import requests as req


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
            'Name': {'ru': 'Валюта'},
            'Type': 'string',
            'Required': 'Y',
        },
    }

    RETURN_PROPERTIES = {
        'valute_name': {
            'Name': {'ru': 'Название валюты'},
            'Type': 'string',
            'Required': 'Y',
        },
        'valute_value': {
            'Name': {'ru': 'Значение валюты'},
            'Type': 'double',
            'Required': 'Y',
        },
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
            responce = req.get('https://www.cbr-xml-daily.ru/daily_json.js')
            data = responce.json()
            valute = data['Valute'][self.props['valute']]['Value']
            self.dynamic_token.call_api_method('bizproc.event.send', {"event_token": self.event_token,
                                                                      "return_values": {"valute_value": float(valute),
                                                                                        "valute_name": self.props[
                                                                                            'valute']}})
        except KeyError:
            self.dynamic_token.call_api_method('bizproc.event.send', {"event_token": self.event_token,
                                                                      "return_values": {"valute_value": float(-1),
                                                                                        "valute_name": self.props[
                                                                                            'valute']}})

        except Exception as exc:
            return dict(ok=False, error=str(exc))

        return dict(ok=True)

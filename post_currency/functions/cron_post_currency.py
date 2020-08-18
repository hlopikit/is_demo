from integration_utils.bitrix24.models import BitrixUserToken
import datetime, requests
from django.utils import timezone
from bs4 import BeautifulSoup

EXCHANGE_RATE_URL = 'http://www.cbr.ru/scripts/XML_daily.asp'


def cron_post_currency():
    token = BitrixUserToken.objects.filter(is_active=True, user__is_admin=True).last()

    # token.call_api_method('app.info')['result']

    cb_check_time = timezone.now() + datetime.timedelta(days=1)
    cb_check_time = cb_check_time.strftime('%d/%m/%Y')

    headers = {
        'User-Agent': 'My User Agent 1.0',
    }
    cb_response = requests.get('{}?date_req={}'.format(EXCHANGE_RATE_URL, cb_check_time), headers=headers)

    response_date = None
    if cb_response.status_code == 200:
        cb_response = BeautifulSoup(cb_response.content, "lxml")

        response_date = cb_response.find_all('valcurs')[0].attrs['date']
        formatted_response_date = response_date[0:2] + '/' + response_date[3:5] + '/' + response_date[6:10]

        if formatted_response_date != cb_check_time:
            message = 'Нет курсов валют на эту дату'
        else:
            needed_currencies = ['USD','EUR']
            message = ''

            currencies = cb_response.find_all("valute")
            for currency in currencies:
                if currency.charcode.text in needed_currencies:
                    message += currency.nominal.text + ' ' + currency.find('name').text + ' = ' + currency.value.text + ' руб.\n'

            if not message:
                message = 'Ни одна из необходимых валют не доступна'
    else:
        message = 'Ошибка получения данных от cbr.ru'

    title = 'Курсы валют'
    if response_date:
        title += ' на ' + response_date

    bx_params = dict(
        POST_TITLE='Курсы валют на ' + response_date,
        POST_MESSAGE=message,
    )
    token.call_api_method(
        'log.blogpost.add',
        bx_params
    )

    return True
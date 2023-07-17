from django.shortcuts import render

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from robot_currency.models import CurrencyRobot


@main_auth(on_cookies=True)
def robot_currency(request):

    return render(request, 'robot_currency_temp.html', locals())

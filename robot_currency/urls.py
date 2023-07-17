from django.urls import path

from .models.robot_currency_model import CurrencyRobot
from .views.install import install
from .views.robot_currency_view import robot_currency
from .views.uninstall import uninstall

app_name = 'bitrix_robot_currency'

urlpatterns = [
    path('home/', robot_currency, name='robot_currency_home'),
    path('install/', install, name='install_robot'),
    path('uninstall/', uninstall, name='uninstall_robot'),
    path('handler/', CurrencyRobot.as_view(), name='handler_robot'),
]

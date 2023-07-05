import json

from django.shortcuts import render

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from integration_utils.bitrix24.models import BitrixUserToken
from integration_utils.its_utils.app_get_params import get_params_from_sources

from django.conf import settings


@main_auth(on_cookies=True)
def reload_start(request):
    app_settings = settings.APP_SETTINGS
    return render(request, 'start_page.html', locals())
from django.shortcuts import render
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth

from django.conf import settings

@main_auth(on_start=True, set_cookie=True)
def start(request):
    app_settings = settings.APP_SETTINGS
    return render(request, 'start_page.html', locals())


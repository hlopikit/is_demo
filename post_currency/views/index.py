from django.shortcuts import render
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth


@main_auth(on_start=True, set_cookie=True)
def index(request):
    return render(request, 'post_currency_index.html', locals())

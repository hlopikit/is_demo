from django.shortcuts import render

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth


@main_auth(on_cookies=True)
def entrance(request):
    """
    Отображает описание приложения.
    """

    return render(request, 'export_deals_temp.html')

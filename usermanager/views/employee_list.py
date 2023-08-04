from django.shortcuts import render

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from usermanager.utils.search_manager import search_manager


@main_auth(on_cookies=True)
def employee_list(request):
    """Позволяет найти непосредственного начальника для пользователя."""

    but = request.bitrix_user_token
    user_dict, user_fields = search_manager(but)

    return render(request, 'list.html',
                  context={'fields': user_fields, 'users': user_dict})

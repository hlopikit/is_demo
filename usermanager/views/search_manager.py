from django.shortcuts import render

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from .utils import search_manager_intermediate


@main_auth(on_cookies=True)
def search_manager(request):
    but = request.bitrix_user_token

    manager_dict, user_dict = search_manager_intermediate(but)

    final_list = [list(manager_dict.keys()),
                  [f'{user_dict[i]["NAME"]} {user_dict[i]["LAST_NAME"]}'
                   for i in manager_dict.keys()],
                  list(manager_dict.values()),
                  [f'{user_dict[str(i)]["NAME"]} '
                   f'{user_dict[str(i)]["LAST_NAME"]}'
                   if i != 'Непосредственного начальника не найдено' else
                   'Непосредственного начальника не найдено'
                   for i in manager_dict.values()]]
    final_list = list(zip(*final_list))

    return render(request, 'searchmanager.html', context={
        'final_list': final_list,
    })

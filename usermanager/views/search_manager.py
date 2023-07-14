from django.shortcuts import render

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from .utils import find_manager


@main_auth(on_cookies=True)
def search_manager(request):
    but = request.bitrix_user_token

    # Создаём структуры данных для хранения значений
    user_dict = dict()
    department_info = dict()
    manager_dict = dict()

    users = but.call_list_method('user.get')
    for user in users:
        user_dict[user['ID']] = {
            'NAME': user['NAME'],
            'LAST_NAME': user['LAST_NAME'],
            'UF_DEPARTMENT': user['UF_DEPARTMENT']
        }
        manager_dict[f'{user["ID"]}'] = []

    c = 0

    res_department = but.call_list_method('department.get')
    for department in res_department:
        if 'PARENT' not in department:
            department_info[department['ID']] = {
                'UF_HEAD': department['UF_HEAD']
            }
        elif 'UF_HEAD' not in department:
            department_info[department['ID']] = {
                'PARENT': department['PARENT']
            }
        else:
            department_info[department['ID']] = {
                'UF_HEAD': department['UF_HEAD'],
                'PARENT': department['PARENT']
            }

    # Получаем ID начальников пользователей, которые были найдены ранее
    for user_id, value in user_dict.items():
        for dp in value['UF_DEPARTMENT']:
            for i in res_department:
                if int(i['ID']) == dp:
                    res = i
                    if 'UF_HEAD' in res:
                        if int(res['UF_HEAD']) != 0 and int(res['UF_HEAD']) != \
                                int(user_id):
                            manager_dict[user_id].append(int(res['UF_HEAD']))
                        else:
                            manager_dict[user_id].append(find_manager(
                                but, [res], int(user_id), res_department))
                            c += 1
                    else:
                        manager_dict[user_id].append(find_manager(
                            but, [res], int(user_id), res_department))
                        c += 1

    for user, manager in manager_dict.items():
        manager_sorted = sorted(manager, key=lambda x: isinstance(x, int),
                                reverse=True)
        manager_dict[user] = manager_sorted[0]

    final_list = [list(manager_dict.keys()), [f'{user_dict[i]["NAME"]} {user_dict[i]["LAST_NAME"]}' for i in manager_dict.keys()],
                  list(manager_dict.values()), [f'{user_dict[str(i)]["NAME"]} {user_dict[str(i)]["LAST_NAME"]}' for i in list(manager_dict.values())]]
    final_list = list(zip(*final_list))

    return render(request, 'searchmanager.html', context={
        'final_list': final_list,
    })

from django.shortcuts import render
from pprint import pprint
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from .utils import find_manager


@main_auth(on_cookies=True)
def search_manager(request):
    but = request.bitrix_user_token

    # Создаём структуры данных для хранения значений
    users = but.call_list_method('user.get')
    user_departments = dict()
    user_id_dict = dict()
    id_user_lst = list()
    manager_dict = dict()
    first_and_last_name_manager = list()

    # Получаем пользователей (имя, фамилию, ID, ID их подразделения)
    for user in users:
        user_departments[f'{user["NAME"]} {user["LAST_NAME"]}'] = \
            user["UF_DEPARTMENT"]
        manager_dict[f'{user["NAME"]} {user["LAST_NAME"]}'] = []
        user_id_dict[f'{user["NAME"]} {user["LAST_NAME"]}'] = int(user["ID"])
        id_user_lst.append(user["ID"])

    res_department = but.call_list_method('department.get')
    print(res_department)
    # Получаем ID начальников пользователей, которые были найдены ранее
    for name, department in user_departments.items():
        for dp in department:
            for i in res_department:
                if i['ID'] == dp:
                    res = i
            print(dp)
            res = but.call_api_method('department.get', {"ID": dp})['result']
            print(res)
            if 'UF_HEAD' in res[0]:
                if int(res[0]['UF_HEAD']) != 0 and int(res[0]['UF_HEAD']) != \
                        int(user_id_dict[name]):
                    manager_dict[name].append(int(res[0]['UF_HEAD']))
                else:
                    manager_dict[name].append(find_manager(
                        but, res, int(user_id_dict[name])))
            else:
                manager_dict[name].append(find_manager(
                    but, res, int(user_id_dict[name])))

    for user, manager in manager_dict.items():
        manager_sorted = sorted(manager, key=lambda x: isinstance(x, int),
                                reverse=True)
        manager_dict[user] = manager_sorted[0]

    # Получаем имя и фамилию начальников
    for manager in manager_dict.values():
        res = but.call_api_method('user.get', {"ID": manager})['result'][0]
        first_and_last_name_manager.append(f'{res["NAME"]} {res["LAST_NAME"]}')

    final_list = [id_user_lst, list(manager_dict.keys()),
                  list(manager_dict.values()), first_and_last_name_manager]
    final_list = list(zip(*final_list))

    return render(request, 'searchmanager.html', context={
        'final_list': final_list,
        'len_user': len(id_user_lst)
    })

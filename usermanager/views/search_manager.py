from django.shortcuts import render

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth


@main_auth(on_cookies=True)
def search_manager(request):
    but = request.bitrix_user_token

    # Создаём структуры данных для хранения значений
    users = but.call_list_method('user.get')
    user_departments = dict()
    user_id_dict = dict()
    id_user_lst = list()
    manager_dict = dict()

    # Получаем пользователей (имя, фамилию, ID, ID их подразделения)
    for user in users:
        user_departments[f'ID: {user["ID"]}, {user["NAME"]} {user["LAST_NAME"]}'] = user["UF_DEPARTMENT"]
        manager_dict[f'ID: {user["ID"]}, {user["NAME"]} {user["LAST_NAME"]}'] = []
        user_id_dict[f'ID: {user["ID"]}, {user["NAME"]} {user["LAST_NAME"]}'] = int(user["ID"])
        id_user_lst.append(user["ID"])

    # Получаем ID начальников пользователей, которые были найдены ранее
    for name, department in user_departments.items():
        for dp in department:
            res = but.call_api_method('department.get', {"ID": dp})['result']
            if int(res[0]['UF_HEAD']) != 0 and int(res[0]['UF_HEAD']) != int(user_id_dict[name]):
                manager_dict[name].append(int(res[0]['UF_HEAD']))
            else:
                pass
               ####РЕАЛИЗОВАТЬ ПОИСК РУКОВОДИТЕЛЯ В ВЫШЕСТОЯЩИХ КОМПАНИЯХ
            ######С ПОМОЩЬЮ РЕКУРСИВНОГО ПОИСКА!!!!!!!!!!!
    print(manager_dict)

    return render(request, 'searchmanager.html', locals())
# Функция для рекурсивного поиска непосредственного начальника
# в вышестоящих подразделениях
def find_manager(but, res, user_id, departments):
    # Базовые случаи выхода из рекурсии
    if 'UF_HEAD' not in res[0]:
        parent = res[0]['PARENT']
        for i in departments:
            if parent == i['ID']:
                res = [i]
        return find_manager(but, res, user_id, departments)

    if int(res[0]['UF_HEAD']) != 0 and user_id != int(res[0]['UF_HEAD']):
        return int(res[0]['UF_HEAD'])

    if 'PARENT' not in res[0]:
        return 'Непосредственного начальника не найдено'
    parent = res[0]['PARENT']

    for i in departments:
        if parent == i['ID']:
            res = [i]

    return find_manager(but, res, user_id, departments)


def search_manager_intermediate(but):
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

    return manager_dict, user_dict

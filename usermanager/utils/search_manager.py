def find_supervisor(departments_dict, current_dep='1', order=0):
    """Рекурсивая функция, осуществляющая поиск начальника, если в настоящем
    подразделении он не был найден."""

    department = departments_dict[current_dep]
    parent_exists = ('PARENT' in department)
    supervisor = department.get('UF_HEAD')
    supervisor_exists = (supervisor and (supervisor != '0'))

    if supervisor_exists:
        return department['UF_HEAD'], order
    else:
        if not parent_exists:
            return "None", order
        return find_supervisor(departments_dict, department['PARENT'], order + 1)


def search_manager(but):
    """Осуществляет поиск начальника для пользователя."""

    users = but.call_list_method('user.get')
    departments = but.call_list_method('department.get')

    #  Записываем в словарь юзеров только поля из массива user_fields и их значения.
    user_fields = ['ID', 'NAME', 'LAST_NAME', 'SECOND_NAME', 'UF_DEPARTMENT']
    user_dict = {}
    for element in users:
        user_dict.update({element['ID']: {}})
        for field in user_fields:
            try:
                user_dict[element['ID']].update({field: element[field]})
            except KeyError:
                pass
        user_dict[element['ID']].pop('ID')

    #  Записываем в словарь подразделения
    departments_dict = {}
    for element in departments:
        departments_dict.update({element['ID']: element})
        departments_dict[element['ID']].pop('ID')

    # Проходимся по всем юзерам, для каждого ищем руководителей.
    for user_id in user_dict:
        user = user_dict[user_id]

        # Руководителей записываем в сет, чтобы не искать дубликаты.
        user.update({'SUPERVISORS': set()})
        for department_id in departments_dict:
            #  Смотрим, состоит ли человек в текущем подразделении.
            #  Если состоит, то в качестве кого?
            if departments_dict[department_id].get('UF_HEAD') == user_id:
                if "PARENT" in departments_dict[department_id]:
                    department = departments_dict[department_id]['PARENT']
                    supervisor_id, order = find_supervisor(departments_dict, department, order=1)
                else:
                    supervisor_id = "None"

            else:
                if int(department_id) in user['UF_DEPARTMENT']:
                    department = department_id
                    supervisor_id, order = find_supervisor(departments_dict, department)
                else:
                    continue
            #  В функцию поиска передается родительское подразделение, если в текущем
            #   юзер является руководителем. В ином случае передается текущее.


            if supervisor_id != "None":
                supervisor = user_dict[supervisor_id]
                conj_str = ""
                for key in ['LAST_NAME', 'NAME', 'SECOND_NAME']:
                    try:
                        conj_str += f'{supervisor[key]} '
                    except KeyError:
                        pass
                conj_str += f"| ID: {supervisor_id} | Порядок: {order}"
                user['SUPERVISORS'].add((supervisor_id, conj_str))
        if user['SUPERVISORS'] == set():
            user['SUPERVISORS'] = ""

    for user_id in user_dict:
        user = user_dict[user_id]
        conj_str = ""
        for key in ['LAST_NAME', 'NAME', 'SECOND_NAME']:
            try:
                conj_str += f"{user[key]} "
            except KeyError:
                pass
        conj_str += f"| ID: {user_id}"
        user.update({'FULL_NAME': conj_str})

    return user_dict, user_fields

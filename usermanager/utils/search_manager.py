def find_supervisor(departments_dict, current_dep='1', order=0):
    """Рекурсивая функция, осуществляющая поиск начальника, если в настоящем
    подразделении он не был найден."""

    for department_id in departments_dict:
        department = departments_dict[department_id]
        if department_id == current_dep:
            parent_exists = ('PARENT' in department)
            if 'UF_HEAD' in department:
                supervisor_exists = (department['UF_HEAD'] != '0' )
            else:
                supervisor_exists = False
            break

    if supervisor_exists:

        return department['UF_HEAD'], order

    else:
        if not parent_exists:

            return "None", order

        return find_supervisor(
            departments_dict, department['PARENT'], order + 1
        )


def search_manager(but):
    """Осуществляет поиск начальника для пользователя."""

    users = but.call_api_method('user.get')['result']
    departments = but.call_api_method('department.get')['result']

    #  Записываем в словарь юзеров только поля из массива user_fields
    #  и их значения.
    user_fields = ['ID', 'NAME', 'LAST_NAME', 'SECOND_NAME', 'UF_DEPARTMENT']
    user_dict = {}

    for element in users:
        user_dict.update({element['ID']: {}})

        for field in user_fields:
            try:
                user_dict[element['ID']].update({field: element[field]})
            except KeyError:
                pass

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
            try:
                if departments_dict[department_id]['UF_HEAD'] == user_id:
                    department = departments_dict[department_id]['PARENT']
                else:
                    if int(department_id) in user['UF_DEPARTMENT']:
                        department = department_id
                    else:
                        continue
            except KeyError:
                if int(department_id) in user['UF_DEPARTMENT']:
                    department = department_id
                else:
                    continue
            #  В функцию поиска передается родительское подразделение, если в
            #  текущем юзер является руководителем. В ином случае передается
            #  текущее.
            supervisor_id, order = find_supervisor(departments_dict,
                                                   department)

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
            except:
                pass

        conj_str += f"| ID: {user_id}"
        user.update({'FULL_NAME': conj_str})

    return user_dict, user_fields

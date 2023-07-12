# Функция для рекурсивного поиска непосредственного начальника
# в вышестоящих подразделениях
def find_manager(but, res, user_id):
    # Базовые случаи выхода из рекурсии
    if 'UF_HEAD' not in res[0]:
        parent = res[0]['PARENT']
        res = but.call_api_method('department.get', {"ID": parent})['result']
        return find_manager(but, res, user_id)

    if int(res[0]['UF_HEAD']) != 0 and user_id != int(res[0]['UF_HEAD']):
        return int(res[0]['UF_HEAD'])
    if 'PARENT' not in res[0]:
        return 'Непосредственного начальника не найдено'

    parent = res[0]['PARENT']
    res = but.call_api_method('department.get', {"ID": parent})['result']
    return find_manager(but, res, user_id)

import json

from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from dateutil import parser as dt


@main_auth(on_cookies=True)
def employee_grid(request):
    """Позволяет вывести список юзеров с помощью ag-grid."""

    but = request.bitrix_user_token
    users = but.call_api_method('user.get')['result']

    #  Записываем в словарь юзеров только поля из массива user_fields и их
    #  значения.
    user_fields = [
        'ID',
        'ACTIVE',
        'EMAIL',
        'NAME',
        'LAST_NAME',
        'SECOND_NAME',
        'PERSONAL_GENDER',
        'PERSONAL_PROFESSION',
        'PERSONAL_WWW',
        'PERSONAL_BIRTHDAY',
        'PERSONAL_PHOTO',
        'PERSONAL_ICQ',
        'PERSONAL_PHONE',
        'PERSONAL_FAX',
        'PERSONAL_MOBILE',
        'PERSONAL_PAGER',
        'PERSONAL_STREET',
        'PERSONAL_CITY',
        'PERSONAL_STATE',
        'PERSONAL_ZIP',
        'PERSONAL_COUNTRY',
        'WORK_COMPANY',
        'WORK_POSITION',
        'UF_DEPARTMENT',
        'UF_INTERESTS',
        'UF_SKILLS',
        'UF_WEB_SITES',
        'UF_XING',
        'UF_LINKEDIN',
        'UF_FACEBOOK',
        'UF_TWITTER',
        'UF_SKYPE',
        'UF_DISTRICT',
        'UF_PHONE_INNER',
    ]

    STATUS = {'Y': 'Онлайн', 'N': 'Не онлайн'}
    GENDER = {'M': 'Мужской', 'F': 'Женский', '': 'Не указан'}

    departments = but.call_api_method('department.get')['result']
    departments_dict = {}

    for department in departments:
        departments_dict.update({department['ID']: department})
        departments_dict[department['ID']].pop('ID')

    for user in users:

        # добавляем отсутствующие поля
        for key in user_fields:
            user.setdefault(key, "")

        # формируем строку для ФИО
        fio_str = ""

        for key in ['LAST_NAME', 'NAME', 'SECOND_NAME']:
            fio_str += f"{user[key]} "

        user['FULL_NAME'] = fio_str

        # добавлеям названия подразделений
        user.setdefault('DEPARTMENTS', '')

        for department_id in user['UF_DEPARTMENT']:
            department = str(department_id)
            user['DEPARTMENTS'] += departments_dict[department]['NAME']
            user['DEPARTMENTS'] += "\n"

        # форматируем дату рождения, если она указана
        if user['PERSONAL_BIRTHDAY']:
            user['PERSONAL_BIRTHDAY'] = (
                dt.parse(user['PERSONAL_BIRTHDAY']).strftime('%d.%m.%Y'))

        # добавляем статус
        user['IS_ONLINE'] = STATUS[user['IS_ONLINE']]

        # добавляем пол
        user['PERSONAL_GENDER'] = GENDER[user['PERSONAL_GENDER']]

    json_user_list = json.dumps(users, cls=DjangoJSONEncoder)

    return render(request, 'ag-list.html',
                  context={'json_user_list': json_user_list})

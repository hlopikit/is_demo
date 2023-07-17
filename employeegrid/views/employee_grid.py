import json

from pprint import pprint

from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from dateutil import parser as dt


@main_auth(on_cookies=True)
def employee_grid(request):
    but = request.bitrix_user_token
    users = but.call_api_method('user.get')['result']
    #  Записываем в словарь юзеров только поля из массива user_fields и их значения.
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

    departments = but.call_api_method('department.get')['result']
    departments_dict = {}
    for element in departments:
        departments_dict.update({element['ID']: element})
        departments_dict[element['ID']].pop('ID')

    for user in users:
        for key in user_fields:
            if key not in user.keys():
                user.update({key: ""})
        conj_str = ""
        for key in ['LAST_NAME', 'NAME', 'SECOND_NAME']:
            try:
                conj_str += f"{user[key]} "
            except:
                pass
        user.update({'FULL_NAME': conj_str})
        user.update({'DEPARTMENTS': ""})
        for department_id in user['UF_DEPARTMENT']:
            department = str(department_id)
            user['DEPARTMENTS'] += departments_dict[department]['NAME']
            user['DEPARTMENTS'] += "\n"
        if user['PERSONAL_BIRTHDAY'] != '':
            user['PERSONAL_BIRTHDAY'] = dt.parse(user['PERSONAL_BIRTHDAY']).strftime('%d.%m.%Y')


    json_user_list = json.dumps(users, cls=DjangoJSONEncoder)

    return render(request, '../../employeegrid/templates/ag-list.html', context={'json_user_list': json_user_list})

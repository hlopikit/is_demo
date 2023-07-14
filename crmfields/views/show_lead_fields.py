import json

from dateutil import parser
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from integration_utils.bitrix24.models import BitrixUserToken
from integration_utils.its_utils.app_get_params import get_params_from_sources

from django.conf import settings

@main_auth(on_cookies=True)
def show_lead_fields(request):
    but = request.bitrix_user_token
    res = but.call_api_method("crm.lead.fields")['result']
    len_res = len(res)
    return render(request, 'showleadfields.html', locals())


    admin_token = BitrixUserToken.objects.get(pk=settings.BITRIX_ROBOT_USER_ID)
    admin_token = BitrixUserToken.objects.filter(user__is_admin=True, is_active=True).first()


    #user_id = request.bitrix_user_token.user.bitrix_id
    #if but.call_list_method('profile').get('ADMIN'):
    #    user_id = request.its_params.get('user_id', user_id)



    result = but.call_list_method('task.elapseditem.getlist', [
        {'CREATED_DATE': 'desc'},
        #{'USER_ID': user_id},
    ])

    users = set()
    for r in result:
        users.add(r.get('USER_ID'))

    users = but.call_list_method('user.get', {'filter': {'ID': list(users)}})

    tasks = set()
    for r in result:
        tasks.add(r.get('TASK_ID'))

    tasks = but.call_list_method('tasks.task.list', {'filter': {'ID': list(tasks)}}).get('tasks')

    projects = set()
    for t in tasks:
        projects.add(t.get('groupId'))

    projects = but.call_list_method('sonet_group.get', {'FILTER': {'ID': list(projects)}, 'IS_ADMIN': 'Y'})

    tasks = {t.get('id'): t for t in tasks}
    projects = {p.get('ID'): p for p in projects}
    users = {u.get('ID'): u for u in users}


    # УДАЛИТЬ
    parser.parse("2020-09")

    records = []
    for r in result:
        date = parser.parse(r.get('CREATED_DATE')).date()
        #dates.setdefault(date, {"records": [], "sum": 0})
        records.append(dict(
            id=r.get('ID'),
            task_id='#{}'.format(r.get('TASK_ID')),
            task_name=tasks.get(r.get('TASK_ID')).get('title'),
            project_id='b{}'.format(tasks.get(r.get('TASK_ID')).get('groupId')),
            project_name=projects.get(tasks.get(r.get('TASK_ID')).get('groupId')).get('NAME') if int(tasks.get(r.get('TASK_ID')).get('groupId')) else "Без проекта",
            user_name=users.get(r.get('USER_ID')).get('NAME'),
            date=date,
            description=r.get('COMMENT_TEXT'),
            time=int(r.get('MINUTES')) / 60
        ))

    result = json.dumps(records, cls=DjangoJSONEncoder)
    return render(request, 'get_fact.html', locals())


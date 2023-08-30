from integration_utils.bitrix24.models import BitrixUserToken
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from copy import deepcopy as new

import time


def finish_tasks(request, types):
    but = BitrixUserToken.objects.filter(user__is_admin=True, is_active=True).first()
    # Определяем временной интервал
    match request.POST.get('interval_unit'):
        case "minutes":
            target_date_obj = timezone.now() - relativedelta(minutes=int(request.POST.get('interval_value')))
        case "hours":
            target_date_obj = timezone.now() - relativedelta(hours=int(request.POST.get('interval_value')))
        case "days":
            target_date_obj = timezone.now() - relativedelta(days=int(request.POST.get('interval_value')))
        case "weeks":
            target_date_obj = timezone.now() - relativedelta(weeks=int(request.POST.get('interval_value')))
        case "years":
            target_date_obj = timezone.now() - relativedelta(years=int(request.POST.get('interval_value')))

    target_date_str = target_date_obj.strftime('%Y-%m-%dT%H:%M:%S%z')

    # Создаем список всех дел, подлежащих завершению
    activity_list = []
    for activity_type in types:
        for activity_filter in create_filter_list(activity_type, target_date_str):
            activity_list += but.call_list_method('crm.activity.list', activity_filter, timeout=600)

    # Если список не пуст, завершаем и возвращаем True (для лога).
    # В ином случае возвращаем False.
    if len(activity_list) != 0:
        activity_batch= []
        associated_entity_batch = []
        for activity in activity_list:
            activity_batch.append(('crm.activity.update', {
                "id": activity['ID'],
                "fields": {
                    "COMPLETED": "Y"
                }
            }))
            if activity['ASSOCIATED_ENTITY_ID'] != "0":
                associated_entity_batch.append(('tasks.task.update', {
                    'taskId': activity['ASSOCIATED_ENTITY_ID'],
                    'fields': {
                        'STATUS': '5'
                    }
                }))
        but.batch_api_call(activity_batch, timeout=10800)
        but.batch_api_call(associated_entity_batch, timeout=10800)
        return True

    else:
        return False


def create_auto_finish_loop(request, types):
    while True:
        but = BitrixUserToken.objects.filter(user__is_admin=True, is_active=True).first()
        # В параметрах приложения есть переменная-флаг.
        # Ее значение отражает статус активности цикла.
        flag = but.call_api_method('app.option.get', {})['result']['complete_tasks_flag']
        if flag == "false":
            print("quitting sync loop")
            break

        finish_tasks(request=request, types=types)
        # 86400 секунд == 1 сутки
        time.sleep(86400)


def create_filter_list(activity_type, target_date_str):
    # Шаблон параметров api-запроса на сервер битрикс.
    filter_template = {
        'filter': {
            'COMPLETED': 'N',
            '<CREATED': target_date_str
        },
        'select': [
            'ID',
            'ASSOCIATED_ENTITY_ID'
        ]
    }
    activity_filter_list = []
    template_copy = new(filter_template)
    # Создаем список параметров на основании отмеченных пунктов.
    match activity_type:
        case "meeting":
            template_copy['filter'].update({
                'TYPE_ID': '1',
                'PROVIDER_ID': ['CRM_MEETING']
            })
            activity_filter_list.append(template_copy)
            template_copy_1 = new(filter_template)
            template_copy_1['filter'].update({
                'TYPE_ID': '6',
                'PROVIDER_ID': ["CRM_CALENDAR_SHARING"]
            })
            activity_filter_list.append(template_copy_1)
        case "call":
            template_copy['filter'].update({
                'TYPE_ID': '2',
                'PROVIDER_ID': ['CRM_TASKS_TASK', 'VOXIMPLANT_CALL']
            })
            activity_filter_list.append(template_copy)
        case "to_do":
            template_copy['filter'].update({
                'TYPE_ID': '6',
                'PROVIDER_ID': ['CRM_TODO']
            })
            activity_filter_list.append(template_copy)
        case "email":
            template_copy['filter'].update({
                'TYPE_ID': '4',
                'PROVIDER_ID': ['CRM_EMAIL']
            })
            activity_filter_list.append(template_copy)
        case "task":
            template_copy['filter'].update({
                'TYPE_ID': '6',
                'PROVIDER_ID': ['CRM_TASKS_TASK']
            })
            activity_filter_list.append(template_copy)
        case "other":
            template_copy['filter'].update({
                'TYPE_ID': '6',
                '!PROVIDER_ID': ['CRM_TASKS_TASK', 'CRM_TODO', 'CRM_CALENDAR_SHARING']
            })
            activity_filter_list.append(template_copy)
    return activity_filter_list


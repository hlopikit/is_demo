import threading

from django.shortcuts import render
from integration_utils.bitrix24.models import BitrixUserToken
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from django.utils import timezone
from dateutil.relativedelta import relativedelta
import time


@main_auth(on_cookies=True)
def initiate_completion(request):
    if request.method == 'POST':
        completion_loop_thread = threading.Thread(target=finish_tasks, daemon=True, args=(request,))
        completion_loop_thread.start()
    return render(request, "complete_tasks_page.html")


def finish_tasks(request):
    types = request.POST.get('activity_type').split(",")
    while True:
        print(types)
        but = BitrixUserToken.objects.filter(user__is_admin=True, is_active=True).first()
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
        print(target_date_str)
        activity_list = but.call_api_method('crm.activity.list', {
            'filter': {
                '>CREATED': target_date_str,
                'TYPE_ID': types,
            },
            'select': ['ID', 'ASSOCIATED_ENTITY_ID']
        })['result']

        activity_deletion_batch = []
        associated_entity_deletion_batch = []
        for activity in activity_list:
            activity_deletion_batch.append(('crm.activity.delete', {'id': activity['ID']}))
            if activity['ASSOCIATED_ENTITY_ID'] != "0":
                associated_entity_deletion_batch.append(('tasks.task.update', {
                    'taskId': activity['ASSOCIATED_ENTITY_ID'],
                    'fields': {
                        'STATUS': '5'
                    }
                }))
        but.batch_api_call(activity_deletion_batch)
        but.batch_api_call(associated_entity_deletion_batch)

        try:
            flag = but.call_api_method('app.option.get', {})['result']['flag']
            print("flag found: ", flag)
        except KeyError:
            but.call_api_method('app.option.set', {'options': {'flag': 'false'}})
            flag = "false"
            print("flag not found and set to false")

        if flag == "false":
            print("quitting sync loop")
            break

        # поменять потом
        time.sleep(10)

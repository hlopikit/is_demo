from django.shortcuts import render
from django.http import Http404
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from integration_utils.bitrix24.models.bitrix_user import BitrixUser
from datetime import datetime, timedelta


@main_auth(on_cookies=True)
def move_deadline(request):
    """Сдвигает крайний срок задачи на день по токену админа"""
    if request.method != "POST":
        raise Http404()

    button_type = request.GET.get("type")

    if button_type not in ["admin", "self"]:
        raise Http404()

    resp = render(request, 'move_tasks_deadline_js/move_button.html', {
        "button_type": button_type,
        "path_to_script": "move_tasks_deadline_js/admin.js"
    })

    task_id = request.POST.get("task_id")

    if not task_id:
        return resp

    but = BitrixUser.objects.get(pk=1).bitrix_user_token
    response = but.call_api_method("tasks.task.get", params={
        "taskId": task_id,
        "select": ["DEADLINE", "CREATED_BY"]
    })

    if button_type == "self":
        if int(response["result"]["task"]["createdBy"]) != request.bitrix_user.bitrix_id:
            return resp

    deadline_iso = response["result"]["task"]["deadline"]

    if not deadline_iso:
        return resp

    deadline = datetime.fromisoformat(deadline_iso)
    deadline += timedelta(days=1)
    deadline_iso = deadline.isoformat()

    but.call_api_method("tasks.task.update", params={
        "taskId": task_id,
        "fields": {"DEADLINE": deadline_iso}
    })

    return resp

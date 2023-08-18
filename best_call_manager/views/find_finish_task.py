import html
from django.shortcuts import render
from best_call_manager.utils.table_creation import get_html_row, get_html_table
from best_call_manager.utils.api_methods import *
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth


@main_auth(on_cookies=True)
def find_finish_task(request):
    """Позволяет собрать все результаты завершенных задач. Создает группу
    если она не существует, а если существует берет ее id. По результату
    задач находит нужный звонок и делает пост с таблицей лучших звонков
    каждого менеджера."""

    if request.method == "POST":
        but = request.bitrix_user_token
        group = get_app_group(but)
        if group["result"]:
            group_id = group["result"][0]["ID"]
        else:
            group_id = create_app_group(but)

        app_tasks_id = get_app_tasks_id(but)
        app_tasks = get_app_tasks(but, app_tasks_id)

        progress_tasks_id = app_tasks_id if app_tasks_id else []
        completed_tasks = dict()

        for app_task in app_tasks:
            if app_task["status"] == '5':
                progress_tasks_id.remove(app_task["id"])
                completed_tasks[app_task["id"]] = app_task

        if not completed_tasks:
            return render(request, 'best_call_manager_temp.html')

        set_app_tasks_id(but, progress_tasks_id)

        calls = dict()
        for task_id, task in completed_tasks.items():
            task_res = get_task_res(but, task_id)
            calls[task_res["text"]] = task["responsible"]["name"]

        app_calls = get_app_calls(but, list(calls.keys()))

        rows = ""
        for counter, app_call in enumerate(app_calls, 1):
            row = get_html_row(app_call, calls, counter)
            rows += row

        html_table = get_html_table(rows)
        add_post(but, f"{html.unescape(html_table)}", [f"SG{group_id}"])

    return render(request, "best_call_manager_temp.html")

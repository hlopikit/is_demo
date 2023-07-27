import html

from django.shortcuts import render

from best_call_manager.utils.row_in_table import row_in_table
from best_call_manager.utils.table_for_post import table_for_post
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth


@main_auth(on_cookies=True)
def find_finish_task(request):
    """Позволяет собрать все результаты завершенных задач. Создает группу
    если она не существует, а если существует берет ее id. По результату
    задач находит нужный звонок и делает пост с таблицей лучших звонков
    каждого менеджера."""

    but = request.bitrix_user_token
    if request.method == 'POST':
        group = but.call_api_method('sonet_group.get', {
            "FILTER": {"NAME": "Лучший звонок за день"}})
        group_id = None
        if group['result']:
            group_id = group['result'][0]['ID']
        else:
            group_id = but.call_api_method('sonet_group.create', {
                "NAME": "Лучший звонок за день", "VISIBLE": "Y",
                "OPENED": "Y"})['result']

        all_tasks = but.call_list_method('tasks.task.list', {
            "filter": {"TITLE": "Лучший звонок за день"},
            "select": ["ID", "TITLE", "STATUS", "RESPONSIBLE_ID",
                       "CREATED_DATE"]})['tasks']

        get_tasks = but.call_list_method('app.option.get', {"option": 'tasks'})

        tasks_progress = get_tasks if get_tasks else []
        tasks = list()

        for task in all_tasks:
            if task['status'] == '5':
                if task['id'] in tasks_progress:
                    tasks_progress.remove(task['id'])
                    tasks.append(task)
            else:
                if task['id'] not in tasks_progress:
                    tasks_progress.append(task['id'])

        but.call_list_method('app.option.set',
                             {"options": {'tasks': tasks_progress}})

        calls = dict()
        if tasks:
            for task in tasks:
                result = but.call_api_method("tasks.task.result.list", {
                    "taskId": task['id']})['result'][0]
                calls[result["text"]] = [task['responsible']['name']]

            all_calls = but.call_list_method('voximplant.statistic.get')
            fields = ''
            counter = 1
            for call in all_calls:
                if call['ID'] in calls:
                    field = row_in_table(call, calls, counter)
                    fields += field
                    counter += 1
            table = table_for_post(fields)
            but.call_list_method('log.blogpost.add',
                                 {"POST_TITLE": f'Новые лучшие звонки',
                                  "POST_MESSAGE": f"{html.unescape(table)}",
                                  "DEST": [f'SG{group_id}']})

    return render(request, 'best_call_manager_temp.html', locals())

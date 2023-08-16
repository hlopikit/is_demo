from django.shortcuts import render

from best_call_manager.utils.datetime_utils import get_now_date
from best_call_manager.utils.setting_goals import setting_goals
from best_call_manager.utils.api_methods import *
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth


@main_auth(on_cookies=True)
def start_find_all_call(request):
    """Позволяет получить все звонки, найти среди них подходящие по условию,
    и поставить пользователям задачу на выбор лучшего звонка за каждый день
    когда они были совершены, также пользователям в комментарии к задаче
    отправляется таблица с удобочитаемыми данными, чтобы пользователь смог
    проанализировать информацию и сделать выбор"""

    if request.method == "POST":
        but = request.bitrix_user_token
        now_date = get_now_date()
        try:
            app_date = get_app_date(but)

            if app_date == now_date:
                return render(request, "best_call_manager_temp.html")
            else:
                calls = get_new_calls(but, app_date, now_date)

        except (TypeError, KeyError):
            calls = get_old_calls(but, now_date)

        task_id_list = setting_goals(but, calls)
        app_tasks_id = get_app_tasks_id(but)
        if app_tasks_id:
            app_tasks_id.extend(task_id_list)
        else:
            app_tasks_id = task_id_list

        set_app_tasks_id(but, app_tasks_id)
        set_app_date(but, now_date)

    return render(request, "best_call_manager_temp.html")

from django.shortcuts import render

from best_call_manager.utils.now_date import now_date
from best_call_manager.utils.setting_goals import setting_goals
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth


@main_auth(on_cookies=True)
def start_find_all_call(request):
    """Позволяет получить все звонки, найти среди них подходящие по условию,
    и поставить пользователям задачу на выбор лучшего звонка за каждый день
    когда они были совершены, также пользователям в комментарии к задаче
    отправляется таблица с удобочитаемыми данными, чтобы пользователь смог
    проанализировать информацию и сделать выбор."""

    but = request.bitrix_user_token

    if request.method == 'POST':
        try:
            resp = but.call_api_method('app.option.get')
            time = now_date()
            options = resp['result']['DATE_FROM_APP_BEST_CALL_MANAGER']

            if options == time:
                pass
            else:
                res = but.call_list_method('voximplant.statistic.get',
                                           {"FILTER": {
                                               ">CALL_START_DATE":
                                                   f"{options}",
                                           }})

                task_id_list = setting_goals(but, res)
                get_tasks = but.call_list_method('app.option.get',
                                                 {"option": 'tasks'})
                if get_tasks:
                    get_tasks += task_id_list
                else:
                    get_tasks = task_id_list

                but.call_api_method('app.option.set', {
                    "options": {'DATE_FROM_APP_BEST_CALL_MANAGER': time,
                                'tasks': get_tasks}})
        except:
            time = now_date()
            res = but.call_list_method('voximplant.statistic.get', {"FILTER": {
                "<CALL_START_DATE": f"{time}",
            }})

            task_id_list = setting_goals(but, res)
            get_tasks = but.call_list_method('app.option.get',
                                             {"option": 'tasks'})
            if get_tasks:
                get_tasks += task_id_list
            else:
                get_tasks = task_id_list

            but.call_api_method('app.option.set', {
                "options": {'DATE_FROM_APP_BEST_CALL_MANAGER': time,
                            'tasks': get_tasks}})

    return render(request, 'best_call_manager_temp.html', locals())

from prettytable import PrettyTable
from django.shortcuts import render

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from .utils import filter_yesterday_day, parse_date, call_type
from usermanager.views.utils import search_manager_intermediate


@main_auth(on_cookies=True)
def start_find_all_call(request):

    but = request.bitrix_user_token
    res = but.call_list_method('voximplant.statistic.get')
    filter_res = filter_yesterday_day(res)
    manager_dict, user_dict = search_manager_intermediate(but)
    manager_calls = dict()

    for res in filter_res:
        if res['PORTAL_USER_ID'] in manager_calls.keys():
            manager_calls[res['PORTAL_USER_ID']].append(res)
        else:
            manager_calls[res['PORTAL_USER_ID']] = [res]

    for manager, calls in manager_calls.items():
        counter = 1

        table = PrettyTable()
        table.field_names = ["№", "ID звонка", "Номер телефона",
                             "Дата и время звонка", "Длительность звонка",
                             "Тип звонка"]

        for call in calls:
            table.add_row([f'{counter}', call['ID'],
                           call['PHONE_NUMBER'],
                           parse_date(call['CALL_START_DATE']),
                           f"{call['CALL_DURATION']} секунд",
                           call_type(call['CALL_TYPE'])])
            counter += 1

        if (manager_dict[manager] !=
                'Непосредственного начальника не найдено'):
            but.call_api_method('tasks.task.add', {'fields': {
                "TITLE": 'Лучший звонок за день',
                "CREATED_BY": manager_dict[manager],
                "RESPONSIBLE_ID": manager,
                "DESCRIPTION": f"[FONT=monospace]{table}[/FONT]"
                               f"\n\n\nВ качестве результата этой задачи "
                               f"напишите, пожалуйста, ID звонка.",
                "TASK_CONTROL": 'N'
            }})
        else:
            but.call_api_method('tasks.task.add', {'fields': {
                "TITLE": 'Лучший звонок за день',
                "CREATED_BY": int(manager),
                "RESPONSIBLE_ID": manager,
                "DESCRIPTION": f"[FONT=monospace]{table}[/FONT]"
                               f"\n\n\nВ качестве результата этой задачи "
                               f"напишите, пожалуйста, ID звонка.",
            }})

    return render(request, 'best_call_manager_temp.html', locals())

from prettytable import PrettyTable

from best_call_manager.utils.add_row import add_row
from best_call_manager.utils.api_method_task_add_with_manager import \
    api_method_task_add_with_manager
from best_call_manager.utils.api_method_task_add_without_manager import \
    api_method_task_add_without_manager
from best_call_manager.utils.parse_date_iso import parse_date_iso
from usermanager.utils.search_manager import search_manager


def setting_goals(but, res):
    """Позволяет поставить задачи по выбору лучшего звонка пользователям."""

    task_id_list = list()
    user_dict, user_fields = search_manager(but)
    res_manager_dict = dict()

    for id_manager, value in user_dict.items():
        if value['SUPERVISORS'] == '':
            res_manager_dict[id_manager] = \
                'Непосредственного начальника не найдено'
        else:
            res_manager_dict[id_manager] = next(iter(value['SUPERVISORS']))[0]

    manager_dict = res_manager_dict
    manager_calls = dict()

    for res in res:

        if res['PORTAL_USER_ID'] in manager_calls.keys():
            manager_calls[res['PORTAL_USER_ID']].append(res)
        else:
            manager_calls[res['PORTAL_USER_ID']] = [res]

    for manager_id, call_list in manager_calls.items():
        manager_calls[manager_id] = sorted(call_list, key=lambda x: x[
            'CALL_START_DATE'])

    for manager, calls in manager_calls.items():
        date_check = None
        counter = 1
        counter_for_calls = 1
        table = PrettyTable()
        table.field_names = ["№", "ID звонка", "Номер телефона",
                             "Дата и время звонка",
                             "Длительность звонка",
                             "Тип звонка"]

        for call in calls:

            if date_check is None:
                date_check = call['CALL_START_DATE'][0:10]

            if call['CALL_START_DATE'][0:10] == date_check:
                add_row(table, counter, call)
                counter += 1

                if counter_for_calls == len(calls):

                    if (manager_dict[manager] !=
                            'Непосредственного начальника не найдено'):
                        task_id = api_method_task_add_with_manager(but,
                                                                   manager,
                                                                   manager_dict,
                                                                   table,
                                                                   parse_date_iso(table.rows[0][3][0:11]))
                        task_id_list.append(task_id)
                    else:
                        task_id = api_method_task_add_without_manager(but,
                                                                      manager,
                                                                      table,
                                                                      parse_date_iso(table.rows[0][3][0:11]))
                        task_id_list.append(task_id)
                else:
                    counter_for_calls += 1
            else:
                if (manager_dict[manager] !=
                        'Непосредственного начальника не найдено'):
                    task_id = api_method_task_add_with_manager(but, manager,
                                                               manager_dict,
                                                               table,
                                                               parse_date_iso(table.rows[0][3][0:11]))
                    task_id_list.append(task_id)
                else:
                    task_id = api_method_task_add_without_manager(but, manager,
                                                                  table,
                                                                  parse_date_iso(table.rows[0][3][0:11]))
                    task_id_list.append(task_id)

                date_check = call['CALL_START_DATE'][0:10]
                table.clear_rows()
                counter = 1
                add_row(table, counter, call)
                counter += 1

                if counter_for_calls == len(calls):
                    if (manager_dict[manager] !=
                            'Непосредственного начальника не найдено'):
                        task_id = api_method_task_add_with_manager(but,
                                                                   manager,
                                                                   manager_dict,
                                                                   table,
                                                                   parse_date_iso(table.rows[0][3][0:11]))
                        task_id_list.append(task_id)
                    else:
                        task_id = api_method_task_add_without_manager(but,
                                                                      manager,
                                                                      table,
                                                                      parse_date_iso(table.rows[0][3][0:11]))
                        task_id_list.append(task_id)
                else:
                    counter_for_calls += 1

    return task_id_list

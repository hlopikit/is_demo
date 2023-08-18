from prettytable import PrettyTable
from best_call_manager.utils.table_creation import add_row, add_row_to_df
from best_call_manager.utils.api_methods import add_task
from best_call_manager.utils.datetime_utils import parse_date_in_dmy
from usermanager.utils.search_manager import search_manager
import pandas as pd


def setting_goals(but, calls):
    """Позволяет поставить задачи по выбору лучшего звонка пользователям."""

    user_dict, user_fields = search_manager(but)
    manager_dict = dict()

    for manager_id, user in user_dict.items():
        if user["SUPERVISORS"] == "":
            manager_dict[manager_id] = manager_id
        else:
            manager_dict[manager_id] = next(iter(user["SUPERVISORS"]))[0]

    call_info_df = pd.DataFrame(
        columns=["CALL_ID", "MANAGER_ID", "PHONE_NUMBER",
                 "START_DATE", "START_DATETIME", "DURATION", "CALL_TYPE"])

    for call in calls:
        add_row_to_df(call_info_df, call)

    call_info_df.sort_values(by="START_DATETIME", inplace=True)
    call_info_df = call_info_df.groupby(["MANAGER_ID", "START_DATE"])

    table = PrettyTable()
    table.field_names = ["№", "ID звонка", "Номер телефона",
                         "Дата и время звонка",
                         "Длительность звонка",
                         "Тип звонка"]

    task_id_list = list()

    for group, call_df in call_info_df:
        call_df.reset_index(drop=True, inplace=True)
        table.clear_rows()
        for index, row in call_df.iterrows():
            add_row(table, index.__hash__() + 1, row)
        task_id = add_task(but, group[0], manager_dict[group[0]], table,
                           parse_date_in_dmy(group[1]))
        task_id_list.append(task_id)

    return task_id_list

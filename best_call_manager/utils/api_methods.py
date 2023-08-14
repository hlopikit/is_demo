def add_task(but, manager_id, supervisor_id, table, date):
    """Позволяет поставить задачу пользователю от вышестоящего руководителя."""

    task_id = but.call_api_method("tasks.task.add",
                                  {"fields": {
                                      "TITLE": f"Оценить свой лучший звонок "
                                               f"за {date}",
                                      "CREATED_BY": supervisor_id,
                                      "RESPONSIBLE_ID": manager_id,
                                      "DESCRIPTION":
                                          f"[FONT=monospace]{table}[/FONT]"
                                          f"\n\n\nВ качестве результата этой "
                                          f"задачи напишите, пожалуйста, "
                                          f"ID звонка.",
                                      "TASK_CONTROL": 'N'
                                  }})["result"]["task"]["id"]

    return task_id


def get_new_calls(but, date):
    """Поозволяет получить все звонки с портала"""

    calls = but.call_list_method("voximplant.statistic.get",
                                 {"FILTER": {
                                     ">=CALL_START_DATE": date
                                 }})
    return calls


def get_old_calls(but, date):
    """Поозволяет получить все звонки с портала"""

    calls = but.call_list_method("voximplant.statistic.get",
                                 {"FILTER": {
                                     "<CALL_START_DATE": date
                                 }})
    return calls


def get_tasks(but):
    """Позволяет получить все задачи, связанные с текущим приложением"""

    tasks = but.call_list_method("app.option.get",
                                 {"option": "tasks"})
    return tasks


def add_tasks(but, date, tasks):
    """Позволяет добавить задачи в опции текущего приложения"""

    but.call_api_method("app.option.set", {
        "options": {"DATE_FROM_APP_BEST_CALL_MANAGER": date,
                    "tasks": tasks}})

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
                                     "<=CALL_START_DATE": date
                                 }})
    return calls


def get_old_calls(but, date):
    """Поозволяет получить все звонки с портала"""

    calls = but.call_list_method("voximplant.statistic.get",
                                 {"FILTER": {
                                     "<CALL_START_DATE": date
                                 }})
    return calls


def get_app_calls(but, calls_id):
    app_calls = but.call_list_method("voximplant.statistic.get", {
        "filter": {"ID": calls_id},
        "select": ["ID", "PHONE_NUMBER", "CALL_DURATION", "RECORD_FILE_ID",
                   "CALL_START_DATE", "CALL_TYPE"]
    })
    return app_calls


def get_app_tasks_id(but):
    """Позволяет получить все задачи, связанные с текущим приложением"""

    tasks_id = but.call_list_method("app.option.get",
                                    {"option": "tasks"})
    return tasks_id


def set_app_tasks_id(but, tasks_id):
    """Позволяет добавить задачи в опции текущего приложения"""

    but.call_api_method("app.option.set", {
        "options": {"tasks": tasks_id}})


def set_app_date(but, date):
    but.call_api_method("app.option.set", {
        "options": {"DATE_FROM_APP_BEST_CALL_MANAGER": date}})


def get_app_date(but):
    options = but.call_api_method("app.option.get")
    app_date = options["result"]["DATE_FROM_APP_BEST_CALL_MANAGER"]
    return app_date


def get_app_group(but):
    group = but.call_api_method("sonet_group.get", {
        "FILTER": {"NAME": "Лучший звонок за день"}})
    return group


def create_app_group(but):
    group_id = but.call_api_method("sonet_group.create", {
        "NAME": "Лучший звонок за день", "VISIBLE": "Y",
        "OPENED": "Y"})["result"]
    return group_id


def get_app_tasks(but, app_tasks_id):
    app_tasks = but.call_list_method("tasks.task.list", {
        "filter": {"ID": app_tasks_id},
        "select": ["ID", "TITLE", "STATUS", "RESPONSIBLE_ID",
                   "CREATED_DATE"]})["tasks"]
    return app_tasks


def get_task_res(but, task_id):
    task_res = but.call_api_method("tasks.task.result.list", {
        "taskId": task_id})["result"][-1]
    return task_res


def add_post(but, message, dest):
    but.call_list_method("log.blogpost.add",
                         {"POST_TITLE": f"Новые лучшие звонки",
                          "POST_MESSAGE": message,
                          "DEST": dest})


def update(but):
    but.call_api_method("app.option.set", {
        "options": {"tasks": None}})

def api_method_task_add_with_manager(but, manager, manager_dict, table):
    """Позволяет поставить задачу пользователю от вышестоящего руководителя."""

    task_id = but.call_api_method('tasks.task.add',
                                  {'fields': {
                                      "TITLE": 'Лучший звонок за день',
                                      "CREATED_BY":
                                          manager_dict[
                                              manager],
                                      "RESPONSIBLE_ID": manager,
                                      "DESCRIPTION": f"[FONT=monospace]{table}[/FONT]"
                                                     f"\n\n\nВ качестве результата этой "
                                                     f"задачи "
                                                     f"напишите, пожалуйста, ID звонка.",
                                      "TASK_CONTROL": 'N'
                                  }})['result']['task']['id']

    return task_id

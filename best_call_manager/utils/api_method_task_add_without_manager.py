def api_method_task_add_without_manager(but, manager, table, date):
    """Позволяет поставить задачу пользователю от самого себя, так как у него
    нет вышестоящего руководителя."""

    task_id = but.call_api_method('tasks.task.add', {'fields': {
        "TITLE": f'Оценить свой лучший звонок за {date}',
        "CREATED_BY": int(manager),
        "RESPONSIBLE_ID": manager,
        "DESCRIPTION": f"[FONT=monospace]{table}[/FONT]"
                       f"\n\n\nВ качестве результата этой задачи "
                       f"напишите, пожалуйста, ID звонка.",
    }})['result']['task']['id']

    return task_id

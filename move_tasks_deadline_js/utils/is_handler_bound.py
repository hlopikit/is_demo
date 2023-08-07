from django.urls import reverse
from django.conf import settings


def is_bound(bitrix_user_token):
    """Узнаем связано ли мес
    то встаривания в окне просмотра задачи с хендлером"""
    response = bitrix_user_token.call_api_method("placement.get")

    handler = settings.DOMAIN + reverse("move_tasks_deadline_js:move_button")
    placement = "TASK_VIEW_SIDEBAR"

    for r in response["result"]:
        if r["handler"] == handler and r["placement"] == placement:
            return True

    return False

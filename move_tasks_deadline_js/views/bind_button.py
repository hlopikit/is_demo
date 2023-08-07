from django.shortcuts import render
from django.urls import reverse
from django.conf import settings
from django.http import Http404
from ..utils.is_handler_bound import is_bound
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth


@main_auth(on_cookies=True)
def bind_button(request):
    """Привязываем хендлер к окну просмотра задачи"""
    if request.method == "GET":
        raise Http404()

    if request.bitrix_user.is_admin:
        bound = is_bound(request.bitrix_user_token)

        if bound:
            message = "Место встраивания уже связано с обработчиком"
        else:
            response = request.bitrix_user_token.call_api_method("placement.bind", params={
                "PLACEMENT": "TASK_VIEW_SIDEBAR",
                "HANDLER": settings.DOMAIN + reverse('move_tasks_deadline_js:move_button')
            })

            if response:
                message = "Связывание прошло успешно"
                bound = True
            else:
                message = "Что-то пошло не так"
    else:
        message = "Только администраторы могут привязывать."

    return render(request, 'move_tasks_deadline_js/index.html', {
        "message": message,
        "bound": bound
    })

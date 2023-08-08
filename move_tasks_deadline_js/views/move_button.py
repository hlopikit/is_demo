from django.shortcuts import render
from django.http import Http404
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth


@main_auth(on_start=True, set_cookie=True)
def move_button(request):
    """Страница с кнопкой сдвига крайнего срока для вставки в окно просмотра задачи"""
    button_type = request.GET.get("type")

    if button_type not in ["js", "admin", "self"]:
        raise Http404()

    script_name = button_type
    if button_type == "self":
        script_name = "admin"

    path_to_script = f"move_tasks_deadline_js/{ script_name }.js"

    return render(request, 'move_tasks_deadline_js/move_button.html', {
        "button_type": button_type,
        "path_to_script": path_to_script
    })

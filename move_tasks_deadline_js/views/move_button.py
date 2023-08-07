from django.shortcuts import render
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth


@main_auth(on_start=True)
def move_button(request):
    """Страница с кнопкой сдвига крайнего срока для вставки в окно просмотра задачи"""
    return render(request, 'move_tasks_deadline_js/move_button.html')

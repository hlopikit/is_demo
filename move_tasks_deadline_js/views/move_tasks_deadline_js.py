from django.shortcuts import render
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth


@main_auth(on_start=True)
def index(request):
    return render(request, 'move_tasks_deadline_js/index.html')

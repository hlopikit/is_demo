from django.http import HttpResponse
from django.shortcuts import render
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from ..utils.utils import create_auto_finish_loop

import threading


@main_auth(on_cookies=True)
def initiate_auto_finish_loop(request):
    if request.method == 'POST':
        types = request.POST.get('activity_type').split(",")
        if types != ['']:
            auto_finish_loop = threading.Thread(target=create_auto_finish_loop, args=(request, types), daemon=True)
            auto_finish_loop.start()
            return HttpResponse("")

    return render(request, 'finish_tasks_page.html')

from django.shortcuts import render
from django.http import HttpResponse

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from ..utils.utils import finish_tasks


@main_auth(on_cookies=True)
def finish_tasks_once(request):
    if request.method == 'POST':
        types = request.POST.get('activity_type').split(",")
        res = finish_tasks(request=request, types=types)
        if res:
            return HttpResponse("Activities finished successfully.")
        else:
            return HttpResponse("No activities to finish.")
    return render(request, 'finish_tasks_page.html')


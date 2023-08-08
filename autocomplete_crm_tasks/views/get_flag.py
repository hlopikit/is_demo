from django.http import HttpResponse
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from integration_utils.bitrix24.models import BitrixUserToken


@main_auth(on_cookies=True)
def get_flag(request):
    if request.method == 'GET':
        but = BitrixUserToken.objects.filter(user__is_admin=True, is_active=True).first()
        try:
            print(but.call_api_method('app.option.get', {}))
            flag = but.call_api_method('app.option.get', {})['result']['complete_tasks_flag']
        except (KeyError, TypeError):
            flag = "false"
            print(flag)
            but.call_api_method('app.option.set', {'options': {'complete_tasks_flag': flag}})
        return HttpResponse(f"{flag}")
    return HttpResponse("Invalid state or token.")

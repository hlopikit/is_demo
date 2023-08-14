from django.http import HttpResponse
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from integration_utils.bitrix24.models import BitrixUserToken


@main_auth(on_cookies=True)
def set_flag(request):
    if request.method == 'POST':
        but = BitrixUserToken.objects.filter(user__is_admin=True, is_active=True).first()
        state = request.POST.get('state')
        but.call_api_method('app.option.set', {'options': {'call_sync_flag': state}})
        return HttpResponse(f"Flag set to {state}")
    return HttpResponse("Invalid token.")
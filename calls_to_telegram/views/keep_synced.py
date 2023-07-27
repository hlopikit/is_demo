from django.http import HttpResponse

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from calls_to_telegram.utils.utils import keep_call_info_synced


@main_auth(on_cookies=True)
def keep_synced(request):
    if request.method == 'POST':
        bot_token = request.POST.get('bot_token')
        calls_chat_id = request.POST.get('calls_chat_id')
        keep_call_info_synced(bot_token, calls_chat_id)
        return HttpResponse("Continuous synchronization is ongoing")

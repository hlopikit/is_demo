from django.shortcuts import render

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from calls_to_telegram.utils.utils import export_calls_to_telegram


@main_auth(on_cookies=True)
def export_calls(request):
    if request.method == 'POST':
        bot_token = request.POST.get('bot_token')
        calls_chat_id = request.POST.get('calls_chat_id')
        export_calls_to_telegram(bot_token, calls_chat_id)
    return render(request, "send_button_page.html")




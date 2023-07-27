from django.shortcuts import render

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth

from integration_utils.vendors.telegram import Bot


@main_auth(on_cookies=True)
def send_message(request):
    if request.method == 'POST':
        bot_token = request.POST.get('bot_token')
        chat_id = request.POST.get('chat_id')
        message_text = request.POST.get('message_text')
        # print(bot_token, chat_id, message_text)
        bot = Bot(token=bot_token)
        bot.send_message(text=message_text, chat_id=chat_id)


    return render(request, 'msg_input.html')

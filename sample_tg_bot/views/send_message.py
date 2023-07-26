from django.shortcuts import render
from telegram import Bot
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
import asyncio

@main_auth(on_cookies=True)
def send_message(request):
    if request.method == 'POST':
        bot_token = request.POST.get('bot_token')
        chat_id = request.POST.get('chat_id')
        message_text = request.POST.get('message_text')
        # print(bot_token, chat_id, message_text)
        bot = Bot(token=bot_token)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        async_result = loop.run_until_complete(bot.send_message(text=message_text, chat_id=chat_id))
        loop.close()

    return render(request, 'msg_input.html')

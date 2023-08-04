import threading

from django.shortcuts import render

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from tg_openai_bot.cron import handle_bot_updates


def run_bot_thread():
    while True:  # Needed cron func, while only in prod stage
        handle_bot_updates('tg_openai_bot.models.open_ai_bot.OpenAiBot')


@main_auth(on_cookies=True)
def start_page_open_ai(request):
    if request.method == 'POST':
        foo_loop = threading.Thread(target=run_bot_thread(), daemon=True)
        foo_loop.start()
    return render(request, 'open_ai_start.html')
